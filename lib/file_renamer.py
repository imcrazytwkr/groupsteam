from pathlib import Path
import logging
import re

from .name_provider import NameProvider

SCREENCAP_RE = re.compile(
    r"^(\d+)_(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(?:_\d+)?.(jpe?g|png)$",
    re.IGNORECASE,
)

# @api: private
logger = logging.getLogger(__name__)


class FileRenamer:
    name_provider: NameProvider

    exist_ok: bool

    def __init__(
        self: FileRenamer, name_provider: NameProvider, exist_ok: bool = False
    ) -> None:
        self.name_provider = name_provider
        self.exist_ok = exist_ok

    def rename_recursively(self: FileRenamer, path: Path):
        if path.is_file():
            self.rename_file(path)
            return

        assert path.is_dir()
        for directory, _, filenames in path.walk():
            assert isinstance(directory, Path)
            if not filenames:
                continue

            dirpath = directory.resolve(strict=True)
            for filename in filenames:
                self.rename_file(dirpath.joinpath(filename))

    def rename_file(self: FileRenamer, source: Path) -> None:
        match = SCREENCAP_RE.match(source.name)
        if match is None:
            return

        # No reason to check anything if we don't care about the file
        assert source.is_file()

        groups = list(match.groups())
        assert len(groups) == 8

        app_id = int(groups[0])
        app_name = self.name_provider.get_name(app_id)

        extname = groups[7].lower()
        if extname == "jpeg":
            extname = "jpg"

        # Expected output: "MiSide - 2026-01-19 at 22.07.15.jpg"
        target_name = (
            app_name
            + " - "
            + "-".join(groups[1:4])
            + " at "
            + ".".join(groups[4:7])
            + "."
            + extname
        )

        target_dir = source.parent.with_name(app_name)
        target_dir.mkdir(mode=source.parent.stat().st_mode, exist_ok=True)

        target = target_dir.joinpath(target_name)

        if not target.exists():
            source.rename(target)
            return

        if source == target:
            # Already properly renamed
            return

        if source.samefile(target):
            source.unlink()
            return

        msg = f"Target file {target} already exists"
        if self.exist_ok:
            logger.warning(msg)
        else:
            raise ValueError(msg)
