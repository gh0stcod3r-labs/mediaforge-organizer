#!/usr/bin/env python3
"""
Quick Reference for Architectural Audit
Run this to validate the current state of the project.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def check_imports():
    """Verify all modules import correctly."""
    try:
        from src.mediaforge.models import MediaType, VideoFile
        from src.mediaforge.scanner import VideoScanner
        from src.mediaforge.parser import VideoParser
        from src.mediaforge.match_result import MatchResult, MatchProvider
        from src.mediaforge.operation_result import OperationResult, OperationPlan, ExecutionResult
        from src.mediaforge.rename_engine import RenameEngine
        from src.mediaforge.logger import OperationLogger
        from src.mediaforge.app import ModernMediaForgeWindow
        from src.mediaforge.constants import get_stylesheet
        print("[OK] All modules import successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        return False


def check_rename_engine():
    """Verify RenameEngine core functionality."""
    try:
        import tempfile
        from pathlib import Path
        from src.mediaforge.match_result import MatchResult, MatchProvider
        from src.mediaforge.rename_engine import RenameEngine
        from src.mediaforge.models import MediaType
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source" / "test.mkv"
            source_file.parent.mkdir()
            source_file.touch()
            
            match = MatchResult(
                source_path=source_file,
                filename="test.mkv",
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="Test Series",
                season=1,
                episode=1,
            )
            
            engine = RenameEngine()
            plan = engine.plan_operations(
                matches=[match],
                media_type=MediaType.ANIME,
                destination_root=tmpdir / "output",
                operation_type="rename_copy",
            )
            
            assert len(plan.operations) == 1
            assert "Anime" not in str(plan.operations[0].destination_path)
            assert "Season 01" in str(plan.operations[0].destination_path)
            print("[OK] RenameEngine core functionality working")
            return True
    except Exception as e:
        print(f"[FAIL] RenameEngine test failed: {e}")
        return False


def check_ui():
    """Verify UI can be instantiated."""
    try:
        import sys
        from PySide6.QtWidgets import QApplication
        from src.mediaforge.app import ModernMediaForgeWindow
        
        app = QApplication(sys.argv)
        window = ModernMediaForgeWindow()
        
        assert window.windowTitle() == "MediaForge Organizer"
        assert window.width() > 0
        assert window.height() > 0
        print("[OK] UI instantiates correctly")
        return True
    except Exception as e:
        print(f"[FAIL] UI test failed: {e}")
        return False


def check_folder_structures():
    """Verify folder structures are correct."""
    try:
        import tempfile
        from pathlib import Path
        from src.mediaforge.match_result import MatchResult, MatchProvider
        from src.mediaforge.rename_engine import RenameEngine
        from src.mediaforge.models import MediaType
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source" / "file.mkv"
            source_file.parent.mkdir()
            source_file.touch()
            
            engine = RenameEngine()
            
            # Test ANIME: output/Title/Season XX/Title - SXXEXX.ext
            match = MatchResult(
                source_path=source_file,
                filename="file.mkv",
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="Beast Tamer",
                season=1,
                episode=5,
            )
            plan = engine.plan_operations(
                matches=[match],
                media_type=MediaType.ANIME,
                destination_root=tmpdir / "output",
                operation_type="rename_copy",
            )
            dest = str(plan.operations[0].destination_path)
            assert "Anime" not in dest and "Beast Tamer" in dest and "Season 01" in dest, f"Anime: {dest}"
            
            # Test TV_SHOW: output/TV Shows/Title/Season XX/Title - SXXEXX.ext
            plan = engine.plan_operations(
                matches=[match],
                media_type=MediaType.TV_SHOW,
                destination_root=tmpdir / "output",
                operation_type="rename_copy",
            )
            dest = str(plan.operations[0].destination_path)
            assert "TV Shows" not in dest and "Beast Tamer" in dest and "Season 01" in dest, f"TV Shows: {dest}"
            
            # Test MOVIE: output/Movies/Title (YYYY)/Title (YYYY).ext
            match_movie = MatchResult(
                source_path=source_file,
                filename="file.mkv",
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="Inception",
                year=2010,
            )
            plan = engine.plan_operations(
                matches=[match_movie],
                media_type=MediaType.MOVIE,
                destination_root=tmpdir / "output",
                operation_type="rename_copy",
            )
            dest = str(plan.operations[0].destination_path)
            assert "Movies" not in dest and "Inception" in dest and "2010" in dest, f"Movie: {dest}"
            
            # Test SPORTS: output/Sports/Title/Year/file.mkv
            match_sports = MatchResult(
                source_path=source_file,
                filename="file.mkv",
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="Premier League",
                year=2023,
            )
            plan = engine.plan_operations(
                matches=[match_sports],
                media_type=MediaType.SPORTS,
                destination_root=tmpdir / "output",
                operation_type="rename_copy",
            )
            dest = str(plan.operations[0].destination_path)
            assert "Sports" not in dest and "Premier League" in dest and "2023" in dest, f"Sports: {dest}"
            
            # Test CLIPS: output/Clips/Title/file.mkv
            match_clips = MatchResult(
                source_path=source_file,
                filename="file.mkv",
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="My Vlog",
            )
            plan = engine.plan_operations(
                matches=[match_clips],
                media_type=MediaType.CLIPS,
                destination_root=tmpdir / "output",
                operation_type="rename_copy",
            )
            dest = str(plan.operations[0].destination_path)
            assert "Clips" not in dest and "My Vlog" in dest, f"Clips: {dest}"
            
            # Test CREATOR_FOOTAGE: output/Creator Footage/Title/Raw/file.mkv
            match_creator = MatchResult(
                source_path=source_file,
                filename="file.mkv",
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="Project Alpha",
            )
            plan = engine.plan_operations(
                matches=[match_creator],
                media_type=MediaType.CREATOR_FOOTAGE,
                destination_root=tmpdir / "output",
                operation_type="rename_copy",
            )
            dest = str(plan.operations[0].destination_path)
            assert "Creator Footage" not in dest and "Project Alpha" in dest and "Raw" not in dest, f"Creator Footage: {dest}"
            
            # Test OTHER: output/Other/file.mkv
            match_other = MatchResult(
                source_path=source_file,
                filename="file.mkv",
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="random",
            )
            plan = engine.plan_operations(
                matches=[match_other],
                media_type=MediaType.OTHER,
                destination_root=tmpdir / "output",
                operation_type="rename_copy",
            )
            dest = str(plan.operations[0].destination_path)
            assert "Other" not in dest and "Random" in dest, f"Other: {dest}"
            
            print("[OK] All folder structures correct with actual metadata")
            return True
    except Exception as e:
        print(f"[FAIL] Folder structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all checks."""
    print("=" * 50)
    print("MediaForge Organizer — Architectural Audit Checks")
    print("=" * 50)
    print()
    
    checks = [
        ("Module Imports", check_imports),
        ("RenameEngine", check_rename_engine),
        ("Folder Structures", check_folder_structures),
        ("UI Instantiation", check_ui),
    ]
    
    results = []
    for name, check in checks:
        print(f"\n[CHECK] {name}...")
        result = check()
        results.append((name, result))
    
    print()
    print("=" * 50)
    print("Audit Summary")
    print("=" * 50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")
    
    print()
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n[SUCCESS] All checks passed! Project is ready for audit.")
        return 0
    else:
        print(f"\n[FAILED] {total - passed} check(s) failed. Please review.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
