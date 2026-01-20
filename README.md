[![license](https://img.shields.io/github/license/imcrazytwkr/groupsteam)](LICENSE)

A simple tool to group Steam screenshots into directories. It is intended to be used with
the files resulting from Steam's "Save an external copy of my screenshots" function.

As of January 2026, it will not work with screenshots exported from Steam manually as
they do not contain steam app id or steam app name prefix within the filename so
distinguishing between screenshots for different games is practically impossble for
those.

## Getting started

These instructions will get you a copy of the project up and running on your local machine
for development and testing purposes. Multi-user installation instructions useful mostly
to package maintainers are also provided in a later section.

### Prerequisites

Requires Python 3.4 due to the way [Pathlib](https://docs.python.org/3/library/pathlib.html)
is used. Python 3.12+ is recommended. Tested on Python versions 3.12-3.14. No external
dependencies are required.

### Linking (local installation)

1. Clone the repo: `git clone 'https://github.com/imcrazytwkr/groupsteam'`
2. Link the main binary:
    - Use make to link it to "$prefix/bin" directory: `make prefix="$HOME/.local" link`
    - Link manually wherever you want: `ln -s -T "$PWD/groupsteam.py" '/some/directory/groupsteam'`

### Global/multi-user installation

This section is mostly providing recommendations compared to strict rules.
Ideally this section is here for package maintainers who want to build
packages for their distros.

1. Clone the repo: `git clone 'https://github.com/imcrazytwkr/groupsteam'`
2. Copy its contents to `/opt/groupsteam`:

```sh
mkdir /opt/groupsteam
cp -r * /opt/groupsteam
```

3. Link the main binary: `ln -s -T '/opt/groupsteam/groupsteam.py' '/usr/bin/groupsteam'`

## How to use

Helf is available using the `groupsteam -h` flag. The rest of this section will be devoted
to explaining how the grouping works.

### Grouping algorithm

The app takes your paths. If you pass it directories, it will scan them recursively for
images, file-paths are taken as-is. When the list is collected, `groupsteam` will scan
every filename for match of steam's raw screenshot naming, extract Steam app id from it,
fetch game name for this ID (either from cache or from Steam Store API), then go to the
screnshot file's parent directory and look for a directory named after the game name. If
it exists, the file will be moved into it under a human-readable format. If it does not
exist, it will be created, and then file will be moved there.

### Example of the app's operation

Let's assume you have a `$HOME/Pictures/Game Captures` directory that contains a 
`Steam Inbox` directory and directories named after your games:

- `MiSide`
- `Steam Inbox`

Let us also assume that the `Steam Inbox` directory has the following files in it:

- `2752180_20260120184917_1.png` (screenshot from "No Sleep for Kaname Date")
- `2527500_20260120133742_1.png` (screenshot from "MiSide")

Let us also assume you have a mapping for "No Sleep for Kaname Date" in your
overrides file (refer to **Configuration** section):

```json
{
  "2752180": "No Sleep for Kaname Date"
}
```

When the app is called as `groupsteam 'Steam Inbox'` from the game capture directory,
it will:

1. Rename `2527500_20260120133742_1.png` into `MiSide - 2026-01-20 at 13.37.42.png` and
   move it to `Game Captures/MiSide` directory that is already present.
2. Rename `2752180_20260120184917_1.png` into
   `No Sleep for Kaname Date - 2026-01-20 at 18.48.17.png` because it found an override
   for it (original name is `No Sleep For Kaname Date - From AI: THE SOMNIUM FILES`).
3. Created the `Game Captures/No Sleep for Kaname Date` directory and moved the
   screenshot from (2) into it.

## Configuration

The app's one and only configuration file is `$XDG_CONFIG_HOME/steamapps.map.json`. It
contains a map of game name overrides for when you don't like the name the game has on
Steam. Example:

```json
{
  "2752180": "No Sleep for Kaname Date"
}
```

You can overrride this file location using the `-o` parameter if you want/need to.

## Redistribution

Feel free to package and re-distribute this small app however you want. I would
appreciate it if you could also include the link to this repository somewhere in
the package meta.

