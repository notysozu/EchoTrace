from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class EraResponse(BaseModel):
    id: str
    label: str
    start_year: Optional[int]
    end_year: Optional[int]
    color_hex: Optional[str]

    class Config:
        from_attributes = True


class EventListItem(BaseModel):
    id: str
    title: str
    year: int
    capsule_type: Optional[str]
    topics: Optional[List[str]]
    thumbnail_url: Optional[str]
    era: Optional[EraResponse]
    perspectives_count: int = 0
    audio_preview_url: Optional[str]
    duration_seconds: Optional[int]

    class Config:
        from_attributes = True


class EventDetail(BaseModel):
    id: str
    title: str
    year: int
    description: Optional[str]
    capsule_type: Optional[str]
    topics: Optional[List[str]]
    thumbnail_url: Optional[str]
    era: Optional[EraResponse]
    related_event_ids: List[str] = []

    class Config:
        from_attributes = True


class AudioFileResponse(BaseModel):
    id: str
    perspective_type: str
    voice_id: Optional[str]
    duration_seconds: Optional[int]
    format: str
    presigned_url: str
    transcript: Optional[str]

    class Config:
        from_attributes = True


class PerspectiveResponse(BaseModel):
    id: str
    perspective_type: str
    audio_file_id: Optional[str]
    summary: Optional[str]
    fact_tags: Optional[Any]

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    data: List[Any]
    next_cursor: Optional[str]
    total: int


class ContributionCreate(BaseModel):
    event_id: str
    type: str           # audio|text|correction
    perspective: Optional[str]
    s3_key: Optional[str]
    notes: Optional[str]


class ContributionResponse(BaseModel):
    id: str
    event_id: str
    type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserHistoryCreate(BaseModel):
    event_id: str
    audio_file_id: Optional[str]
    position_seconds: int = 0
    completed: bool = False


class BookmarkCreate(BaseModel):
    event_id: str
    audio_file_id: Optional[str]
    timestamp_sec: Optional[int]
    note: Optional[str]


class EventRelationResponse(BaseModel):
    id: str
    title: str
    relation_type: str
    year: int
