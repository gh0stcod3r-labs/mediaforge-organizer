# 📋 MediaForge Milestone 4 — Phase 3 Implementation Plan

## Scope

Production-readiness for large real-world batches (50-1000+ files).

**Phase 1**: ✅ Foundation  
**Phase 2**: ✅ Providers  
**Phase 3**: 🟡 Performance (this phase)  
**Phase 4**: Planning Cross-platform  
**Phase 5**: Planning Documentation  

---

## Core Priorities (in order)

### 1. Enhanced Cache System
**File**: Update `src/mediaforge/cache.py`
- Smarter cache keys: provider + normalized query + media type + year + season/episode
- Schema versioning for cache entries
- Corruption recovery (detect and handle malformed JSON)
- Better hit/miss tracking
- Cache statistics export

### 2. Parallel Provider Lookup
**File**: New `src/mediaforge/async_matcher.py`
- ThreadPoolExecutor for concurrent provider searches
- Respect provider rate limits (max 2-3 concurrent)
- Preserve result ordering
- Cancel support (stop new tasks, keep completed)
- Memory-efficient (no file content loading)

### 3. Cancel/Resume Handling
**Update**: `src/mediaforge/app.py` _scan_videos()
- Flag-based cancellation (thread-safe)
- Preserve partial results
- Update UI status
- Summary on cancellation

### 4. Plan Preview Hardening
**Update**: Existing Plan Preview dialog
- Display all MatchResult fields
- Read-only view (no editing)
- Status/warning column
- Export functionality

### 5. Operation Log Export
**Update**: `src/mediaforge/logger.py`
- CSV export
- JSON export
- Incremental writing during operations
- Statistics: success count, failure count, duration

### 6. Match Report
**New**: `src/mediaforge/match_report.py`
- Summary statistics
- Provider usage breakdown
- Cache hit/miss ratio
- API failure tracking
- Confidence distribution
- Display in UI (new dialog or status)

### 7. Status Bar Updates
**Update**: `src/mediaforge/app.py` status bar
- Live progress: "Matching 145 / 318"
- Current provider
- Cache hit/miss
- Errors count

---

## Implementation Details

### 1. Enhanced Cache System

```python
# Better cache key structure
def get_cache_key(provider, query, media_type=None, year=None, season=None):
    """Create normalized cache key."""
    normalized = query.lower().strip()
    # Remove common filler
    for word in ["720p", "1080p", "[", "]", "."]:
        normalized = normalized.replace(word, "")
    
    key_parts = [provider, normalized, media_type or "unknown"]
    if year:
        key_parts.append(str(year))
    if season:
        key_parts.append(f"s{season}")
    
    return "|".join(key_parts)

# Cache entry with metadata
@dataclass
class CacheEntry:
    key: str
    result: MatchResult
    timestamp: float
    ttl_seconds: int = 86400
    schema_version: int = 1
    provider_version: str = "1.0"
```

### 2. Parallel Matching

```python
class AsyncMatcher:
    """Parallel provider lookup with rate limiting."""
    
    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.cancel_flag = threading.Event()
    
    def match_batch(self, filenames, selector):
        """Match files in parallel."""
        futures = []
        results = []
        
        for i, filename in enumerate(filenames):
            if self.cancel_flag.is_set():
                break
            
            future = self.executor.submit(
                selector.search_with_fallback,
                filename
            )
            futures.append((i, future))
        
        # Collect results preserving order
        for index, future in futures:
            try:
                result = future.result(timeout=10)
                results.append((index, result))
            except Exception as e:
                # Log error, continue
                pass
        
        return results
    
    def cancel(self):
        """Signal cancellation."""
        self.cancel_flag.set()
```

### 3. Cancel/Resume

```python
# In _scan_videos()
self.match_cancelled = False

def _on_cancel_match(self):
    """Cancel ongoing match operation."""
    self.match_cancelled = True

# In match loop
if self.match_cancelled:
    break

# After match completes
if self.match_cancelled:
    QMessageBox.information(self, "Canceled",
        f"Matched {len(matched)}/{total_files} files")
else:
    QMessageBox.information(self, "Success",
        f"Matched {len(matched)}/{total_files} files")
```

### 4. Plan Preview

**Existing Plan Preview, enhanced**:
- Add columns: provider, confidence, status
- Make read-only
- Add "Export as CSV" button
- Display as table (not editable list)

### 5. Operation Log Export

```python
# In OperationLogger
def export_csv(self, path):
    """Export operations to CSV."""
    import csv
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timestamp', 'operation', 'source', 'destination',
            'provider', 'confidence', 'status', 'duration', 'error'
        ])
        writer.writeheader()
        for op in self.operations:
            writer.writerow(op.to_dict())

def export_json(self, path):
    """Export operations to JSON."""
    import json
    with open(path, 'w') as f:
        json.dump(
            [op.to_dict() for op in self.operations],
            f, indent=2
        )
```

### 6. Match Report

