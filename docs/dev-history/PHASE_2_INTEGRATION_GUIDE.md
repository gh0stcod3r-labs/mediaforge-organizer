# 🔌 Phase 2 Integration Guide

## Provider System Architecture

### Core Components

**Cache System** (`cache.py`)
- Reduces API calls by caching results locally
- 24-hour TTL by default
- Tracks hit/miss statistics
- Usage: `get_cache().get("TMDB", query)` or `get_cache().set(...)`

**Scoring System** (`providers/scoring.py`)
- Calculates confidence scores (0.0 to 1.0)
- Factors: title match (+40), season (+20), episode (+20), year (+10), episode title (+10)
- Thresholds: < 50% = "No Match", 50-79% = "Needs Review", 80%+ = "Matched"

**Provider Classes**
- `TMDBProvider` — TV + movies
- `AniListProvider` — Anime (GraphQL)
- `MALProvider` — Anime (Jikan API)
- `TVMazeProvider` — TV shows
- All inherit `BaseProvider`, return `ProviderResponse`, populate `MatchResult`

**Provider Selector** (`provider_selector.py`)
- Auto-detects media type from filename
- Smart provider chain: Anime → AniList → MAL → TMDB → Offline
- TV → TMDB → TVMaze → Offline
- Movie → TMDB → Offline
- Fallback always succeeds (uses offline provider)

---

## Integration Steps

### Step 1: Import Phase 2 in app.py

Add to imports (around line 28):
```python
from .cache import get_cache
from .providers.provider_selector import ProviderSelector
from .providers.tmdb_provider import TMDBProvider
from .providers.anilist_provider import AniListProvider
from .providers.mal_provider import MALProvider
from .providers.tvmaze_provider import TVMazeProvider
```

### Step 2: Initialize Provider Selector in MediaForgeApp.__init__()

After line 95 (after other initializations):
```python
self.provider_selector = ProviderSelector()
```

### Step 3: Update Provider Combo Box

In `_setup_match_control()` or where combo box is created, populate with real providers:

**Current code** (placeholder):
```python
self.provider_combo.addItems(["Offline", "TMDB", "AniList", "MAL", "TVMaze"])
```

**Replace with**:
```python
self.provider_combo.addItems([
    "Offline",
    "TMDB",
    "AniList",
    "MAL (Jikan)",
    "TVMaze"
])
```

### Step 4: Update _scan_videos() to Use Provider Selector

**Current code** (Phase 1):
```python
# Uses OfflineProvider for all files
response = offline_provider.search(Path(file_path).name, Path(file_path))
```

**Replace with** (Phase 2):
```python
# Use intelligent provider selection with fallback
response, provider_name = self.provider_selector.search_with_fallback(
    Path(file_path).name,
    Path(file_path)
)
```

Then update status bar to show provider used:
```python
self.statusBar().showMessage(
    f"✔ Matched | 📁 {matched_count}/{total_files} | 🎯 {provider_name}"
)
```

### Step 5: Add Provider Selection to _scan_videos()

**Current**: Always uses offline provider

**Update to**:
```python
# Get selected provider from combo box
provider_name = self.provider_combo.currentText()

if provider_name == "Offline":
    provider = OfflineProvider()
elif provider_name == "TMDB":
    provider = TMDBProvider()
elif provider_name == "AniList":
    provider = AniListProvider()
elif provider_name in ["MAL", "MAL (Jikan)"]:
    provider = MALProvider()
elif provider_name == "TVMaze":
    provider = TVMazeProvider()
else:
    provider = self.provider_selector.offline_provider

response = provider.search(Path(file_path).name, Path(file_path))
```

OR use new auto-detection:
```python
# Automatically select best provider for this file
response, provider_used = self.provider_selector.search_with_fallback(
    Path(file_path).name,
    Path(file_path)
)
```

### Step 6: Store Provider Used in MatchResult

