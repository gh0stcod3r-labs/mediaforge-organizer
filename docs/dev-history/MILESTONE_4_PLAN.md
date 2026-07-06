# MediaForge Milestone 4 — Provider Polish, Performance & Cross-Platform

## Overview

Stabilize MediaForge for real-world testing on Windows and macOS. Focus on provider reliability, batch performance, and platform-specific edge cases.

**Milestone 3 Status**: ✅ Complete (UI, Match Engine, File Operations)  
**Milestone 4 Phase 1 Status**: ✅ COMPLETE (Foundation Built & Integrated)  
**Goal**: Production-ready provider integration with robust error handling.

---

## ✅ Phase 1: Foundation (COMPLETE)

### ✅ Phase 1.1: Settings Persistence
- ✅ Created `config.py` with `SettingsManager`
- ✅ Settings stored to `~/.mediaforge/settings.json`
- ✅ Integrated into app.py
- ✅ Window geometry restoration
- ✅ Provider selection persistence
- ✅ API key storage (local, never in repo)
- ✅ Last used paths remembered

---

### ✅ Phase 1.2: Error Messages & UX
- ✅ Created `error_handler.py` with 20+ friendly error types
- ✅ Created `dialogs.py` with 4 custom dialogs
- ✅ Integrated into app.py
- ✅ All exceptions caught and shown as friendly messages
- ✅ User suggestions included with each error
- ✅ Technical errors logged for debugging

---

### ✅ Phase 1.3: Advanced Filename Matching
- ✅ Created `matcher.py` with AdvancedMatcher
- ✅ Supports 9+ filename patterns (S01E01, 1x01, Episode, etc.)
- ✅ Removes fansub tags, codec info, quality tags
- ✅ Confidence scoring system
- ✅ Integrated as OfflineProvider

---

### ✅ Phase 1.4: Provider Architecture
- ✅ Created `providers/__init__.py` with `BaseProvider`
- ✅ Created `providers/offline_provider.py`
- ✅ Provider framework ready for Phase 2 adapters
- ✅ ProviderStatus enum, ProviderResponse dataclass

---

### ✅ Phase 1.5: Integration into App.py
- ✅ Settings restoration on startup
- ✅ Provider selection UI
- ✅ API key configuration dialog
- ✅ Progress dialog during batch operations
- ✅ Friendly error handling throughout
- ✅ Window geometry persistence
- ✅ Undo confirmation dialog

---

## Core Implementation (Phase 2: Providers & Quality)

### Phase 2.1: Provider Hardening (Days 3-5)
Priority: **HIGH** — Core functionality

**Files to update:**
- Create provider adapters: `src/mediaforge/providers/` folder
  - `base_provider.py` — Abstract base
  - `tmdb_provider.py` — TMDB adapter
  - `anilist_provider.py` — AniList adapter
  - `mal_provider.py` — MyAnimeList/Jikan adapter
  - `tvmaze_provider.py` — TVMaze adapter
  - `offline_provider.py` — Local parser fallback
  - `ai_cleanup_provider.py` — Optional AI title cleanup

**Tasks per provider:**
- [ ] Graceful timeout handling (5s default)
- [ ] Retry logic (exponential backoff)
- [ ] Rate limit detection (429, 503)
- [ ] Invalid API key detection (401, 403)
- [ ] No match handling (return low-confidence)
- [ ] Bad response handling (malformed JSON, missing fields)
- [ ] No internet handling (offline mode)
- [ ] Return clean MatchResult with provider, confidence, metadata

---

### Phase 2.2: Match Quality (Days 5-7)
Priority: **HIGH** — Core output quality

**Files to create:**
- `src/mediaforge/matcher.py` — Advanced filename parsing

**Tasks:**
- [ ] Improve anime filename parsing: strip fansub tags, codec tags
- [ ] Support anime episode formats: S01E01, 1x01, Episode 01, absolute numbers
- [ ] Improve TV filename parsing: handle year in title, episode ranges
- [ ] Improve movie parsing: extract year reliably
- [ ] Handle messy release names: version numbers, region codes, quality tags
- [ ] Mark results <70% confidence as "Needs Review"
- [ ] Return structured metadata (title, season, episode, year, type)

---

## Performance & Reliability (Phase 3)

### Phase 3.1: Batch Performance (Days 7-9)
Priority: **MEDIUM** — Real-world stress test

**Files to update:**
- `src/mediaforge/app.py` — Add worker threads/async
- `src/mediaforge/rename_engine.py` — Add cancellation support

**Tasks:**
- [ ] Profile with 50, 300, 1000+ files
- [ ] Implement work queue (threading or asyncio)
- [ ] No UI freeze during match phase
- [ ] Live progress updates (files/sec, ETA)
- [ ] Cancellable operations (graceful shutdown)
- [ ] Preserve partial results if cancelled
- [ ] Incremental log writes

---

### Phase 3.2: Plan Preview & Logging (Days 9-11)
Priority: **MEDIUM** — UX refinement

**Files to update:**
- `src/mediaforge/app.py` — Add Plan Preview table
- `src/mediaforge/logger.py` — Enhance logging, add export

**Tasks:**
- [ ] Display final operation plan (read-only table)
- [ ] Columns: original file, destination folder, final filename, operation, provider, confidence, status
- [ ] Add warnings column (low confidence, skipped duplicates)
- [ ] Operation log: readable format with all fields
- [ ] Add CSV export
- [ ] Add JSON export

