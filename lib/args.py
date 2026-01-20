from argparse import ArgumentParser
from typing import NamedTuple
from pathlib import Path

from .env import get_path

# XDG_CONFIG_HOME
CONFIG_DIR = get_path("XDG_CONFIG_HOME", Path.home().joinpath(".config"))
DEFAULT_OVERRIDES_PATH = CONFIG_DIR.joinpath("steamapps.overrides.json")

# XDG_DATA_HOME
DATA_DIR = get_path("XDG_DATA_HOME", Path.home().joinpath(".local", "share"))
DEFAULT_CACHE_PATH = DATA_DIR.joinpath("steamapps.map.json")

# @visibility: private
parser = ArgumentParser(prog="groupsteam", allow_abbrev=False)

parser.add_argument(
    "-c",
    "--cache",
    "--cache-file",
    dest="cache_file",
    type=str,
    metavar="FILE",
    help='set the cache file to [FILE] isntead of "$XDG_DATA_HOME/steamapps.map.json"',
)

parser.add_argument(
    "-o",
    "--overrdes",
    "--overrides-file",
    dest="overrides_file",
    type=str,
    metavar="FILE",
    help='set the overrides file to [FILE] isntead of "$XDG_CONFIG_HOME/steamapps.map.json"',
)

parser.add_argument(
    "-i",
    "--ignore",
    "--ignore-existing",
    dest="ignore_existing",
    action="store_true",
    help="do not throw error if target file already exists, just do not rename",
)

parser.add_argument(
    "paths",
    nargs="+",
    metavar="PATH",
    help="paths to files and directories to group",
)


class Options(NamedTuple):
    cache_path: Path
    overrides_path: Path
    paths: list[Path]
    ignore_existing: bool


# @visibility: private
def normalize_to_path(raw: Union[str, Path, None], default: Path) -> Path:
    if raw is None:
        return default

    if isinstance(raw, Path):
        return Path.resolve()

    assert isinstance(raw, str)
    if len(raw) == 0:
        return default

    return normalize_to_path(Path(raw), default)


def parse_options(args: list[str]) -> Options:
    parsed = parser.parse_args(args)

    cache_path = normalize_to_path(parsed.cache_file, DEFAULT_CACHE_PATH)

    return Options(
        normalize_to_path(parsed.cache_file, DEFAULT_CACHE_PATH),
        normalize_to_path(parsed.overrides_file, DEFAULT_OVERRIDES_PATH),
        [Path(path).resolve(strict=True) for path in parsed.paths],
        bool(parsed.ignore_existing),
    )


__all__ = ["Options", "parse_options"]

assert __name__ != "__main__", "Do no evil"
