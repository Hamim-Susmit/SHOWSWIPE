PROVIDER_MAP = {
    8: {"name": "Netflix", "color": "#e50914"},
    9: {"name": "Prime Video", "color": "#00a8e0"},
    15: {"name": "Hulu", "color": "#1ce783"},
    337: {"name": "Disney+", "color": "#113ccf"},
    350: {"name": "Apple TV+", "color": "#a0a0a0"},
    384: {"name": "HBO Max", "color": "#a855f7"},
    386: {"name": "Peacock", "color": "#000000"},
    73: {"name": "Tubi", "color": "#ff6b35"},
}

PLATFORM_TO_PROVIDER_ID = {v["name"]: k for k, v in PROVIDER_MAP.items()}


def normalize_providers(providers_response: dict, region: str = "US") -> list[dict]:
    result = providers_response.get("results", {}).get(region, {})
    platforms: list[dict] = []
    for p in result.get("flatrate", []):
        if p["provider_id"] in PROVIDER_MAP:
            platforms.append({**PROVIDER_MAP[p["provider_id"]], "type": "flatrate", "price": None})
    for p in result.get("rent", []):
        if p["provider_id"] in PROVIDER_MAP:
            platforms.append({**PROVIDER_MAP[p["provider_id"]], "type": "rent", "price": 3.99})
    for p in result.get("ads", []):
        if p["provider_id"] in PROVIDER_MAP:
            platforms.append({**PROVIDER_MAP[p["provider_id"]], "type": "ads", "price": None})
    for p in result.get("buy", []):
        if p["provider_id"] in PROVIDER_MAP:
            platforms.append({**PROVIDER_MAP[p["provider_id"]], "type": "buy", "price": 14.99})
    return platforms
