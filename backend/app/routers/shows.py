from fastapi import APIRouter, Depends, Query
from redis.asyncio import Redis

from app.redis_client import get_redis
from app.schemas.show import ShowCard, ShowDetail
from app.services.cache import CACHE_TTL, discover_key, get_or_set
from app.services.providers import PLATFORM_TO_PROVIDER_ID, normalize_providers
from app.services.soundtrack import resolve_soundtrack
from app.services.tmdb import TMDBClient, normalize_show

router = APIRouter(prefix="/shows", tags=["shows"])
client = TMDBClient()


@router.get("", response_model=list[ShowCard])
async def get_shows(
    platforms: list[str] = Query(default=[]),
    languages: list[str] = Query(default=["en"]),
    availability: str = "flatrate",
    page: int = 1,
    page_size: int = 20,
    redis: Redis = Depends(get_redis),
):
    provider_ids = [PLATFORM_TO_PROVIDER_ID[p] for p in platforms if p in PLATFORM_TO_PROVIDER_ID]
    filters = {"provider_ids": provider_ids, "languages": languages or ["en"], "page": page, "page_size": page_size}
    discover = await get_or_set(redis, discover_key(filters), CACHE_TTL["discover"], lambda: client.discover_shows(filters))

    cards = []
    for show in discover.get("results", [])[:page_size]:
        providers = await get_or_set(redis, f"tmdb:providers:{show['id']}:US", CACHE_TTL["providers"], lambda sid=show["id"]: client.get_watch_providers(sid))
        normalized = [p for p in normalize_providers(providers) if availability == "all" or p["type"] == availability]
        if platforms and not any(p["name"] in platforms for p in normalized):
            continue
        cards.append({
            "tmdb_id": show["id"],
            "title": show.get("name"),
            "poster_path": show.get("poster_path"),
            "backdrop_path": show.get("backdrop_path"),
            "overview": show.get("overview"),
            "original_language": show.get("original_language"),
            "vote_average": show.get("vote_average"),
            "first_air_date": show.get("first_air_date"),
            "platforms": normalized,
        })
    return cards


@router.get("/{tmdb_id}", response_model=ShowDetail)
async def get_show_detail(tmdb_id: int, redis: Redis = Depends(get_redis)):
    details = await get_or_set(redis, f"tmdb:details:{tmdb_id}", CACHE_TTL["details"], lambda: client.get_show_details(tmdb_id))
    providers = await get_or_set(redis, f"tmdb:providers:{tmdb_id}:US", CACHE_TTL["providers"], lambda: client.get_watch_providers(tmdb_id))
    credits = await get_or_set(redis, f"tmdb:credits:{tmdb_id}", CACHE_TTL["credits"], lambda: client.get_cast_and_crew(tmdb_id))
    trailer_key = await get_or_set(redis, f"tmdb:trailer:{tmdb_id}", CACHE_TTL["trailer"], lambda: client.get_trailer_key(tmdb_id))
    keywords = await client.get_keywords(tmdb_id)
    soundtrack = await get_or_set(redis, f"tmdb:soundtrack:{tmdb_id}", CACHE_TTL["soundtrack"], lambda: resolve_soundtrack(tmdb_id, keywords))
    return normalize_show(details, providers, credits, trailer_key, soundtrack)
