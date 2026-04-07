import json

from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.vote import Vote, VoteType


async def compute_match(show_id, circle_id, db: AsyncSession, redis: Redis):
    cache_key = f"match:{circle_id}:{show_id}"
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    votes_result = await db.execute(select(Vote, User.name).join(User, Vote.user_id == User.id).where(Vote.show_id == show_id, Vote.circle_id == circle_id))
    rows = votes_result.all()
    members_result = await db.execute(select(func.count(User.id)).where(User.circle_id == circle_id))
    member_count = members_result.scalar_one() or 1

    likers = [name for vote, name in rows if vote.vote_type in {VoteType.like, VoteType.super}]
    match_pct = int((len(likers) / member_count) * 100)
    payload = {"is_match": match_pct >= 50, "match_pct": match_pct, "likers": likers}
    await redis.setex(cache_key, 300, json.dumps(payload))
    return payload
