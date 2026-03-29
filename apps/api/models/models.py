from sqlalchemy import (
    Column, String, Integer, BigInteger, Boolean, Text, Float,
    ForeignKey, TIMESTAMP, ARRAY, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class Era(Base):
    __tablename__ = "eras"

    id = Column(String, primary_key=True)           # 'era_ancient'
    label = Column(String, nullable=False)           # 'Ancient World'
    start_year = Column(Integer)
    end_year = Column(Integer)
    description = Column(Text)
    color_hex = Column(String(7))                   # '#4A90D9'

    events = relationship("Event", back_populates="era")


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)          # negative = BCE
    description = Column(Text)
    era_id = Column(String, ForeignKey("eras.id"))
    capsule_type = Column(String)                   # snapshot|narrative|immersive
    topics = Column(ARRAY(String), default=[])
    thumbnail_url = Column(String)
    is_published = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    era = relationship("Era", back_populates="events")
    audio_files = relationship("AudioFile", back_populates="event", cascade="all, delete-orphan")
    perspectives = relationship("Perspective", back_populates="event", cascade="all, delete-orphan")
    sources = relationship("Source", back_populates="event", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_events_year", "year"),
        Index("idx_events_era", "era_id"),
        Index("idx_events_published", "is_published"),
    )


class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    perspective_type = Column(String, nullable=False)  # narrator|eyewitness|historian|opposition
    voice_id = Column(String)
    s3_key = Column(String, nullable=False)
    format = Column(String, default="mp3")
    duration_seconds = Column(Integer)
    file_size_bytes = Column(BigInteger)
    version = Column(Integer, default=1)
    transcript = Column(Text)
    is_active = Column(Boolean, default=True)
    generated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="audio_files")

    __table_args__ = (
        Index("idx_audio_event", "event_id"),
        Index("idx_audio_active", "is_active"),
    )


class Perspective(Base):
    __tablename__ = "perspectives"

    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    audio_file_id = Column(String, ForeignKey("audio_files.id"))
    perspective_type = Column(String, nullable=False)
    summary = Column(Text)
    script_text = Column(Text)
    fact_tags = Column(JSONB, default=[])
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="perspectives")


class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"))
    source_type = Column(String)                   # wikipedia|book|archive
    url = Column(String)
    title = Column(String)
    author = Column(String)
    accessed_at = Column(TIMESTAMP(timezone=True))

    event = relationship("Event", back_populates="sources")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)          # Auth0 sub
    email = Column(String, unique=True, nullable=False)
    display_name = Column(String)
    avatar_url = Column(String)
    role = Column(String, default="listener")      # listener|contributor|admin
    preferences = Column(JSONB, default={})
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class ListeningHistory(Base):
    __tablename__ = "listening_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    audio_file_id = Column(String, ForeignKey("audio_files.id"))
    listened_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    position_seconds = Column(Integer, default=0)
    completed = Column(Boolean, default=False)

    __table_args__ = (
        Index("idx_history_user", "user_id", "listened_at"),
    )


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    audio_file_id = Column(String, ForeignKey("audio_files.id"))
    timestamp_sec = Column(Integer)
    note = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    items = relationship("PlaylistItem", back_populates="playlist", cascade="all, delete-orphan",
                         order_by="PlaylistItem.position")


class PlaylistItem(Base):
    __tablename__ = "playlist_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    playlist_id = Column(String, ForeignKey("playlists.id", ondelete="CASCADE"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    position = Column(Integer, nullable=False)

    playlist = relationship("Playlist", back_populates="items")
    __table_args__ = (
        UniqueConstraint("playlist_id", "position"),
    )


class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    event_id = Column(String, ForeignKey("events.id"))
    type = Column(String)                          # audio|text|correction
    perspective = Column(String)
    s3_key = Column(String)
    notes = Column(Text)
    status = Column(String, default="pending_review")  # pending_review|approved|rejected
    reviewed_by = Column(String, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class EventRelation(Base):
    __tablename__ = "event_relations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    from_event_id = Column(String, ForeignKey("events.id"), nullable=False)
    to_event_id = Column(String, ForeignKey("events.id"), nullable=False)
    relation_type = Column(String, nullable=False)  # sequence|cause|influence|contrast
    weight = Column(Float, default=1.0)

    __table_args__ = (
        UniqueConstraint("from_event_id", "to_event_id", "relation_type"),
        Index("idx_relations_from", "from_event_id"),
        Index("idx_relations_to", "to_event_id"),
    )
