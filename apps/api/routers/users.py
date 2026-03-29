from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from core.auth import verify_token
from schemas.schemas import ContributionCreate, ContributionResponse
from models.models import Contribution
import uuid

router = APIRouter()


@router.post("/contributions", response_model=ContributionResponse, status_code=status.HTTP_201_CREATED)
async def create_contribution(
    contrib: ContributionCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(verify_token)
):
    """
    Submit a new user contribution (audio or text).
    Requires valid Auth0 JWT token.
    """
    new_contrib = Contribution(
        id=f"cnt_{uuid.uuid4().hex[:12]}",
        user_id=user.get("sub"),
        event_id=contrib.event_id,
        type=contrib.type,
        perspective=contrib.perspective,
        s3_key=contrib.s3_key,
        notes=contrib.notes,
        status="pending_review"
    )
    
    db.add(new_contrib)
    await db.commit()
    await db.refresh(new_contrib)
    
    return new_contrib


@router.get("/users/me/history")
async def get_my_listening_history(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(verify_token)
):
    """Get listening history for authenticated user."""
    # Placeholder for history query
    return {"message": "History endpoint scaffolded", "user_id": user.get("sub")}
