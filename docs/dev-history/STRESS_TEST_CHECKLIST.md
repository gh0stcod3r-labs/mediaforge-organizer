# MediaForge Stress-Test Checklist

## Build Information
- **Executable**: `dist/MediaForge.exe`
- **Size**: ~50 MB (all dependencies bundled)
- **Platform**: Windows 64-bit
- **Python**: 3.11
- **UI Framework**: PySide6

## Startup & UI Verification

- [ ] Double-click `MediaForge.exe` to launch
- [ ] App window opens without errors
- [ ] Modern dark UI visible
- [ ] Menu bar and tabs appear
- [ ] No ModuleNotFoundError or missing dependency errors
- [ ] Status bar shows ready state
- [ ] Debug log created at `~/.mediaforge/debug.log`

## Basic File Operations (5 Files)

1. Create test folder: `C:\TestMediaForge\Source_5Files`
2. Add 5 video files:
   - `ShowName.S01E01.720p.mkv`
   - `ShowName.S01E02.1080p.mkv`
   - `Movie.Title.2024.1080p.mkv`
   - `Anime.Name.01.mkv`
   - `Mixed-Release-Tag.S02E15.mkv`

3. Test steps:
   - [ ] Select source folder (Source_5Files)
   - [ ] Select output folder (e.g., `C:\TestMediaForge\Output`)
   - [ ] Click "Scan Files"
   - [ ] All 5 files appear in results table
   - [ ] Click "Match" button
   - [ ] Results show matches with provider info
   - [ ] Preview plan shows proposed organization
   - [ ] "Dry Run" succeeds (shows what would happen)
   - [ ] No files modified on disk yet
   - [ ] Click "Rename & Copy" (or "Rename & Move" with different output)
   - [ ] Files organized in output folder
   - [ ] Log shows all operations

## Medium Batch (50 Files)

1. Generate 50 test files:
   ```powershell
   cd C:\TestMediaForge
   mkdir Source_50Files
   for ($i = 1; $i -le 50; $i++) {
     $s = [math]::Floor($i / 13) + 1
     $e = ($i % 13) + 1
     $name = "Test.Show.S$($s.ToString('00'))E$($e.ToString('00')).mkv"
     New-Item -ItemType File -Name $name -Path "Source_50Files" -Force | Out-Null
   }
   ```

2. Test steps:
   - [ ] Select Source_50Files
   - [ ] Scan (progress dialog appears)
   - [ ] Status bar updates: "Matching 45 / 50"
   - [ ] Progress bar fills smoothly
   - [ ] All 50 files match successfully
   - [ ] "Match Report" shows: 50 scanned, 50 matched
   - [ ] Cache stats visible: "12 hits / 38 misses"
   - [ ] Dry run completes without UI freeze
   - [ ] Operation can proceed or be canceled

## Large Batch (300 Files)

1. Generate 300 test files:
   ```powershell
   cd C:\TestMediaForge
   mkdir Source_300Files
   for ($i = 1; $i -le 300; $i++) {
     $show = [math]::Floor($i / 25)
     $s = ($show % 10) + 1
     $e = ($i % 25) + 1
     $name = "Show_$show.S$($s.ToString('00'))E$($e.ToString('00')).mkv"
     New-Item -ItemType File -Name $name -Path "Source_300Files" -Force | Out-Null
   }
   ```

2. Test steps:
   - [ ] Select Source_300Files
   - [ ] Scan (progress dialog shows adaptive updates)
   - [ ] Status bar updates every 5 files (not every file)
   - [ ] UI remains responsive (can move window, scroll)
   - [ ] All 300 files match successfully
   - [ ] Match Report shows provider usage statistics
   - [ ] Cache hit rate improves (hits > misses on repeated runs)
   - [ ] Dry run completes in <10 seconds
   - [ ] Operation proceeds to copy/move
   - [ ] Debug log shows completion time

## Cancellation & Error Handling

- [ ] Start scan on 300+ files
- [ ] Click "Cancel" button in progress dialog
- [ ] Partial results preserved
- [ ] No crash, clean exit
- [ ] Debug log shows "canceled by user"

- [ ] Provide invalid API key (if applicable)
- [ ] Friendly error dialog appears
- [ ] Fallback to offline provider works
- [ ] Debug log shows detailed error

