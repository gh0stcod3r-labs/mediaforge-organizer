# MediaForge Organizer

A local-first desktop app for renaming and organizing video files (TV shows, anime, movies) into a clean, consistent folder structure — built with PySide6.

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Three-panel layout** — input files on the left, settings behind a single gear icon in the middle, and the organized output (new filename + destination folder) on the right
- **Metadata providers** — TMDB, AniList, MyAnimeList (Jikan), TVMaze, or fully offline filename parsing; "Automatic" mode chains providers and rejects low-confidence matches instead of accepting the wrong show
- **Smart filename parsing** — handles `S01E01`, `1x01`, `Episode 01`, bare anime numbering (`Show - 01`), standalone season markers (`S2`, `Season 2`, `2nd Season`), and absolute episode numbering for long-running shows (e.g. converts `One Piece - 1085` to the correct season/episode using the show's real per-season episode counts)
- **Safety first** — copy by default (never touches originals), optional move mode, dry-run preview, and an undo log for the last batch
- **Drag & drop** — drop files or folders straight onto the input panel, or scan a source folder
- **Duplicate-safe** — automatically resolves filename collisions in the destination
- **Operation log** — every rename/copy/move is logged and exportable to CSV/JSON

## Folder Structure

```
Destination/Series Name/Season 01/Series Name - S01E01 - Episode Title.ext
Destination/Movie Title/Movie Title - 2010.ext
```

## Installation

### Run from source

```
git clone https://github.com/<your-org>/mediaforge-organizer.git
cd mediaforge-organizer
pip install -r requirements.txt
python src/main.py
```

Requires Python 3.8+ and PySide6. Works fully offline; TMDB/AniList/MyAnimeList/TVMaze are optional and only used if you configure them in Settings.

### Prebuilt Windows executable

Download `MediaForge.exe` from the [Releases](../../releases) page — no Python install required.

## Usage

1. **Browse** to a source folder (or drag files/folders onto the input panel) and an output folder.
2. Click the **gear icon** to choose a metadata provider, media category, and copy/move/dry-run behavior. TMDB/AniList/MAL/TVMaze API keys (if used) are configured there too.
3. Click **Scan Videos** to parse and match every file.
4. Review the **Organized Output** panel — it shows the new filename and destination folder for each file before anything happens on disk.
5. Click **Rename & Copy** (or **Rename & Move**, depending on Settings) to execute. Use **Undo Last** to revert the most recent batch.

## Building the executable

```
pip install pyinstaller
pyinstaller MediaForge.spec
```

The output is written to `dist/MediaForge.exe`.

## Project Structure

```
mediaforge/
  src/
    main.py                    # Application entry point
    mediaforge/
      app.py                   # PySide6 UI (3-panel layout)
      dialogs.py                # Settings, API key, progress, undo dialogs
      scanner.py                # Video file discovery
      matcher.py                 # Filename -> title/season/episode parsing
      rename_engine.py           # Destination path + filename construction
      config.py                  # Persisted settings
      cache.py                   # Provider response caching
      logger.py                  # Operation log + undo stack
      providers/                 # TMDB, AniList, MAL, TVMaze, offline
  tests/
    test_rename_engine.py        # Regression tests for parsing/naming
  docs/dev-history/               # Internal development notes/checkpoints
```

## Running tests

```
python tests/test_rename_engine.py
```

## License

MIT — see [LICENSE](LICENSE).
