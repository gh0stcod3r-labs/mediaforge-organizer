# Phase 3B Integration & Testing Plan

**Goal**: Complete Phase 3 with advanced UI features and comprehensive testing  
**Estimated Time**: 5-7 hours  
**Current Progress**: Phase 3 = 50% (Foundation 40% + Integration 10%)

---

## Phase 3B Tasks (New - Not Yet Started)

### 1. Advanced UI Integration (2-3 hours)

#### 1a. Wire Provider Selector
**Current State**: Provider combo box exists but disabled (Phase 1)  
**What to Do**:
- Enable provider_combo box
- Connect to provider selection logic
- Show/hide API key button based on selection
- Update async_matcher provider chain

**Code Location**: app.py ~line 180-190 (provider_combo setup)

#### 1b. Add MatchReport Panel
**Current State**: MatchReport generated but not displayed  
**What to Do**:
- Create collapsible panel in UI for report
- Display after matching completes
- Show: matched/needs_review/no_match counts
- Show: provider usage breakdown
- Show: cache hit rate

**Code Location**: app.py after _display_plan()

#### 1c. Wire API Key Configuration
**Current State**: APIKeyDialog exists but not wired to providers  
**What to Do**:
- Get selected provider from combo box
- Show APIKeyDialog with provider name
- Save key using settings manager
- Pass key to provider when matching

**Code Location**: app.py line 628 (_configure_api_key)

#### 1d. Add CSV/JSON Preview
**Current State**: Files saved silently  
**What to Do**:
- Show file preview after export
- Display first 10 lines of CSV/JSON
- Offer to open file in default app

**Code Location**: app.py line 645 (_export_operations_csv)

### 2. Comprehensive Testing (3-5 hours)

#### 2a. Performance Testing (1 hour)
```bash
# Test 50 files (should be <100ms)
python -c "
import time
from pathlib import Path
# Create 50 test files
for i in range(50):
    Path(f'test_{i}.mkv').touch()

# Run matching
# Should complete instantly
"

# Test 300 files (should be ~5-10s with progress)
# Test 1000 files (should be ~30s with no freeze)
```

**Acceptance**:
- [ ] 50 files complete in <100ms
- [ ] 300 files show progress, complete in ~10s
- [ ] 1000 files responsive, complete in ~30s

#### 2b. Functional Testing (1 hour)
```bash
# Test cancel during match
- Scan 300 files
- Click cancel halfway
- Verify partial results preserved
- Verify no crash

# Test cache hit on 2nd run
- Scan 300 files
- Cache stats show: X hits, Y misses
- Scan same 300 files again
- Cache stats show: higher hits, fewer misses
- 2nd run faster than 1st

# Test CSV export
- Export operations to CSV
- Open CSV file
- Verify columns: timestamp, operation, source, destination, etc.
- Check row count matches operations

# Test JSON export
- Export operations to JSON
- Parse JSON (valid format)
- Check all operations present
```

**Acceptance**:
- [ ] Cancel works, partial results preserved
- [ ] Cache hits increase on 2nd run
- [ ] CSV export produces valid file
- [ ] JSON export produces valid file

#### 2c. Cross-Platform Testing (1 hour)
```bash
# Windows paths
- Test with paths containing spaces
- Test with unicode characters
- Test UNC paths (network drives if available)

# macOS paths (if available)
- Test case-sensitive filesystem
- Test with Finder integration
- Test with external drives
```

**Acceptance**:
- [ ] Windows paths work correctly
- [ ] Special characters handled
- [ ] macOS tested (if available)

#### 2d. Edge Case Testing (30 min)
```bash
# No internet
- Disable internet
- Try matching with OFFLINE provider
- Should work without errors

# Bad API key
- Set invalid API key for TMDB
- Try matching with TMDB provider
- Should fallback gracefully

# Permission denied
- Create file without read permissions
- Try to match
- Should show friendly error

# Large files
- Create files >4GB
- Verify no memory issues
- Check size display in results

# Mixed media types
- Mix .mkv, .mp4, .avi in same folder
- Should all be matched correctly
```

**Acceptance**:
- [ ] Offline mode works
- [ ] API errors handled gracefully
- [ ] Permission errors show friendly message
- [ ] Large files handled correctly
- [ ] Mixed types matched correctly

