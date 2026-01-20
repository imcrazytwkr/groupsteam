#!/usr/bin/env python3

from pathlib import Path
import sys

from lib.name_provider import NameProvider
from lib.file_renamer import FileRenamer
from lib.env import get_path


# XDG_CONFIG_HOME
config_dir = get_path("XDG_CONFIG_HOME", Path.home().joinpath(".config"))
overrides_path = config_dir.joinpath("steamapps.overrides.json")

# XDG_DATA_HOME
data_dir = get_path("XDG_DATA_HOME", Path.home().joinpath(".local", "share"))
cache_path = data_dir.joinpath("steamapps.map.json")

if __name__ == "__main__":
    name_provider = NameProvider(cache_path, overrides_path)
    file_renamer = FileRenamer(name_provider, exist_ok=False)
    file_renamer.rename_recursively(Path(sys.argv[1]).resolve(strict=True))
    name_provider.flush()
