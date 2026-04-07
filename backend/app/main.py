from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.redis_client import redis_client
from app.routers import circle, shows, votes, ws

app = FastAPI(title="ShowSwipe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shows.router, prefix="/api")
app.include_router(circle.router, prefix="/api")
app.include_router(votes.router, prefix="/api")
app.include_router(ws.router, prefix="/ws")


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await redis_client.ping()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
