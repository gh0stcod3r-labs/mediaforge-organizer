# Phase 3 Integration Checklist - Next Session

**Goal**: Wire Phase 3 components into app.py and test real-world batches  
**Estimated Time**: 5-7 hours (integration + testing)  
**Difficulty**: Medium (straightforward API integration)

---

## Pre-Integration Checklist

- [x] All Phase 3 core components built (5/5)
- [x] All verification checks pass (6/6)
- [x] All audit checks pass (4/4)
- [x] Zero breaking changes confirmed
- [x] Documentation complete

**Status: READY FOR INTEGRATION ✅**

---

## Integration Tasks (In Order)

### Task 1: Import AsyncMatcher into app.py
**Time**: 15 minutes

```python
# Add to imports (around line 20)
from mediaforge.async_matcher import AsyncMatcher

# Add to __init__ (around line 95)
self.async_matcher = AsyncMatcher(max_workers=3, timeout=10)
```

**Verification**:
- [ ] app.py still launches without errors
- [ ] `audit_check.py` still passes 4/4

### Task 2: Refactor _scan_videos() to Use AsyncMatcher
**Time**: 1 hour

**Current pattern** (line ~350):
```python
# Old sequential matching
for filename in video_files:
    match = self.offline_provider.search(filename)
```

**New async pattern**:
```python
# New parallel matching with progress
self.progress_dialog = ProgressDialog(self)
self.progress_dialog.show()

def progress_callback(current, total, current_file):
    self.progress_dialog.update_progress(current, total, current_file)
    self.statusBar().showMessage(f"Matching {current}/{total}: {current_file}")

results, completed = self.async_matcher.match_batch_with_progress(
    filenames=video_files,
    selector=self.provider_selector,
    callback=progress_callback
)

self.progress_dialog.close()
```

**Verification**:
- [ ] Test with 50 files - should be <100ms
- [ ] Test with 300 files - should show progress updates
- [ ] Cancel button works
- [ ] Results match previous version

### Task 3: Display MatchReport After Operation
**Time**: 30 minutes

```python
# After matching completes
from mediaforge.match_report import MatchReport

report = MatchReport.from_matches(
    matches=[(result, "OFFLINE") for result in results],
    provider_stats=None
)

# Show report in dialog or status panel
print(report.summary())

# Optional: save to file
# report_path = Path.home() / ".mediaforge" / "last_report.txt"
# with open(report_path, "w") as f:
#     f.write(report.summary())
```

**Verification**:
- [ ] Report displays after match
- [ ] Shows matched/needs_review/no_match counts
- [ ] Shows provider usage

### Task 4: Wire Cancel Button to AsyncMatcher
**Time**: 15 minutes

```python
# Find cancel button in UI (around line ~420)
self.cancel_button.clicked.connect(self._on_cancel_match)

# Add handler
def _on_cancel_match(self):
    if hasattr(self, 'async_matcher'):
        self.async_matcher.cancel()
    if hasattr(self, 'progress_dialog'):
        self.progress_dialog.close()
```

**Verification**:
- [ ] Cancel button stops matching
- [ ] Partial results preserved
- [ ] No crashes on cancel

### Task 5: Add Operation Log Export Buttons
**Time**: 30 minutes

```python
# Add buttons near operation log area
export_csv_button = QPushButton("Export CSV")
export_csv_button.clicked.connect(self._export_operations_csv)

export_json_button = QPushButton("Export JSON")
export_json_button.clicked.connect(self._export_operations_json)

# Add handlers
def _export_operations_csv(self):
    path = QFileDialog.getSaveFileName(self, "Save Operations", "", "CSV (*.csv)")[0]
    if path:
        self.logger.export_csv(Path(path))
        self.statusBar().showMessage("Operations exported to CSV")

def _export_operations_json(self):
    path = QFileDialog.getSaveFileName(self, "Save Operations", "", "JSON (*.json)")[0]
    if path:
        self.logger.export_json(Path(path))
        self.statusBar().showMessage("Operations exported to JSON")
```

