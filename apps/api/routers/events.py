from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from core.database import get_db
from core.cache import cache, TTL_TIMELINE, TTL_EVENT
from schemas.schemas import EventListItem, EventDetail, PaginatedResponse
from models.models import Event, Era
from core.storage import generate_presigned_url

router = APIRouter()


@router.get("/timeline", response_model=PaginatedResponse)
async def get_timeline(
    era: Optional[str] = None,
    topic: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50),
    cursor_year: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get scrollable timeline of events."""
    cache_key = f"timeline:{era}:{topic}:{limit}:{cursor_year}"
    cached = await cache.get(cache_key)
    if cached:
        return cached

    query = select(Event).options(
        selectinload(Event.era), 
        selectinload(Event.audio_files)
    ).where(Event.is_published == True)

    if era:
        query = query.where(Event.era_id == era)
    if topic:
        query = query.where(Event.topics.any(topic))
    if cursor_year is not None:
        query = query.where(Event.year < cursor_year)

    query = query.order_by(desc(Event.year)).limit(limit + 1)
    result = await db.execute(query)
    events = result.scalars().all()

    has_more = len(events) > limit
    items = events[:limit]
    
    next_cursor = str(items[-1].year) if has_more and items else None

    # Transform to response schema dicts for caching
    data = [
        EventListItem.model_validate({
            **item.__dict__,
            "era": item.era,
            "perspectives_count": 0, 
            "audio_preview_url": generate_presigned_url(item.audio_files[0].s3_key) if getattr(item, 'audio_files', None) else None,
            "duration_seconds": item.audio_files[0].duration_seconds if getattr(item, 'audio_files', None) else None,
        }).model_dump(mode='json')
        for item in items
    ]
    
    response = {
        "data": data,
        "next_cursor": next_cursor,
        "total": 0 # Optimization: avoid slow count(*) on large tables
    }

    await cache.set(cache_key, response, TTL_TIMELINE)
    return response


@router.get("/events", response_model=List[EventListItem])
async def list_events(
    db: AsyncSession = Depends(get_db)
):
    """Get all published events (basic list)."""
    query = select(Event).options(selectinload(Event.era)).where(Event.is_published == True).limit(50)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/events/{event_id}", response_model=EventDetail)
async def get_event(event_id: str, db: AsyncSession = Depends(get_db)):
    """Get full details for a specific event."""
    cache_key = f"event:{event_id}"
    cached = await cache.get(cache_key)
    if cached:
        return cached

    query = select(Event).options(
        selectinload(Event.era)
    ).where(Event.id == event_id)
    
    result = await db.execute(query)
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    response = EventDetail.model_validate(event).model_dump(mode='json')
    await cache.set(cache_key, response, TTL_EVENT)
    return response

import httpx
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    event_id: str
    event_name: str
    summary_text: str
    era_label: str

@router.post("/events/generate")
async def trigger_generation(req: GenerateRequest):
    """Trigger the asynchronous AI generation pipeline in the worker service."""
    try:
        # Calls the internal docker network address of the worker service
        async with httpx.AsyncClient() as client:
            resp = await client.post("http://worker:3001/generate", json={
                "eventId": req.event_id,
                "eventName": req.event_name,
                "summaryText": req.summary_text,
                "eraLabel": req.era_label
            }, timeout=10.0)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Worker communication failed: {str(e)}")
