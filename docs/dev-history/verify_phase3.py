#!/usr/bin/env python3
"""Phase 3 foundation verification tool."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_imports():
    """Verify all Phase 3 modules import correctly."""
    print("[CHECK] Phase 3 Module Imports...")
    try:
        from mediaforge.cache import get_cache, MetadataCache
        print("  [OK] cache.py - Enhanced cache system")
        
        from mediaforge.async_matcher import AsyncMatcher, BatchMatchResult
        print("  [OK] async_matcher.py - Parallel matching")
        
        from mediaforge.match_report import MatchReport
        print("  [OK] match_report.py - Match report generation")
        
        from mediaforge.logger import OperationLogger
        print("  [OK] logger.py - Enhanced with export methods")
        
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def check_cache_features():
    """Verify enhanced cache features."""
    print("\n[CHECK] Cache Features...")
    try:
        from mediaforge.cache import MetadataCache
        
        cache = MetadataCache()
        
        # Check new features
        assert hasattr(cache, 'get_cache_key'), "Missing get_cache_key()"
        print("  [OK] Smart cache key generation")
        
        assert hasattr(cache, 'cleanup_corrupted'), "Missing cleanup_corrupted()"
        print("  [OK] Corruption recovery")
        
        # Check cache operations
        cache.set("test_provider", "test_query", {"data": "value"})
        result = cache.get("test_provider", "test_query")
        assert result is not None, "Cache set/get failed"
        print("  [OK] Cache set/get operations")
        
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def check_async_matcher():
    """Verify AsyncMatcher functionality."""
    print("\n[CHECK] Async Matcher...")
    try:
        from mediaforge.async_matcher import AsyncMatcher, BatchMatchResult
        from mediaforge.providers.provider_selector import ProviderSelector
        
        matcher = AsyncMatcher(max_workers=2, timeout=10)
        
        assert hasattr(matcher, 'match_batch'), "Missing match_batch()"
        print("  [OK] match_batch() method")
        
        assert hasattr(matcher, 'match_batch_with_progress'), "Missing match_batch_with_progress()"
        print("  [OK] match_batch_with_progress() method")
        
        assert hasattr(matcher, 'cancel'), "Missing cancel() method"
        print("  [OK] cancel() method")
        
        # Test with small batch
        selector = ProviderSelector()
        test_files = ["test_file.mkv", "another_file.mp4"]
        results, attempts, completed = matcher.match_batch(test_files, selector)
        
        assert isinstance(results, list), "Invalid result type"
        print("  [OK] Returns list of results")
        
        assert isinstance(attempts, list) and len(attempts) == len(test_files), "Invalid attempts list"
        print("  [OK] Returns per-file provider attempt info")
        
        assert isinstance(completed, int), "Completed count not int"
        print("  [OK] Returns completed count")
        
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def check_match_report():
    """Verify MatchReport functionality."""
    print("\n[CHECK] Match Report...")
    try:
        from mediaforge.match_report import MatchReport
        from mediaforge.match_result import MatchResult, MatchProvider
        from pathlib import Path
        
        report = MatchReport()
        
        # Create test match
        match = MatchResult(
            source_path=Path("/tmp/test.mkv"),
            filename="test.mkv",
            provider=MatchProvider.OFFLINE,
            confidence=0.95,
            title="Test Series",
            season=1,
            episode=1
        )
        
        report.add_match(match, "OFFLINE")
        
        assert report.files_scanned == 1, "Add match failed"
        print("  [OK] add_match() method")
        
        assert hasattr(report, 'summary'), "Missing summary() method"
        summary = report.summary()
        assert len(summary) > 0, "Summary is empty"
        print("  [OK] summary() generation")
        
        assert hasattr(report, 'to_dict'), "Missing to_dict() method"
        report_dict = report.to_dict()
        assert 'files_scanned' in report_dict, "Invalid report structure"
        print("  [OK] to_dict() JSON serialization")
        
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def check_logger_export():
    """Verify OperationLogger export features."""
    print("\n[CHECK] Logger Export Features...")
    try:
        from mediaforge.logger import OperationLogger
        import tempfile
        
        logger = OperationLogger()
        
        assert hasattr(logger, 'export_csv'), "Missing export_csv()"
        print("  [OK] export_csv() method")
        
        assert hasattr(logger, 'export_json'), "Missing export_json()"
        print("  [OK] export_json() method")
        
        assert hasattr(logger, 'export_report'), "Missing export_report()"
        print("  [OK] export_report() method")
        
        # Test exports with temp files (may have empty log)
        # These methods should not crash even without operations
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "test.csv"
            json_path = Path(tmpdir) / "test.json"
            
            # Just test they don't crash
            logger.export_csv(csv_path)
            logger.export_json(json_path)
            
            print("  [OK] export_csv() executes")
            print("  [OK] export_json() executes")
        
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def check_providers_compatibility():
    """Verify Phase 2 providers still work."""
    print("\n[CHECK] Provider Compatibility...")
    try:
        from mediaforge.providers.offline_provider import OfflineProvider
        from mediaforge.providers.tmdb_provider import TMDBProvider
        from mediaforge.providers.anilist_provider import AniListProvider
        
        offline = OfflineProvider()
        assert offline.provider_name == "Offline Parser", f"Offline provider name is {offline.provider_name}"
        print("  [OK] Offline provider")
        
        tmdb = TMDBProvider()
        assert hasattr(tmdb, 'requires_api_key'), "Missing requires_api_key"
        print("  [OK] TMDB provider")
        
        anilist = AniListProvider()
        assert hasattr(anilist, 'test_connection'), "Missing test_connection"
        print("  [OK] AniList provider")
        
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 50)
    print("Phase 3 Foundation Verification")
    print("=" * 50)
    
    checks = [
        ("Module Imports", check_imports),
        ("Cache Features", check_cache_features),
        ("Async Matcher", check_async_matcher),
        ("Match Report", check_match_report),
        ("Logger Export", check_logger_export),
        ("Provider Compatibility", check_providers_compatibility),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  [ERROR] Unexpected error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("Phase 3 Verification Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")
    
    print()
    if passed == total:
        print(f"Result: {passed}/{total} checks passed")
        print("[SUCCESS] Phase 3 foundation verified! Ready for integration.")
        return 0
    else:
        print(f"Result: {passed}/{total} checks passed")
        print("[WARNING] Some checks failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
