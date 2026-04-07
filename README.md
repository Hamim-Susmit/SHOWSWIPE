# ShowSwipe

A Tinder-style TV discovery app where your Binge Circle swipes together and surfaces shared matches.

![Screenshot placeholder](./docs/screenshot-placeholder.png)

## Prerequisites
- Node 20
- Python 3.11
- Docker + Docker Compose

## Quick start
```bash
git clone <your-repo-url>
cd showswipe
cp .env.example .env
# Add your TMDB_API_KEY to .env
docker compose up
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# API docs: http://localhost:8000/docs
```

## Architecture overview
ShowSwipe uses a React + Vite frontend with Zustand state, and a FastAPI backend with async SQLAlchemy, Redis caching, and WebSocket events. The implementation follows the phased plan in the build prompt: infrastructure, backend core/models/services/routers, frontend swipe experience, real-time events, and polish.

## TMDB API key
Register for a TMDB API key at: https://www.themoviedb.org/settings/api

## Feature roadmap
- Replace soundtrack seed data with MusicBrainz integration
- Add invite links and lightweight auth
- Improve recommendation ranking with collaborative filtering
- Add actor drill-down and show detail deep links
- Add production deployment manifests