---

### Phase 3.3: Undo Hardening (Days 11-12)
Priority: **MEDIUM** — Safety critical

**Files to update:**
- `src/mediaforge/rename_engine.py` — Track folder creation
- `src/mediaforge/logger.py` — Enhance undo logic

**Tasks:**
- [ ] Track which folders were created by MediaForge
- [ ] Undo: only delete empty MediaForge-created folders
- [ ] Confirm dialog before destructive undo
- [ ] Log undo results
- [ ] Handle missing files gracefully
- [ ] Test undo with partial failures

---

## Cross-Platform & Polish (Phase 4)

### Phase 4.1: Cross-Platform Hardening (Days 12-14)
Priority: **MEDIUM** — Stability

**Files to audit:**
- All modules — pathlib compliance check

**Tasks:**
- [ ] Verify pathlib used everywhere (no hardcoded separators)
- [ ] Handle Windows reserved names: CON, PRN, AUX, NUL, COM1-9, LPT1-9
- [ ] Handle invalid filename chars: < > : " | ? * \0
- [ ] Check path length (260 on Windows, ~4096 on Unix)
- [ ] Case-sensitive filesystem detection (for rename conflicts)
- [ ] Permission error handling
- [ ] External drive detection
- [ ] Network drive warnings

---

### Phase 4.2: Settings Persistence Integration (Days 14-15)
Priority: **LOW** — Polish

**Tasks:**
- [ ] Restore window size/position on startup
- [ ] Restore last selected provider
- [ ] Restore last selected operation mode
- [ ] Restore last destination root
- [ ] Restore theme preference
- [ ] Restore column widths (if applicable)

---

## Testing (Phase 5)

### Phase 5.1: Test Matrix (Days 15-17)
Priority: **HIGH** — Quality assurance

**Test cases:**
- [ ] Clean anime season (20 files, properly named)
- [ ] Messy anime (fansub tags, version numbers)
- [ ] TV show season (30 files)
- [ ] Movie folder (10 files)
- [ ] Mixed folder (anime + TV + movies)
- [ ] No internet (offline mode)
- [ ] Missing API key (graceful prompt)
- [ ] Invalid API key (friendly error)
- [ ] Duplicate destination file (skip/replace dialog)
- [ ] Copy to external drive
- [ ] Move across drives
- [ ] Dry run (no changes)
- [ ] Undo after copy/move/rename

---

### Phase 5.2: Documentation (Days 17-18)
Priority: **MEDIUM** — User guidance

**README sections:**
- [ ] Basic workflow: scan → match → preview → execute
- [ ] Match providers: which provider, when used, priority
- [ ] API key setup: per-provider instructions
- [ ] AI Title Cleanup: optional, how it works
- [ ] Copy vs Move: when to use each
- [ ] Dry Run: preview without changes
- [ ] Undo limitations: what can/can't be undone
- [ ] Windows/macOS notes: known issues, workarounds
- [ ] Troubleshooting: common errors

---

## Acceptance Criteria

- [x] Provider errors do not crash app
- [ ] Large batches remain responsive
- [ ] Match results are higher quality
- [ ] Plan Preview is accurate
- [ ] Operation Log is exportable
- [ ] Undo is safer
- [ ] Settings persist
- [ ] Windows/macOS path issues handled
- [ ] README updated
- [ ] No UI redesign
- [ ] No licensing yet

---

## Implementation Order

**Week 1:**
1. Settings persistence (`config.py`)
2. Error handling (`error_handler.py`, `dialogs.py`)
3. Provider base class and adapters

**Week 2:**
4. Match quality improvements
5. Batch performance optimization
6. Plan preview & logging enhancements

**Week 3:**
7. Undo hardening
8. Cross-platform edge cases
9. Settings integration
10. Documentation

---

## Files to Create/Update

**Create:**
- `src/mediaforge/config.py` — Settings manager
- `src/mediaforge/error_handler.py` — Error messages
- `src/mediaforge/dialogs.py` — Custom dialogs
- `src/mediaforge/providers/base_provider.py`
- `src/mediaforge/providers/tmdb_provider.py`
- `src/mediaforge/providers/anilist_provider.py`
- `src/mediaforge/providers/mal_provider.py`
- `src/mediaforge/providers/tvmaze_provider.py`
- `src/mediaforge/providers/offline_provider.py`
- `src/mediaforge/providers/ai_cleanup_provider.py`
- `src/mediaforge/matcher.py` — Advanced parsing
- `tests/test_providers.py`
- `tests/test_cross_platform.py`

**Update:**
- `src/mediaforge/app.py` — Integrate all above
- `src/mediaforge/rename_engine.py` — Cancellation, folder tracking
- `src/mediaforge/logger.py` — Enhanced logging, export
- `README.md` — User documentation

---

## Success Metrics

- **Reliability**: Provider errors handled gracefully, no crashes
- **Performance**: 1000 files processed in <2 min, responsive UI
- **Quality**: >80% of matches >80% confidence
- **Safety**: Undo works correctly, no data loss
- **Usability**: First-time user can scan, match, execute without errors
- **Documentation**: README covers all major workflows

---

**Status**: 🚀 Ready to begin Phase 1  
**Target completion**: ~3 weeks of focused development
