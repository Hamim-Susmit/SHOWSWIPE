from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import Circle, User
from app.models.vote import Vote
from app.schemas.circle import CircleCreate, CircleCreateResponse, CircleOut

router = APIRouter(prefix="/circle", tags=["circle"])


@router.post("", response_model=CircleCreateResponse)
async def create_circle(payload: CircleCreate, db: AsyncSession = Depends(get_db)):
    circle = Circle(name=payload.name)
    db.add(circle)
    await db.flush()

    members = [User(name=member.name, circle_id=circle.id) for member in payload.members]
    db.add_all(members)
    await db.commit()
    await db.refresh(circle)
    return {"circle_id": str(circle.id), "members": [{"id": str(m.id), "name": m.name, "vote_count": 0} for m in members]}


@router.get("/{circle_id}", response_model=CircleOut)
async def get_circle(circle_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circle).where(Circle.id == circle_id))
    circle = result.scalar_one_or_none()
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    users = (await db.execute(select(User).where(User.circle_id == circle.id))).scalars().all()
    members = []
    for user in users:
        votes = await db.execute(select(func.count(Vote.id)).where(Vote.user_id == user.id))
        members.append({"id": str(user.id), "name": user.name, "vote_count": votes.scalar_one()})

    return {"id": str(circle.id), "name": circle.name, "members": members}