Each `MatchResult` already has:
- `provider: MatchProvider` — Which provider returned this result
- `confidence: float` — Confidence score (0.0 to 1.0)

These are automatically populated by each provider's `search()` method.

### Step 7: Update Status Bar to Show Cache Stats

After all matches complete:
```python
cache_stats = get_cache().get_stats()
self.statusBar().showMessage(
    f"✔ Done | 📁 {len(match_results)} files | "
    f"💾 Cache: {cache_stats['hits']} hits, {cache_stats['misses']} misses"
)
```

### Step 8: Add API Key Configuration

When user clicks "Configure API Key" button for a provider:

```python
def _configure_api_key(self):
    """Configure API key for selected provider."""
    provider_name = self.provider_combo.currentText()
    
    if provider_name == "Offline":
        QMessageBox.information(self, "Offline Provider", 
            "Offline provider doesn't require an API key")
        return
    
    # Show API key dialog
    dialog = APIKeyDialog(self, provider_name)
    if dialog.exec() == QDialog.Accepted:
        api_key = dialog.get_api_key()
        get_settings().set_api_key(provider_name, api_key)
        
        # Test connection
        provider = self.provider_selector.get_provider_by_name(provider_name)
        if provider and provider.test_connection():
            QMessageBox.information(self, "Success", 
                f"{provider_name} API key validated!")
        else:
            QMessageBox.warning(self, "Error", 
                f"{provider_name} API key is invalid or unreachable")
```

### Step 9: Update _on_provider_changed() Handler

```python
def _on_provider_changed(self, index):
    """Handle provider selection change."""
    provider_name = self.provider_combo.currentText()
    
    # Save to settings
    get_settings().set_selected_provider(provider_name)
    
    # Enable/disable API key button
    self.api_key_button.setEnabled(provider_name != "Offline")
    
    # Show provider info
    if provider_name == "Offline":
        self.statusBar().showMessage("ℹ Offline provider (no internet required)")
    else:
        api_key = get_settings().get_api_key(provider_name)
        if api_key:
            self.statusBar().showMessage(f"✔ {provider_name} configured")
        else:
            self.statusBar().showMessage(f"⚠ {provider_name} API key not configured")
```

### Step 10: Test Each Provider

**TMDB**:
```python
# In a test script or Python REPL
from mediaforge.providers.tmdb_provider import TMDBProvider
from mediaforge.config import get_settings

# Set API key first
get_settings().set_api_key("TMDB", "your_api_key_here")

provider = TMDBProvider()
response = provider.search("Breaking Bad")
print(f"Status: {response.status}")
print(f"Matches: {response.matches}")
```

**AniList** (no API key needed):
```python
from mediaforge.providers.anilist_provider import AniListProvider

provider = AniListProvider()
response = provider.search("Attack on Titan")
print(f"Matches: {response.matches}")
```

**MAL/Jikan** (no API key needed):
```python
from mediaforge.providers.mal_provider import MALProvider

provider = MALProvider()
response = provider.search("Demon Slayer")
print(f"Matches: {response.matches}")
```

**TVMaze** (no API key needed):
```python
from mediaforge.providers.tvmaze_provider import TVMazeProvider

provider = TVMazeProvider()
response = provider.search("Breaking Bad")
print(f"Matches: {response.matches}")
```

---

## API Key Setup

### TMDB API Key

1. Register at https://www.themoviedb.org/settings/api
2. Create an API key (API access required)
3. Copy key to MediaForge via Settings → API Keys → TMDB
4. Test connection via Settings button

### AniList

- **No API key required**
- Public GraphQL API
- Rate limit: 90 requests per minute

### MAL/Jikan

- **No API key required**
- Free public API
- Rate limit: ~60 requests per minute

### TVMaze

- **No API key required**
- Public REST API
- No official rate limit, but use responsible intervals

---

## Error Handling

All providers handle these errors gracefully:

