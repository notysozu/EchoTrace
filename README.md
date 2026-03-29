# EchoTrace

[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-20-339933?style=flat-square&logo=node.js)](https://nodejs.org/)

**Audio-first historical knowledge platform for immersive time-traveling through sound.**

## Overview

EchoTrace is an immersive audio archive that transforms historical milestones into multi-perspective, spatial soundscapes. By leveraging generative AI to script and synthesize authentic period-specific voices, it allows users to experience "the room where it happened" through the ears of those who lived it. It bridges the gap between static textbooks and cinematic storytelling, providing a lean-back discovery experience for history enthusiasts and students alike.

## Key Features

- **Infinite Scrolling Timeline**: Explore historical milestones chronologically across thousands of years with a seamless, high-density interface.
- **Multi-Perspective Storytelling**: Experience events through four distinct lenses—Narrator, Eyewitness, Historian, and Opposition voices.
- **Cinematic Voice Synthesis**: Premium AI-generated audio powered by ElevenLabs, capturing the gravity and tone of historical eras.
- **Immersive Soundscapes**: Dynamically mixed ambient background layers using FFmpeg to create a rich, spatial presence.
- **Persistent Global Player**: A floating audio engine that maintains playback and state across entire site transitions.
- **Smart Discovery**: AI-driven categorization by era, topic, and historical significance for tailored knowledge exploration.

## Prerequisites

Before setting up EchoTrace, ensure you have the following installed:

- **Node.js** (v20.x or higher) — [Download](https://nodejs.org/)
- **Python** (v3.12.x or higher) — [Download](https://www.python.org/)
- **Docker & Docker Compose** — [Get Docker](https://docs.docker.com/get-docker/)
- **FFmpeg** — Required for audio multiplexing. [Install Guide](https://ffmpeg.org/download.html)
- **Redis** — Used for job queues and caching.
- **PostgreSQL** — Primary relational data store.

## Installation

Follow these steps to get your EchoTrace development environment running:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/notysozu/EchoTrace.git
   cd EchoTrace
   ```

2. **Configure Environment Variables:**
   Copy the example environment file and fill in your API keys (OpenAI, ElevenLabs, AWS).
   ```bash
   cp .env.example .env
   ```

3. **Start Infrastructure (Docker):**
   Launch PostgreSQL, Redis, and the FastAPI backend.
   ```bash
   docker-compose up -d
   ```

4. **Install Dependencies:**
   ```bash
   # Install root and workspace dependencies
   npm install
   
   # Install Python dependencies for the API
   cd apps/api && pip install -r requirements.txt && cd ../..
   ```

5. **Run Database Migrations:**
   ```bash
   cd apps/api
   alembic upgrade head
   cd ../..
   ```

6. **Verify Installation:**
   Run the dev stack and ensure all services boot without errors.
   ```bash
   npm run dev
   ```

## Usage

### 🌐 Explore the Timeline
Open [http://localhost:3000](http://localhost:3000) in your browser to explore the interactive timeline.
- **Scroll** through historical eras.
- **Click** on an event to open the perspective switcher.
- **Listen** to immersive audio narratives while navigating the site.

### 🤖 Trigger AI Generation
You can generate new immersive content for any historical event via the internal API:

```bash
curl -X POST http://localhost:8001/v1/events/generate \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt-apollo",
    "event_name": "Apollo 11",
    "summary_text": "First humans on the moon.",
    "era_label": "Space Race"
  }'
```

The worker service will automatically:
1. Write 4 distinct scripts using OpenAI.
2. Synthesize audio with ElevenLabs.
3. Mix soundscapes via FFmpeg.
4. Upload to S3 and notify the frontend.

## Configuration

EchoTrace uses environment variables for secure API integration and service routing.

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://...` | Connection URI for the PostgreSQL instance. |
| `REDIS_URL` | `redis://localhost:6379` | Connection URI for the Redis broker. |
| `OPENAI_API_KEY` | `required` | Key for automated script generation via GPT-4o. |
| `ELEVENLABS_API_KEY` | `required` | Key for cinematic voice synthesis. |
| `S3_BUCKET_NAME` | `echotrace-audio` | Destination bucket for final processed audio assets. |
| `AWS_REGION` | `us-east-1` | AWS region for S3 bucket operations. |
| `WORKER_PORT` | `3001` | The internal API port for the Node.js production worker. |

## Tech Stack

### 📱 Frontend (Web)
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + Framer Motion
- **State**: Zustand (Global player) + React Query (Data)
- **Audio**: Howler.js

### ⚙️ Backend (API)
- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL (SQLAlchemy + Alembic)
- **Validation**: Pydantic v2
- **Caching**: Redis

### 🤖 AI Worker
- **Runtime**: Node.js (TypeScript)
- **Queues**: BullMQ + Redis
- **Models**: OpenAI GPT-4o
- **Voices**: ElevenLabs API
- **Processing**: FFmpeg

## Project Structure

```text
EchoTrace/
├── apps/
│   ├── web/          # Next.js 14 Frontend (React, Zustand, Howler.js)
│   ├── api/          # FastAPI Backend (Python, SQLAlchemy, Alembic)
│   └── worker/       # Node.js AI Pipeline (BullMQ, OpenAI, ElevenLabs)
├── docker-compose.yml # Infrastructure (Postgres, Redis, Backend orchestration)
├── package.json      # Monorepo workspace configuration
└── .env.example      # Global environment template
```

## Roadmap

EchoTrace is currently in active development.

- [x] **Phase 1**: Core Frontend & Timeline UI.
- [x] **Phase 2**: Backend API & Database Schema.
- [x] **Phase 3**: AI Pipeline (OpenAI + ElevenLabs + FFmpeg).
- [ ] **Auth**: User profiles and persistent listening history.
- [ ] **Discovery**: Full-text search and AI-driven era recommendations.
- [ ] **Streaming**: Adaptive Bitrate Streaming (HLS) for optimized mobile playback.

## Contributing

We welcome contributions to EchoTrace! To get started:

1. **Fork** the repository and create your branch from `main`.
2. **Open an issue** to discuss the change you wish to make.
3. Ensure your code follows the existing style and all services boot correctly.
4. Submit a **Pull Request** with a detailed description of your changes.

Check out our [GitHub Issues](https://github.com/notysozu/EchoTrace/issues) for "good first issue" labels.

<!-- AUDIT: License -->