**Verification**:
- [ ] Export buttons work
- [ ] CSV file contains correct data
- [ ] JSON file contains correct data

### Task 6: Plan Preview Hardening
**Time**: 30 minutes

**Current Plan Preview** (around line ~580):
- [ ] Add columns: provider, confidence
- [ ] Make table read-only (set `setEditTriggers(QAbstractItemView.NoEditTriggers)`)
- [ ] Populate provider column with `match.provider.value`
- [ ] Populate confidence column with `f"{int(match.confidence*100)}%"`

**Verification**:
- [ ] Provider column shows correctly
- [ ] Confidence column shows correctly
- [ ] No editing possible

---

## Testing Matrix (3 hours)

### Performance Tests
```python
# Test 50 files (instant)
python -c "
import time
from mediaforge.async_matcher import AsyncMatcher
from mediaforge.providers.provider_selector import ProviderSelector

files = [f'file_{i}.mkv' for i in range(50)]
selector = ProviderSelector()
matcher = AsyncMatcher()

start = time.time()
results, completed = matcher.match_batch(files, selector)
elapsed = time.time() - start

print(f'50 files: {elapsed:.2f}s')
assert elapsed < 0.5, 'Should be instant'
"

# Test 300 files (responsive, ~5-10s)
# Test 1000 files (completes in ~30s)
```

### Functional Tests
- [ ] Cache hits reduce 2nd run time
- [ ] Cancel preserves partial results
- [ ] Error handling graceful
- [ ] No memory leaks (profile with memory_profiler)

---

## Integration Validation Checklist

### After Each Task
- [ ] `audit_check.py` still passes 4/4
- [ ] `verify_phase3.py` still passes 6/6
- [ ] No new error messages in logs
- [ ] UI remains responsive

### Final Validation
- [ ] All Phase 3 components integrated
- [ ] All integration tasks complete
- [ ] All verification checks pass
- [ ] All testing matrix items pass
- [ ] Zero breaking changes

---

## Success Criteria

**Phase 3 integration is complete when:**

✅ AsyncMatcher wired into _scan_videos()  
✅ Progress updates show during match  
✅ MatchReport displays after operation  
✅ Cancel button works correctly  
✅ Operation log export works  
✅ 50 files test <100ms  
✅ 300 files test ~5-10s responsive  
✅ 1000 files test completes in ~30s  
✅ All audit checks pass 4/4  
✅ Zero breaking changes  

---

## If Things Go Wrong

### AsyncMatcher Not Responding
1. Check if `max_workers=3` is reasonable for your system
2. Try `max_workers=1` temporarily to test sequential fallback
3. Check for provider timeout issues (default 10s)

### Progress Updates Not Showing
1. Verify callback is wired: `callback=progress_callback`
2. Check statusBar().showMessage() is being called
3. Ensure QThread doesn't block UI

### Memory Issues
1. Profile with `memory_profiler`
2. Check that results aren't being stored multiple times
3. Ensure GC can collect old batches

### Plan Preview Not Updating
1. Verify table is being refreshed: `self.matches_table.setModel()`
2. Check column indices match data
3. Ensure read-only flag doesn't prevent display

---

## Next Steps After Integration

Once Phase 3 integration complete:
1. Run full test suite
2. Test on macOS (cross-platform verification)
3. Profile with real 1000-file batch
4. Performance benchmarking
5. Create Phase 4 plan (licensing, GitHub releases, etc.)

---

## Files Reference

### Core Components (Use in Integration)
- `src/mediaforge/async_matcher.py` - Main async engine
- `src/mediaforge/match_report.py` - Report generation
- `src/mediaforge/cache.py` (v2) - Enhanced cache
- `src/mediaforge/logger.py` - Export methods

### Integration Point
- `src/mediaforge/app.py` - Main application file
  - _scan_videos() method (line ~350)
  - UI initialization (__init__)
  - Button connections

### Verification Tools
- `audit_check.py` - Verify no breaking changes
- `verify_phase3.py` - Verify Phase 3 components

---

**Ready to integrate!** Start with Task 1 and work through sequentially. Each task builds on the previous one.
