from urllib.parse import quote_plus

SHOW_SOUNDTRACKS = {
    1396: [
        {"title": "Baby Blue", "artist": "Badfinger", "singer": "Tom Evans"},
        {"title": "Crystal Blue Persuasion", "artist": "Tommy James", "singer": "Tommy James"},
    ],
    66732: [
        {"title": "Running Up That Hill", "artist": "Kate Bush", "singer": "Kate Bush"},
    ],
    93405: [
        {"title": "Way Back Then", "artist": "Jung Jae-il", "singer": "Jung Jae-il"},
    ],
}


def build_song_links(song: dict) -> dict:
    query = quote_plus(f"{song['title']} {song['artist']}")
    return {
        **song,
        "spotify_url": f"https://open.spotify.com/search/{query}",
        "youtube_url": f"https://www.youtube.com/results?search_query={query}",
    }


async def resolve_soundtrack(tmdb_id: int, keywords: dict | None = None) -> list[dict]:
    _ = keywords
    return [build_song_links(song) for song in SHOW_SOUNDTRACKS.get(tmdb_id, [])]
