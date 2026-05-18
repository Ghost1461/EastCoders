import json
from pathlib import Path

from fastapi import HTTPException


def get_source_user_id_from_api_key(platform_key: str, api_key: str) -> str:
    api_keys_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "mock_sources"
        / "api_keys.json"
    )

    if not api_keys_path.exists():
        raise HTTPException(
            status_code=404,
            detail="API key dosyası bulunamadı."
        )

    with open(api_keys_path, "r", encoding="utf-8") as file:
        api_keys = json.load(file)

    for item in api_keys:
        if (
            item.get("platform", "").lower() == platform_key.lower()
            and item.get("api_key") == api_key
        ):
            return item["user_id"]

    raise HTTPException(
        status_code=401,
        detail="Geçersiz API key veya platform"
    )