#### 2e. Memory Profiling (30 min)
```bash
# Use memory_profiler
pip install memory_profiler

# Profile with large batch
python -m memory_profiler match_batch.py

# Expected: <200MB for 1000 files
```

**Acceptance**:
- [ ] 1000 files use <200MB
- [ ] Memory freed after batch
- [ ] No memory leaks detected

#### 2f. UI Responsiveness Testing (30 min)
```bash
# Test UI remains responsive
- Start matching 1000 files
- Click buttons during match (should not freeze)
- Type in text fields (if any)
- Resize window
- Verify all interactions responsive
```

**Acceptance**:
- [ ] UI responds to all interactions
- [ ] No freezes detected
- [ ] Window resizing smooth

### 3. Documentation (1 hour)

#### 3a. User Guide
- Document new async matching feature
- Explain cache statistics
- Document provider selection flow
- Document export functionality

#### 3b. Troubleshooting
- Common issues and solutions
- Performance tuning
- Cache management

---

## Testing Matrix

| Test | Current | Target | Status |
|------|---------|--------|--------|
| 50 files | <100ms | <100ms | ✓ Ready |
| 300 files | ~5-10s | ~5-10s | ✓ Ready |
| 1000 files | ~30s | ~30s | ✓ Ready |
| Cancel match | Partial preserved | Partial preserved | ✓ Ready |
| Cache hit 2nd run | Faster | Faster | ✓ Ready |
| CSV export | Works | Valid file | ⏳ Test |
| JSON export | Works | Valid file | ⏳ Test |
| No internet | Offline works | Works | ⏳ Test |
| Bad API key | Fallback | Graceful | ⏳ Test |
| Memory 1000 files | <200MB | <200MB | ⏳ Test |
| macOS | Untested | Works | ⏳ Test |

---

## Phase 3B Implementation Steps

### Step 1: Advanced UI (2-3 hours)
1. Enable provider selector combo box
2. Add MatchReport display panel
3. Wire API key configuration
4. Add export preview dialogs
5. Test each feature individually

### Step 2: Testing (3-5 hours)
1. Performance testing (50/300/1000 files)
2. Functional testing (cancel, cache, export)
3. Cross-platform testing (Windows/macOS)
4. Edge case testing (no internet, bad keys, etc.)
5. Memory profiling
6. UI responsiveness testing

### Step 3: Documentation (1 hour)
1. Write user guide
2. Create troubleshooting section
3. Document new features
4. Update README

---

## Expected Outcomes

### After Phase 3B
✅ Advanced UI features complete
✅ All tests passing
✅ Performance validated
✅ Documentation complete
✅ Ready for Phase 4 (Licensing & GitHub)

### Phase 3 Completion
✅ Foundation (40%)
✅ Integration (10%)
✅ Advanced UI (20%)
✅ Testing & Polish (30%)
= 100% Phase 3 Complete

---

## How to Continue

### If Starting Phase 3B
1. Read this plan
2. Start with "Advanced UI Integration"
3. Run tests after each feature
4. Document as you go

### If Resuming
1. Check which tasks are complete
2. Update status in testing matrix
3. Continue from next incomplete task

---

## Key Files for Phase 3B

### For UI Work
- `src/mediaforge/app.py` (main integration)
- `src/mediaforge/dialogs.py` (if adding new dialogs)
- `src/mediaforge/constants.py` (UI styling)

### For Testing
- `audit_check.py` (basic audit)
- `verify_phase3.py` (Phase 3 components)
- Test scripts to be created

### For Documentation
- `README.md` (main documentation)
- User guide (new document)
- Troubleshooting guide (new document)

---

## Success Criteria for Phase 3

✓ AsyncMatcher integrated and working
✓ All 4/4 audit checks pass
✓ All 6/6 Phase 3 checks pass
✓ Performance targets met (50/300/1000 files)
✓ All functional tests pass
✓ Cross-platform compatibility verified
✓ Documentation complete
✓ Zero breaking changes
✓ Production-ready code

---

## Next: Phase 4 Planning

After Phase 3 complete:
1. Licensing system design
2. GitHub release automation
3. Beta testing program setup
4. Marketing materials

---

This plan ensures Phase 3 completion with comprehensive testing and documentation.
