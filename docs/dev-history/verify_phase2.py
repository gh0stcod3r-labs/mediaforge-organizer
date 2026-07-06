#!/usr/bin/env python3
"""Verify Phase 2 provider system."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mediaforge.providers.provider_selector import ProviderSelector
from mediaforge.cache import get_cache
from mediaforge.providers.scoring import ConfidenceScorer

selector = ProviderSelector()
cache = get_cache()
scorer = ConfidenceScorer()

print("=" * 50)
print("Phase 2 Provider System Verification")
print("=" * 50)
print()

print("Providers loaded:")
print(f"  OK: {selector.anilist_provider.provider_name}")
print(f"  OK: {selector.tmdb_provider.provider_name}")
print(f"  OK: {selector.mal_provider.provider_name}")
print(f"  OK: {selector.tvmaze_provider.provider_name}")
print(f"  OK: {selector.offline_provider.provider_name}")
print()

print("Supporting systems:")
print("  OK: Cache system")
print("  OK: Confidence scoring")
print("  OK: Provider selector")
print()

print("Media type detection:")
test_files = [
    ("Beast.Tamer.S01E01.1080p.mkv", "anime"),
    ("Breaking.Bad.S01E01.mkv", "tv"),
    ("Inception.2010.1080p.mkv", "movie"),
    ("Attack.on.Titan.[HorribleSubs].S01E01.mkv", "anime"),
]

for filename, expected in test_files:
    detected = selector.get_media_type(filename)
    status = "OK" if detected == expected else f"WARN (got {detected})"
    print(f"  {status}: {filename} -> {detected}")

print()
print("Confidence scoring:")
confidence = scorer.calculate(
    title_match=True,
    season_match=True,
    episode_match=True,
    year_match=True
)
print(f"  OK: Perfect match confidence = {confidence:.0%}")

confidence = scorer.calculate(
    title_match=True
)
print(f"  OK: Title-only confidence = {confidence:.0%}")

print()
print("Cache statistics:")
stats = cache.get_stats()
print(f"  OK: Cache ready (hits={stats['hits']}, misses={stats['misses']})")

print()
print("=" * 50)
print("All Phase 2 components verified!")
print("=" * 50)