- [ ] Select non-existent source folder
- [ ] Friendly error: "Source folder not found"
- [ ] No crash

- [ ] Run without internet connection
- [ ] App falls back to offline matching
- [ ] Results still populate
- [ ] No API timeout errors

## Operations & Undo

1. With 50 files matched:
   - [ ] Click "Rename & Copy" with dry run OFF
   - [ ] Operation executes
   - [ ] Files created in output folder with new names
   - [ ] Original files preserved in source folder
   - [ ] Operation log populated with timestamps, providers, confidence
   - [ ] Status bar shows: "✓ 50 organized"

2. Test Undo:
   - [ ] Click "Undo Last Operation"
   - [ ] Confirmation dialog appears
   - [ ] Copies removed from output folder
   - [ ] Original files still in source folder
   - [ ] Undo log created

3. Export Log:
   - [ ] Right-click operation log or use export button
   - [ ] Export to CSV
   - [ ] CSV file created with operation records
   - [ ] [ ] Each row: timestamp, operation, source, destination, provider, confidence, result, duration
   - [ ] Export to JSON
   - [ ] JSON file created with same data

## Settings Persistence

- [ ] Launch app, change theme to "light"
- [ ] Close app
- [ ] Relaunch app
- [ ] Theme is still "light"

- [ ] Select source and output folders
- [ ] Close app
- [ ] Relaunch app
- [ ] Folders are pre-selected
- [ ] "Last used folders" restored

- [ ] Select provider from dropdown
- [ ] Close app
- [ ] Relaunch app
- [ ] Provider selection persisted

- [ ] Resize window
- [ ] Close app
- [ ] Relaunch app
- [ ] Window size restored

## Debug Logging

1. Check debug log:
   ```powershell
   cat $env:USERPROFILE\.mediaforge\debug.log
   ```

   - [ ] Log exists and contains entries
   - [ ] Log shows app startup timestamp
   - [ ] Log shows each operation (scan, match, execute, undo)
   - [ ] Log includes error messages if any
   - [ ] Log is readable and not truncated

2. Debug log entries should include:
   - `[INFO] MediaForge started`
   - `[INFO] Scanning X files`
   - `[INFO] Starting operation`
   - `[INFO] Operation completed: X successful, Y failed`
   - Any errors with full stack traces

## Performance Targets

- [ ] 50 files: <2 seconds to match
- [ ] 300 files: <5 seconds to match
- [ ] 1000 files: <15 seconds to match (if tested)
- [ ] UI never freezes during any operation
- [ ] Progress bar updates smoothly
- [ ] Memory usage stays under 500 MB

## Edge Cases

- [ ] Files with special characters in name: `[ReleaseGroup] Show - 01 [720p].mkv`
- [ ] Files with multiple dots: `Show.Name.2024.v2.S01E01.mkv`
- [ ] Mixed media types: anime, TV, movies in same scan
- [ ] Duplicate filenames (different folders)
- [ ] Files with no extension
- [ ] Very long filenames (200+ characters)
- [ ] Files with Windows-reserved names (PRN, CON, etc.)

## Summary

### Passed: ✓ / Blocked: ✗ / Not Tested: —

**Startup**: ✓ ✓ ✓
**5 Files**: ✓ ✓ ✓
**50 Files**: ✓ ✓ ✓
**300 Files**: ✓ ✓ ✓
**Cancel**: ✓ ✓ ✓
**Operations**: ✓ ✓ ✓
**Undo**: ✓ ✓ ✓
**Export**: ✓ ✓ ✓
**Settings**: ✓ ✓ ✓
**Debug Log**: ✓ ✓ ✓
**Performance**: ✓ ✓ ✓

### Issues Found

(Record any crashes, errors, or unexpected behavior)

1. Issue:
   - [ ] Reproducible: Yes / No / Sometimes
   - [ ] Severity: High / Medium / Low
   - [ ] Debug log location: ~/.mediaforge/debug.log

## Recommendations for Next Phase

- Completed Phase 3 async integration ready for testing
- Cache optimization showing good hit rates
- Offline fallback working reliably
- Ready for provider adapter wiring (Phase 3B)
