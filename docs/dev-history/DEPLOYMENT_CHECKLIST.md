# MediaForge Stress-Test Build — Deployment Checklist

## Pre-Deployment Verification

- [x] Build completed successfully
- [x] Executable created: `dist/MediaForge.exe` (47.4 MB)
- [x] Phase 3 verification passed (6/6 checks)
- [x] Audit checks passed (4/4 checks)
- [x] No build errors or warnings
- [x] Debug logging enabled and tested
- [x] All dependencies bundled

## Files Ready for Distribution

### Executable
```
dist/MediaForge.exe  (47.4 MB)
```
Single-file Windows executable. No installation needed. Just download and double-click.

### Documentation
```
STRESS_TEST_README.md           - Quick start guide
STRESS_TEST_CHECKLIST.md         - Test scenarios
STRESS_TEST_BUILD_SUMMARY.md     - Build details & acceptance criteria
```

## System Requirements for Users

- Windows 10 or Windows 11 (64-bit)
- No Python installation required
- 4 GB RAM minimum
- 1 GB free disk space

## User Instructions

### 1. Download & Extract
- User downloads `MediaForge.exe`
- User creates test folder: `C:\TestMediaForge\`
- User copies `MediaForge.exe` into test folder (or Documents, Desktop, etc.)

### 2. First Launch
- Double-click `MediaForge.exe`
- App launches in 2-3 seconds
- Modern dark UI appears
- Status bar shows "Ready"

### 3. First Test (5 Files)
- Create test folder: `Source_5Files`
- Add 5 video files (or any .mkv/.mp4 files)
- Select folders in UI
- Click "Scan Files"
- Results appear
- Click "Match"
- Click "Dry Run" to preview
- Review "Plan Preview" tab
- Click "Rename & Copy" to execute

### 4. Monitor Progress
- Progress dialog shows real-time updates
- Status bar shows: "Matching X / Y"
- Debug log written to: `~/.mediaforge/debug.log`

### 5. Verify Output
- Check output folder for organized files
- Review "Operation Log" tab
- Export log to CSV or JSON if desired

### 6. Run Additional Tests
- Follow scenarios in `STRESS_TEST_CHECKLIST.md`
- Test 50-file and 300-file batches
- Test cancellation
- Test undo
- Check performance metrics

## Troubleshooting for Users

If app won't launch:
1. Right-click → Properties → General → Check "Unblock" button
2. Move executable to a different folder (e.g., Documents)
3. Check `~/.mediaforge/debug.log` for error details
4. Report error with debug log content

If files won't match:
- Use filename format like: `ShowName.S01E01.mkv`
- Check debug log for detailed parsing info
- Offline provider should work regardless of internet

If UI freezes:
- Note file count and filename patterns
- Report with debug log

## Collect Feedback

Users should report:
1. **What worked**: Specific features, file counts, operations
2. **What failed**: Error messages, filename examples, steps to reproduce
3. **Performance**: File count, time taken, CPU/memory usage
4. **Debug log**: Upload `~/.mediaforge/debug.log` with any crashes

## After Testing

### Success Path
- User reports: "All tests passed, 300 files organized in 4 seconds"
- Next: Proceed to Phase 3B (provider UI wiring, MatchReport display)

### Issues Path
- User reports specific crashes/errors
- Investigation: Review debug log, reproduce issue
- Fix: Address critical bugs
- Rebuild: Create new .exe with fixes
- Retest: Verify fix

## Sign-Off

- [x] Executable ready
- [x] Documentation complete
- [x] Verification passed
- [x] Deployment checklist created
- [x] Ready to send to user for stress testing

**Status**: ✓ Ready for distribution

---

## For User: What to Expect

### Execution Timeline
- **Startup**: 2-3 seconds
- **Scan 5 files**: <1 second
- **Match 5 files**: 1-2 seconds
- **Scan 50 files**: 1-2 seconds
- **Match 50 files**: 2-3 seconds
- **Scan 300 files**: 2-3 seconds
- **Match 300 files**: 4-6 seconds
- **Operation (copy/move)**: Depends on file sizes

### Expected Debug Log Entries
```
[INFO] === MediaForge App Starting ===
[INFO] Settings loaded
[INFO] Core components initialized
[INFO] Phase 3 components initialized (async_matching enabled)
[INFO] UI setup complete
[INFO] Scanning X files
[INFO] Using AsyncMatcher for parallel matching
[INFO] Matching X / Y
[INFO] Operation completed: X successful, 0 failed, 0 skipped
```

### Success Indicators
- App opens without errors
- Files appear in results table
- Provider info shows in match results
- Confidence scores reasonable (60-100%)
- Operations execute without crashing
- Logs export cleanly
- Undo works safely

---

**Build Date**: 2026-06-30  
**Build Version**: M4-Phase-3A-Stress-Test-v1  
**Status**: Ready for real-world stress testing ✓
