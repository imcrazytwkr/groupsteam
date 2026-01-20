#!/usr/bin/env python3

import sys

from lib.name_provider import NameProvider
from lib.file_renamer import FileRenamer
from lib.args import parse_options


if __name__ == "__main__":
    options = parse_options(sys.argv[1:])

    name_provider = NameProvider(options.cache_path, options.overrides_path)
    file_renamer = FileRenamer(name_provider, exist_ok=options.ignore_existing)

    for path in options.paths:
        file_renamer.rename_recursively(path)

    name_provider.flush()