```python
@dataclass
class MatchReport:
    files_scanned: int
    files_matched: int
    files_needs_review: int
    files_no_match: int
    
    provider_usage: Dict[str, int]  # {"TMDB": 150, "AniList": 100}
    cache_hits: int
    cache_misses: int
    api_failures: int
    
    confidence_distribution: Dict[str, int]  # {"80-100": 200, "50-79": 50}
    estimated_folders_created: int
    
    def summary(self) -> str:
        """Generate text summary."""
        return f"""
        Matched: {self.files_matched}/{self.files_scanned}
        Needs Review: {self.files_needs_review}
        No Match: {self.files_no_match}
        
        Cache: {self.cache_hits} hits, {self.cache_misses} misses
        API Failures: {self.api_failures}
        """
```

### 7. Status Bar

```python
# Update during matching
for i, filename in enumerate(filenames):
    self.statusBar().showMessage(
        f"Matching {i+1}/{len(filenames)} | "
        f"Provider: {current_provider} | "
        f"Cache: {cache_hits} hits, {cache_misses} misses"
    )
    QApplication.processEvents()  # Keep UI responsive
```

---

## Phase 3 Tasks (Daily Breakdown)

### Day 1: Cache Hardening
- [ ] Add normalized cache keys
- [ ] Add schema versioning
- [ ] Add corruption recovery
- [ ] Test with 50 files

### Day 2: Parallel Matching
- [ ] Create AsyncMatcher class
- [ ] Integrate with ProviderSelector
- [ ] Add cancel support
- [ ] Test with 300 files

### Day 3: Cancel/Resume & Plan Preview
- [ ] Implement cancel handlers
- [ ] Enhance Plan Preview
- [ ] Add export buttons
- [ ] Test cancellation

### Day 4: Operation Log & Reports
- [ ] CSV export
- [ ] JSON export
- [ ] Match report generation
- [ ] Display in UI

### Day 5: Status Bar & Polish
- [ ] Live status updates
- [ ] Performance testing (1000 files)
- [ ] Memory profiling
- [ ] Bug fixes

---

## Testing Targets

### Batch Sizes
- [ ] 50 files (should be instant)
- [ ] 300 files (should be ~5-10 seconds)
- [ ] 1000 files (should be ~20-30 seconds)

### Scenarios
- [ ] Cache hit path (second run)
- [ ] Cache miss path (first run)
- [ ] Mix of anime/TV/movie
- [ ] No internet (fallback to offline)
- [ ] Provider timeout
- [ ] Cancel during match
- [ ] Duplicate files same series

### Performance Targets
- [ ] UI never freezes (progress updates every 100ms)
- [ ] Memory stable (< 200MB for 1000 files)
- [ ] Cache hits show 10× speedup
- [ ] Parallel reduces time by 2-3×

---

## API Changes

### MetadataCache (Enhanced)

```python
get_cache_key(provider, query, media_type, year, season) -> str
get_with_key(key) -> Optional[MatchResult]
set_with_key(key, result, ttl) -> None
get_stats() -> CacheStats
export_stats() -> Dict
```

### AsyncMatcher (New)

```python
match_batch(filenames, selector) -> List[MatchResult]
cancel() -> None
is_cancelled() -> bool
get_progress() -> int  # current index
```

### MatchReport (New)

```python
from_results(results) -> MatchReport
summary() -> str
to_dict() -> Dict
```

---

## Backward Compatibility

✅ All changes are additive (no breaking changes)
✅ Existing APIs still work unchanged
✅ RenameEngine not modified
✅ MatchResult not modified
✅ UI not redesigned

---

## Success Criteria

| Criterion | Measure | Target |
|-----------|---------|--------|
| Batch performance | 300 files | < 10 seconds |
| Large batch | 1000 files | < 30 seconds |
| Responsiveness | UI freezes | 0 (progress every 100ms) |
| Memory usage | 1000 files | < 200 MB |
| Cache speedup | Cache hits | 10× faster |
| Parallel speedup | With threading | 2-3× faster |
| Cancel support | Works? | Yes, preserves results |
| Export support | CSV/JSON | Both working |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Threading bugs | Careful lock usage, test thoroughly |
| Memory growth | Profile, use iterators not lists |
| Cache corruption | Validation, recovery, clear option |
| Order loss | Track indices, restore order |
| Rate limits | Respect limits, add backoff |

---

## Documentation

- `PHASE_3_PLAN.md` — This file (architecture)
- `PHASE_3_TESTING.md` — Test cases and procedures
- `PHASE_3_PERFORMANCE.md` — Performance profiling results
- Code comments — Method-level documentation
- Docstrings — Class-level documentation

---

## Next Phase Planning

Phase 4 (Cross-platform & Stability):
- Windows/macOS path edge cases
- Undo safety improvements
- Settings persistence completeness

Phase 5 (Documentation & Release):
- README updates
- User guide
- Troubleshooting
- GitHub release automation

---

## Summary

Phase 3 transforms MediaForge from a single-batch organizer into a production-ready system:

- ✅ Handles 1000+ files smoothly
- ✅ Intelligent caching (10× speedup)
- ✅ Parallel matching (2-3× speedup)
- ✅ Cancel/resume support
- ✅ Rich reporting and export
- ✅ Live status updates
- ✅ Zero breaking changes

**Timeline**: 5 days  
**Complexity**: High (threading, caching, UI updates)  
**Impact**: Transforms from demo to production tool
