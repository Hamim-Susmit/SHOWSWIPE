from pydantic import BaseModel


class ProviderOut(BaseModel):
    name: str
    color: str
    type: str
    price: float | None = None


class CastOut(BaseModel):
    id: int
    name: str
    character: str | None = None
    profile_url: str | None = None


class CrewOut(BaseModel):
    name: str
    job: str


class SoundtrackOut(BaseModel):
    title: str
    artist: str
    singer: str | None = None
    spotify_url: str
    youtube_url: str


class ShowCard(BaseModel):
    tmdb_id: int
    title: str
    poster_path: str | None = None
    backdrop_path: str | None = None
    overview: str | None = None
    original_language: str | None = None
    vote_average: float | None = None
    first_air_date: str | None = None
    platforms: list[ProviderOut] = []


class ShowDetail(BaseModel):
    tmdb_id: int
    title: str
    tagline: str = ""
    overview: str = ""
    poster_url: str | None = None
    backdrop_url: str | None = None
    rating: float = 0
    vote_count: int = 0
    seasons: int = 1
    year: str = ""
    original_language: str = "en"
    genres: list[str] = []
    platforms: list[ProviderOut] = []
    cast: list[CastOut] = []
    crew: list[CrewOut] = []
    trailer_key: str | None = None
    soundtrack: list[SoundtrackOut] = []
