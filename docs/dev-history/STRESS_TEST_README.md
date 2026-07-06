# MediaForge Organizer — Stress-Test Build

## Quick Start

### System Requirements
- **Windows 10** or **Windows 11** (64-bit)
- **No Python installation required** (all dependencies bundled)
- **Recommended RAM**: 4 GB or more
- **Recommended Storage**: 1 GB free disk space

### Launch
1. Extract `MediaForge.exe` from `dist/` folder
2. Double-click `MediaForge.exe`
3. App window opens with modern dark UI

### First Run
- Debug log created at: `C:\Users\<YourUsername>\.mediaforge\debug.log`
- Settings saved at: `C:\Users\<YourUsername>\.mediaforge\settings.json`
- Cache created at: `C:\Users\<YourUsername>\.mediaforge\cache\`

## Basic Workflow

1. **Select Source Folder**
   - Click "Browse..." next to "Source Folder"
   - Choose folder containing video files

2. **Select Output Folder**
   - Click "Browse..." next to "Output Folder"
   - Choose destination folder

3. **Click "Scan Files"**
   - MediaForge scans for video files (.mkv, .mp4, .avi, etc.)
   - Progress dialog shows scanning progress
   - Results table populates with files

4. **Click "Match"**
   - Each file is parsed for metadata
   - Provider determines series name, season, episode
   - Confidence score calculated
   - Results update live in table

5. **Review Plan**
   - "Plan Preview" tab shows proposed organization
   - Verify filenames, destinations, operations
   - Read-only (no editing here)

6. **Dry Run (Recommended)**
   - Click "Dry Run" button
   - Simulates operation without modifying files
   - Shows what would happen
   - Verify output before proceeding

7. **Execute Operation**
   - Click "Rename & Copy" or "Rename & Move"
   - Confirmation dialog appears
   - Operation executes with progress updates
   - Original files preserved (copy) or moved (move)

8. **Review & Export Log**
   - Operation Log tab shows detailed record
   - Timestamps, providers, confidence, status
   - Export to CSV or JSON for external review

9. **Undo (if needed)**
   - Click "Undo Last Operation"
   - Removes files created by MediaForge
   - Preserves original files

## Features in This Build

### Integrated (Phase 3A)
✓ Modern UI with light/dark theme  
✓ File scanning and parsing  
✓ Provider-based metadata matching  
✓ Confidence scoring (0-100%)  
✓ Batch operations (50, 300, 1000+ files)  
✓ Progress dialog with cancel button  
✓ Async matching with intelligent fallback  
✓ Cache system with hit/miss tracking  
✓ Smart cache key generation  
✓ Corruption recovery  
✓ Operation logging (timestamp, provider, confidence, result)  
✓ Export to CSV/JSON  
✓ Settings persistence (theme, folders, provider selection)  
✓ Friendly error messages  
✓ Debug logging to file  
✓ Dry Run preview  
✓ Undo with safety checks  
✓ Rename + Copy  
✓ Rename + Move  

### Tested
- 5 file batch
- 50 file batch
- 300 file batch
- Cancellation during scan
- Fallback to offline matching (no internet)
- Cache hit on repeated batches
- Settings persistence across restarts
- Operation undo without data loss

### Not Yet in This Build
- Manual provider selection wiring (can select but limited effect)
- TMDB, AniList, MAL, TVMaze provider selection UI integration
- API key configuration UI (providers work with offline fallback)
- Match Report display panel
- Advanced match report statistics display

## Testing Strategy

**Use included**: `STRESS_TEST_CHECKLIST.md`

Quick test (5 min):
- Launch app
- Create 5 test files
- Scan and match
- Dry run
- Verify output

Medium test (20 min):
- Generate 50 test files
- Full workflow
- Check performance
- Export log

Heavy test (1 hour):
- Generate 300 test files
- Full workflow with cache testing
- Cancel operations
- Test undo
- Check debug log

## Troubleshooting

### App Won't Launch
1. Check Windows Defender/Antivirus (may block new .exe)
2. Right-click `MediaForge.exe` → Properties → General → Check "Unblock"
3. Extract to a different folder (not Desktop, try Documents)
4. Check debug log for error: `C:\Users\<You>\.mediaforge\debug.log`

### "ModuleNotFoundError" on Launch
- Indicates dependency not bundled correctly
- Report with full error from debug log
- Workaround: Run from source with `python src/main.py`

### Files Won't Match
- Offline provider parses filenames into: Title, Season, Episode
- If filename is too messy, confidence may be low
- Use file format: `ShowName.S01E01.mkv` or `ShowName 1x01.mkv`

### Performance Issues (UI Freeze)
- Expected: Phase 3 async matching may need tuning
- Check debug log for provider lookup times
- Workaround: Disable async matching (settings)
- Report with file count and debug log

### Permission Denied on Undo
- Destination folder may be locked by another app
- Close other file managers/explorers
- Try undo again

### Cache Corruption
- Delete `C:\Users\<You>\.mediaforge\cache\`
- App will regenerate on next match
- Check debug log for details

## Log Locations

**Debug Log**:  
`C:\Users\<YourUsername>\.mediaforge\debug.log`

**Settings**:  
`C:\Users\<YourUsername>\.mediaforge\settings.json`

**Cache**:  
`C:\Users\<YourUsername>\.mediaforge\cache\`

**Operation Log** (in-app):  
Operations tab → Export CSV/JSON

## Stress Test Goals

1. **Stability**: No crashes on 50, 300, 1000+ file batches
2. **Performance**: UI stays responsive during matching
3. **Accuracy**: Filenames parsed correctly
4. **Logging**: All operations recorded with provider and confidence
5. **Fallback**: Works without internet or API keys (offline mode)
6. **Persistence**: Settings survive restarts
7. **Safety**: Undo works without data loss
8. **Export**: Logs exportable as CSV/JSON

## Reporting Issues

When reporting issues:
1. Note exact steps to reproduce
2. Include file count and filename examples
3. Attach debug log: `~/.mediaforge/debug.log`
4. Describe what happened vs. what was expected
5. Note Windows version (10 or 11)

## Architecture Notes

**Phase 1**: UI + Rename Engine (Baseline)  
**Phase 2**: Provider Adapters (TMDB, AniList, MAL, TVMaze)  
**Phase 3**: Performance Foundation (Async, Cache, Reporting)  
**Phase 3A**: Integration (This Build) ✓  
**Phase 3B**: Upcoming (Provider UI wiring, MatchReport display)  

This build focuses on **stability and real-world validation** before continuing feature development.

## Next Steps (After Testing)

1. Gather stress-test feedback
2. Fix any critical bugs
3. Tune async matching parameters (workers, timeouts)
4. Wire provider selector to actual TMDB/AniList/etc.
5. Add MatchReport display panel
6. Add API key configuration dialog
7. Comprehensive cross-platform testing (macOS)
8. Performance optimization (1000+ file batches)
9. Release as stable beta

---

**Build Date**: [Generated on stress-test phase start]  
**Executable**: `dist/MediaForge.exe` (~50 MB)  
**Status**: Ready for stress testing ✓  
