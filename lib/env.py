from pathlib import Path
import os


def get_path(env_name: str, fallback: Path) -> Path:
    value = os.getenv(env_name)
    if not value:
        return fallback.resolve(strict=True)

    dirpath = Path(value).resolve()
    dirpath.mkdir(exist_ok=True)
    return dirpath
