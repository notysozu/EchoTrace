from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import events, audio, users
from core.database import engine, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EchoTrace API",
    description="Backend audio delivery and knowledge graph for EchoTrace",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://echotrace.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(events.router, prefix="/v1", tags=["Events"])
app.include_router(audio.router, prefix="/v1", tags=["Audio"])
app.include_router(users.router, prefix="/v1", tags=["Users"])


@app.on_event("startup")
async def on_startup():
    # Only suitable for simple hackathon init, normally use Alembic
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    logger.info("EchoTrace API starting up")


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
