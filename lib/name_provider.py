from pathlib import Path
from time import sleep
import json

from .http import fetch_json

STEAM_URL = "https://store.steampowered.com/api/appdetails/"


class NameProvider:

    cache_path: Path

    cache: dict[int, str]

    overrides: dict[int, str]

    pending = False

    def __init__(
        self: NameProvider,
        cache_path: Path,
        overrides_path: Path,
    ) -> None:
        self.cache_path = cache_path

        self.cache = read_dict(self.cache_path)

        self.overrides = read_dict(overrides_path)

    def get_name(self: NameProvider, app_id: int) -> str:
        if app_id in self.overrides:
            return self.overrides[app_id]

        if app_id in self.cache:
            return self.cache[app_id]

        app_name = self.fetch_name(app_id)
        self.cache[app_id] = app_name
        return app_name

    def fetch_name(self: NameProvider, app_id: int) -> str:
        if self.pending:
            sleep(1)
        else:
            self.pending = True

        payload = fetch_json(f"{STEAM_URL}?appids={app_id}")
        assert isinstance(payload, dict)

        key = str(app_id)
        assert key in payload

        data = payload[key]
        assert data.get("success", False)
        assert "data" in data

        app_data = data["data"]
        assert app_data.get("type", "fubar").lower() == "game"
        assert app_data.get("steam_appid", -1) == app_id

        app_name = app_data.get("name", "").strip()
        assert len(app_name) > 0

        return app_name

    def flush(self: NameProvider) -> None:
        if self.pending:
            write_dict(self.cache_path, self.cache)


# @api: private
def read_dict(filepath: Path) -> dict[int, str]:
    if not filepath.is_file():
        return {}

    with open(filepath) as infile:
        payload = json.load(infile)

    if not payload:
        return {}

    return {int(app_id): app_name for app_id, app_name in payload.items()}


# @api: private
def write_dict(filepath: Path, data: dict[int, str]) -> None:
    if not data:
        return

    with open(filepath, "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False, allow_nan=False)
