import uuid

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.show import Show
from app.models.user import User
from app.models.vote import Vote, VoteType
from app.redis_client import get_redis
from app.routers.ws import manager
from app.services.matcher import compute_match
from app.services.tmdb import TMDBClient

router = APIRouter(tags=["votes"])
client = TMDBClient()


@router.post("/votes")
async def submit_vote(payload: dict, db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    user = (await db.execute(select(User).where(User.id == payload["user_id"]))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    show = (await db.execute(select(Show).where(Show.tmdb_id == int(payload["show_id"])))).scalar_one_or_none()
    if not show:
        details = await client.get_show_details(int(payload["show_id"]))
        show = Show(
            tmdb_id=details["id"],
            title=details.get("name", "Unknown"),
            original_language=details.get("original_language", "en"),
            poster_path=details.get("poster_path"),
            backdrop_path=details.get("backdrop_path"),
            overview=details.get("overview"),
            tagline=details.get("tagline"),
            vote_average=details.get("vote_average", 0),
            vote_count=details.get("vote_count", 0),
            seasons=details.get("number_of_seasons", 1),
            genres=[g["name"] for g in details.get("genres", [])],
        )
        db.add(show)
        await db.flush()

    vote = (await db.execute(select(Vote).where(Vote.show_id == show.id, Vote.user_id == user.id))).scalar_one_or_none()
    vote_type = VoteType(payload["vote_type"])
    if vote:
        vote.vote_type = vote_type
    else:
        db.add(Vote(show_id=show.id, user_id=user.id, circle_id=uuid.UUID(payload["circle_id"]), vote_type=vote_type))
    await db.commit()

    match = await compute_match(show.id, uuid.UUID(payload["circle_id"]), db, redis)
    if vote_type in {VoteType.like, VoteType.super}:
        await manager.broadcast(payload["circle_id"], {"event": "vote", "user": user.name, "show_title": show.title, "vote": vote_type.value})
    if match["is_match"] and vote_type in {VoteType.like, VoteType.super}:
        await manager.broadcast(payload["circle_id"], {"event": "match", "show_title": show.title, "match_pct": match["match_pct"], "likers": match["likers"]})

    return {"saved": True, "match": match["is_match"], "match_pct": match["match_pct"], "likers": match["likers"]}


@router.get("/matches/{circle_id}")
async def get_matches(circle_id: str, db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    circle_users = (await db.execute(select(User).where(User.circle_id == circle_id))).scalars().all()
    user_ids = [u.id for u in circle_users]
    vote_rows = (await db.execute(select(Vote).where(Vote.circle_id == circle_id, Vote.user_id.in_(user_ids)))).scalars().all()

    by_show: dict[uuid.UUID, list[Vote]] = {}
    for vote in vote_rows:
        by_show.setdefault(vote.show_id, []).append(vote)

    matches = []
    for show_id, votes in by_show.items():
        match = await compute_match(show_id, uuid.UUID(circle_id), db, redis)
        if match["is_match"]:
            show = (await db.execute(select(Show).where(Show.id == show_id))).scalar_one()
            matches.append({
                "tmdb_id": show.tmdb_id,
                "title": show.title,
                "poster_path": show.poster_path,
                "match_pct": match["match_pct"],
                "likers": match["likers"],
                "platforms": show.platforms or [],
            })
    return sorted(matches, key=lambda x: x["match_pct"], reverse=True)
