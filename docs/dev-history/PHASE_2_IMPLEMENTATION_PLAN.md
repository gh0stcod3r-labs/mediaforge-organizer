# 📋 MediaForge Milestone 4 — Phase 2 Implementation Plan

## Scope

Implement 4 real metadata providers using the BaseProvider framework established in Phase 1.

**Do NOT**:
- Redesign UI
- Change RenameEngine
- Change MatchResult structure
- Change Operation Log
- Change Undo
- Add licensing

---

## Provider Implementation Order

### 1. Cache System (Foundation)
**File**: `src/mediaforge/cache.py`
- Local cache manager using `~/.mediaforge/cache/`
- JSON-based cache with TTL (24 hours default)
- Keys: provider + query → result
- Methods: get(), set(), clear(), is_expired()

### 2. TMDB Provider (High Priority)
**File**: `src/mediaforge/providers/tmdb_provider.py`
- API: https://api.themoviedb.org/3
- Supports: TV shows, Movies
- Returns: title, season, episode, episode title, year, TMDB ID, confidence
- Error handling: invalid key, timeout, rate limit, no match
- Caching: enabled

### 3. AniList Provider (High Priority)
**File**: `src/mediaforge/providers/anilist_provider.py`
- API: GraphQL https://graphql.anilist.co
- Supports: Anime series
- Returns: English title, Romaji, episode count, year, AniList ID, confidence
- No authentication needed
- Error handling: timeout, rate limit, no match
- Caching: enabled

### 4. MAL/Jikan Provider (High Priority)
**File**: `src/mediaforge/providers/mal_provider.py`
- API: https://api.jikan.moe/v4
- Supports: Anime
- Returns: official title, alternative titles, episode count, year, MAL ID, confidence
- No authentication needed
- Error handling: timeout, rate limit, no match
- Caching: enabled

### 5. TVMaze Provider (High Priority)
**File**: `src/mediaforge/providers/tvmaze_provider.py`
- API: https://www.tvmaze.com/api
- Supports: TV series
- Returns: series, episode title, season, episode, TVMaze ID, confidence
- No authentication needed
- Error handling: timeout, rate limit, no match
- Caching: enabled

### 6. Provider Selection Logic
**File**: `src/mediaforge/providers/provider_selector.py`
- Auto-detect media type (anime vs TV vs movie)
- Fallback chain: Anime → TMDB → TVMaze → Offline
- Intelligent provider ordering

### 7. Confidence Scoring
**File**: `src/mediaforge/providers/scoring.py`
- Title match: +40
- Season match: +20
- Episode match: +20
- Year match: +10
- Episode title match: +10
- Max: 100%
- < 80% = Needs Review

### 8. Integration into app.py
- Populate provider combo with real providers
- Test connection button
- API key configuration
- Status bar updates
- Cache statistics reporting

---

## Confidence Scoring System

```
Base Score: 0%

Title matched exactly:        +40
Title matched (fuzzy):        +30
Season matched:               +20
Episode matched:              +20
Year matched:                 +10
Episode title matched:        +10
Source has season/episode:    +10 (if provider-specific field)

Maximum: 100%
Minimum: 0%

< 50%:  Red    (No Match)
50-79%: Yellow (Needs Review)
80%+:   Green  (Confident)
```

---

## API Error Handling Strategy

All providers handle gracefully:
- **401/403**: Invalid API key → friendly error + settings prompt
- **404**: No results found → mark as "No Match"
- **429**: Rate limited → exponential backoff (1s, 2s, 4s, 8s)
- **500+**: Server error → retry once after 2s, then fail gracefully
- **Timeout** (5s default): Fallback to offline provider
- **No internet**: Catch socket error → fallback to offline provider

---

## Response Cache

**Location**: `~/.mediaforge/cache/`

**Cache Format**:
```json
{
  "provider": "TMDB",
  "query": "Attack on Titan 2013",
  "result": {
    "title": "Attack on Titan",
    "year": 2013,
    "season": 1,
    "episode": null,
    "provider": "TMDB",
    "confidence": 0.95,
    "id": "30984"
  },
  "timestamp": 1719792787,
  "ttl": 86400
}
```

**Cache Keys**:
- TMDB: `tmdb_tv_{series_query}` or `tmdb_movie_{movie_query}`
- AniList: `anilist_{query}`
- MAL: `mal_{query}`
- TVMaze: `tvmaze_{query}`

**Batch Optimization**:
- Cache hit before API call
- Multiple files with same series → 1 API call
- Example: 318 anime episodes of same series → 1 series lookup + N episode lookups (cached)

---

## Implementation Timeline

**Day 1**: Cache system + TMDB provider
**Day 2**: AniList + MAL/Jikan providers
**Day 3**: TVMaze provider + Provider selector
**Day 4**: Integration + Testing
**Day 5**: Polish + Documentation

---

## Testing Checklist

### TMDB Provider
- [ ] Search TV show (Breaking Bad)
- [ ] Search movie (Inception)
- [ ] Handle invalid API key
- [ ] Handle timeout
- [ ] Handle rate limit
- [ ] Cache working
- [ ] Confidence scoring accurate

### AniList Provider
- [ ] Search anime (Attack on Titan)
- [ ] Parse Romaji + English title
- [ ] Episode count correct
- [ ] Timeout handling
- [ ] Cache working
- [ ] Confidence scoring

### MAL Provider
- [ ] Search anime (Demon Slayer)
- [ ] Alternative titles
- [ ] Episode count
- [ ] Timeout handling
- [ ] Cache working

### TVMaze Provider
- [ ] Search TV show (Breaking Bad)
- [ ] Episode lookup
- [ ] Timeout handling
- [ ] Cache working

### Integration
- [ ] All 4 providers in combo box
- [ ] API key dialog works
- [ ] Auto-detection works (anime → AniList first)
- [ ] Fallback chain works
- [ ] Batch matching with cache optimization
- [ ] UI unchanged

---

## Status Bar Updates

Show real-time information:
```
✔ Ready | 📁 318 Files | 🎯 TMDB | 📊 Cache: 95 hits, 5 misses | ⏳ Matching...
```

---

## Acceptance Criteria

- ✅ TMDB provider works (TV + movies)
- ✅ AniList provider works (anime)
- ✅ MAL/Jikan provider works (anime)
- ✅ TVMaze provider works (TV)
- ✅ Automatic provider selection
- ✅ Confidence scoring accurate
- ✅ Caching reduces API calls
- ✅ Batch optimization working
- ✅ Friendly error handling
- ✅ API keys stored securely (settings)
- ✅ UI unchanged
- ✅ RenameEngine untouched

---

## Notes

- All API keys go through SettingsManager (never hardcoded)
- All timeouts default to 5 seconds
- All providers return MatchResult (no provider-specific types)
- Fallback chain: Anime → AniList → MAL → TMDB → Offline
- UI shows provider used + confidence + cache status
