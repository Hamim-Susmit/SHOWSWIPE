from pydantic import BaseModel


class MemberCreate(BaseModel):
    name: str


class MemberOut(BaseModel):
    id: str
    name: str
    vote_count: int = 0
