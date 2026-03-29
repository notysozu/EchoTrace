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

<!-- AUDIT: Missing standard sections: Contributing, License -->
<!-- AUDIT: No technical documentation on the mono-repo structure -->
