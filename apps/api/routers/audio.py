from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from core.cache import cache, TTL_AUDIO_META
from core.storage import generate_presigned_url
from schemas.schemas import AudioFileResponse, PerspectiveResponse
from models.models import AudioFile, Perspective

router = APIRouter()


@router.get("/events/{event_id}/audio", response_model=List[AudioFileResponse])
async def get_event_audio(event_id: str, db: AsyncSession = Depends(get_db)):
    """Get all audio files for an event (all perspectives) with presigned URLs."""
    cache_key = f"audio_meta:{event_id}"
    cached_audio = await cache.get(cache_key)

    if not cached_audio:
        query = select(AudioFile).where(
            AudioFile.event_id == event_id,
            AudioFile.is_active == True
        )
        result = await db.execute(query)
        audio_files = result.scalars().all()
        
        if not audio_files:
            return []
            
        cached_audio = [
            {
                "id": a.id,
                "perspective_type": a.perspective_type,
                "voice_id": a.voice_id,
                "duration_seconds": a.duration_seconds,
                "format": a.format,
                "transcript": a.transcript,
                "s3_key": a.s3_key
            } for a in audio_files
        ]
        await cache.set(cache_key, cached_audio, TTL_AUDIO_META)

    # Generate fresh presigned URLs on every request (don't cache the URL itself long-term)
    response = []
    for audio in cached_audio:
        url = generate_presigned_url(audio["s3_key"])
        response.append({
            **audio,
            "presigned_url": url
        })

    return response


@router.get("/events/{event_id}/perspectives", response_model=List[PerspectiveResponse])
async def get_event_perspectives(event_id: str, db: AsyncSession = Depends(get_db)):
    """Get text/metadata for all perspectives on an event."""
    query = select(Perspective).where(Perspective.event_id == event_id)
    result = await db.execute(query)
    perspectives = result.scalars().all()
    return perspectives
