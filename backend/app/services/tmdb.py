from typing import Any

import httpx

from app.config import settings
from app.services.providers import normalize_providers


class TMDBClient:
    def __init__(self) -> None:
        self.base_url = settings.tmdb_base_url
        self.api_key = settings.tmdb_api_key

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        payload = {"api_key": self.api_key, **(params or {})}
        async with httpx.AsyncClient(base_url=self.base_url, timeout=20) as client:
            response = await client.get(path, params=payload)
            response.raise_for_status()
            return response.json()

    async def discover_shows(self, filters: dict[str, Any]) -> dict:
        params = {
            "with_watch_providers": ",".join(map(str, filters.get("provider_ids", []))),
            "watch_region": filters.get("region", "US"),
            "with_original_language": "|".join(filters.get("languages", ["en"])),
            "sort_by": "popularity.desc",
            "page": filters.get("page", 1),
        }
        if filters.get("genres"):
            params["with_genres"] = filters["genres"]
        return await self._get("/discover/tv", params)

    async def get_show_details(self, tmdb_id: int) -> dict:
        return await self._get(f"/tv/{tmdb_id}")

    async def get_watch_providers(self, tmdb_id: int, region: str = "US") -> dict:
        _ = region
        return await self._get(f"/tv/{tmdb_id}/watch/providers")

    async def get_cast_and_crew(self, tmdb_id: int) -> dict:
        return await self._get(f"/tv/{tmdb_id}/credits")

    async def get_trailer_key(self, tmdb_id: int) -> str | None:
        data = await self._get(f"/tv/{tmdb_id}/videos")
        videos = data.get("results", [])
        for wanted in ("Trailer", "Teaser"):
            for item in videos:
                if item.get("type") == wanted and item.get("site") == "YouTube":
                    return item.get("key")
        return None

    async def get_person_image(self, person_id: int) -> str | None:
        data = await self._get(f"/person/{person_id}/images")
        first = (data.get("profiles") or [{}])[0]
        path = first.get("file_path")
        return f"{settings.tmdb_image_base}{path}" if path else None

    async def get_keywords(self, tmdb_id: int) -> dict:
        return await self._get(f"/tv/{tmdb_id}/keywords")


def normalize_cast(cast: list[dict]) -> list[dict]:
    normalized = []
    for person in cast[:8]:
        path = person.get("profile_path")
        normalized.append(
            {
                "id": person.get("id"),
                "name": person.get("name", "Unknown"),
                "character": person.get("character"),
                "profile_url": f"{settings.tmdb_image_base}{path}" if path else None,
            }
        )
    return normalized


def normalize_crew(crew: list[dict]) -> list[dict]:
    allowed = {"Creator", "Director", "Executive Producer", "Showrunner", "Composer", "Writer"}
    return [{"name": c.get("name", "Unknown"), "job": c.get("job", "")}
            for c in crew if c.get("job") in allowed]


def normalize_show(details: dict, providers: dict, credits: dict, trailer_key: str | None, soundtrack: list[dict]) -> dict:
    return {
        "tmdb_id": details["id"],
        "title": details.get("name", "Unknown"),
        "tagline": details.get("tagline", ""),
        "overview": details.get("overview", ""),
        "poster_url": f"{settings.tmdb_image_base}{details['poster_path']}" if details.get("poster_path") else None,
        "backdrop_url": f"{settings.tmdb_image_base}{details['backdrop_path']}" if details.get("backdrop_path") else None,
        "rating": round(details.get("vote_average", 0), 1),
        "vote_count": details.get("vote_count", 0),
        "seasons": details.get("number_of_seasons", 1),
        "year": details.get("first_air_date", "")[:4],
        "original_language": details.get("original_language", "en"),
        "genres": [g["name"] for g in details.get("genres", [])],
        "platforms": normalize_providers(providers),
        "cast": normalize_cast(credits.get("cast", [])),
        "crew": normalize_crew(credits.get("crew", [])),
        "trailer_key": trailer_key,
        "soundtrack": soundtrack,
    }
