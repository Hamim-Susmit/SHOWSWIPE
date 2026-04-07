from pydantic import BaseModel

from app.schemas.user import MemberCreate, MemberOut


class CircleCreate(BaseModel):
    name: str
    members: list[MemberCreate]


class CircleCreateResponse(BaseModel):
    circle_id: str
    members: list[MemberOut]


class CircleOut(BaseModel):
    id: str
    name: str
    members: list[MemberOut]