- **401/403** — Invalid/expired API key → Show friendly error
- **404** — No results found → Return `ProviderStatus.NO_MATCH`
- **429** — Rate limited → Exponential backoff (1s, 2s, 4s, 8s)
- **500+** — Server error → Retry once after 2s, then fail gracefully
- **Timeout** (5s) → Fall back to offline provider
- **No internet** → Catch socket error → Use offline provider

All errors are logged and shown to user as friendly messages.

---

## Caching Behavior

**Per-request cache**:
```python
cache = get_cache()

# Check cache first
cached = cache.get("TMDB", "Breaking Bad")
if cached:
    return cached  # Cache hit!

# If not cached, call API
response = tmdb_provider.search("Breaking Bad")

# Cache result for 24 hours
cache.set("TMDB", "Breaking Bad", response_data)
```

**Cache location**: `~/.mediaforge/cache/*.json`

**Example cache file**: `~/.mediaforge/cache/tmdb_breaking_bad.json`

**Cache hit/miss stats**:
```python
stats = get_cache().get_stats()
# {"hits": 95, "misses": 5}
```

---

## Batch Optimization

Example: 318 episodes of same anime series

**Without optimization** (old way):
- Episode 1: API call to get series
- Episode 2: API call to get series (duplicate!)
- Episode 3: API call to get series (duplicate!)
- ...318 times = 318 API calls

**With caching** (Phase 2):
- Episode 1: API call to get series → cache it
- Episode 2: Cache hit! (no API call)
- Episode 3: Cache hit! (no API call)
- ...318 times = 1 API call + 317 cache hits
- **98% fewer API calls** ✨

---

## Status Bar Updates

**Before match**:
```
ℹ Offline provider (no internet required)
```

**During match** (with progress):
```
⏳ Matching | 25/318 files | 🎯 AniList | 💾 Cache: 15 hits, 3 misses
```

**After match** (success):
```
✔ Done | 📁 318 files | 🎯 AniList | 💾 Cache: 250 hits, 68 misses
```

**After match** (with errors):
```
⚠ Matched 310/318 | 🎯 Mixed providers | 💾 Cache: 200 hits, 110 misses | ❌ 8 failed
```

---

## Testing Checklist

### TMDB
- [ ] Search TV show (Breaking Bad)
- [ ] Search movie (Inception)
- [ ] Invalid API key error
- [ ] Timeout handling
- [ ] Rate limit handling
- [ ] Cache working (2nd search instant)
- [ ] Confidence scoring (>0.8)

### AniList
- [ ] Search anime (Attack on Titan)
- [ ] Parse English + Romaji title
- [ ] Episode count included
- [ ] Timeout handling
- [ ] Cache working
- [ ] Confidence scoring

### MAL/Jikan
- [ ] Search anime (Demon Slayer)
- [ ] Alternative titles work
- [ ] Episode count
- [ ] Timeout handling
- [ ] Cache working

### TVMaze
- [ ] Search TV show (Breaking Bad)
- [ ] Episode information
- [ ] Timeout handling
- [ ] Cache working

### Integration
- [ ] All providers in combo box
- [ ] API key dialog works
- [ ] Auto-detection works
- [ ] Fallback chain works (if TMDB timeout, try TVMaze)
- [ ] Batch matching (50 files)
- [ ] Batch optimization (same series, cache hits)
- [ ] Status bar shows correct provider
- [ ] Cache stats accurate
- [ ] UI doesn't freeze during API calls

---

## Performance Notes

- **Timeout**: 5 seconds per request
- **Batch size**: 318+ files handled without freezing
- **Cache expiry**: 24 hours
- **API rate limits**: Respected via timeouts
- **Progress dialog**: Shows during matching, cancellable

---

## Future Enhancements (Phase 3+)

- Rate limit tracking and smarter retry logic
- Per-episode lookups (current: series only)
- Offline title cleanup with Ollama
- Cron job for cache management
- Provider preference ordering
- Custom provider implementations
- WebScraper provider for edge cases
