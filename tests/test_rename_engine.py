"""Tests for the RenameEngine module."""

import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mediaforge.match_result import MatchResult, MatchProvider
from src.mediaforge.rename_engine import RenameEngine
from src.mediaforge.models import MediaType
from src.mediaforge.matcher import AdvancedMatcher


def test_plan_generation_anime():
    """Test plan generation for anime media type."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        matches = []
        for episode in range(1, 6):
            source_file = tmpdir / "source" / f"Beast Tamer - S01E{episode:02d}.mkv"
            source_file.parent.mkdir(parents=True, exist_ok=True)
            source_file.touch()
            matches.append(
                MatchResult(
                    source_path=source_file,
                    filename=source_file.name,
                    provider=MatchProvider.TMDB,
                    confidence=0.95,
                    title="Beast Tamer",
                    series_name="Beast Tamer",
                    season=1,
                    episode=episode,
                    episode_title="Meeting of Fate" if episode == 1 else None,
                )
            )

        engine = RenameEngine()
        dest_root = tmpdir / "output"

        plan = engine.plan_operations(
            matches=matches,
            media_type=MediaType.ANIME,
            destination_root=dest_root,
            operation_type="rename_copy",
        )

        print("[PASS] Anime plan generation:")
        print(f"  Operations: {len(plan.operations)}")
        print(f"  Folders to create: {len(plan.folders_to_create)}")

        op = plan.operations[0]
        print(f"  Destination: {op.destination_path}")

        assert "Beast Tamer" in str(op.destination_path)
        assert "Season 01" in str(op.destination_path)
        assert "Anime" not in str(op.destination_path)
        assert "Meeting of Fate" in str(op.destination_path.name)
        print("  [OK] Correct Series/Season folder structure")


def test_plan_generation_tv():
    """Test plan generation for TV show media type."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "source" / "Breaking Bad - S01E01.mkv"
        source_file.parent.mkdir()
        source_file.touch()
        
        match = MatchResult(
            source_path=source_file,
            filename=source_file.name,
            provider=MatchProvider.OFFLINE,
            confidence=0.90,
            title="Breaking Bad",
            season=1,
            episode=1,
        )
        
        engine = RenameEngine()
        dest_root = tmpdir / "output"
        
        plan = engine.plan_operations(
            matches=[match],
            media_type=MediaType.TV_SHOW,
            destination_root=dest_root,
            operation_type="rename_copy",
        )
        
        print("\n[PASS] TV Show plan generation:")
        op = plan.operations[0]
        print(f"  Destination: {op.destination_path}")
        
        assert "Breaking Bad" in str(op.destination_path)
        assert "Season 01" in str(op.destination_path)
        assert "TV Shows" not in str(op.destination_path)
        print("  [OK] Correct TV show structure")


def test_plan_generation_movie():
    """Test plan generation for movie media type."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "source" / "Inception.mkv"
        source_file.parent.mkdir()
        source_file.touch()
        
        match = MatchResult(
            source_path=source_file,
            filename=source_file.name,
            provider=MatchProvider.OFFLINE,
            confidence=0.95,
            title="Inception",
            year=2010,
        )
        
        engine = RenameEngine()
        dest_root = tmpdir / "output"
        
        plan = engine.plan_operations(
            matches=[match],
            media_type=MediaType.MOVIE,
            destination_root=dest_root,
            operation_type="rename_copy",
        )
        
        print("\n[PASS] Movie plan generation:")
        op = plan.operations[0]
        print(f"  Destination: {op.destination_path}")
        
        assert "Movies" not in str(op.destination_path)
        assert "Inception" in str(op.destination_path)
        assert "2010" in str(op.destination_path.name)
        print("  [OK] Correct movie structure with year")


def test_dry_run():
    """Test dry run (no files created)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "source" / "test.mkv"
        source_file.parent.mkdir()
        source_file.write_text("dummy")
        
        match = MatchResult(
            source_path=source_file,
            filename=source_file.name,
            provider=MatchProvider.OFFLINE,
            confidence=0.95,
            title="Test",
        )
        
        engine = RenameEngine()
        dest_root = tmpdir / "output"
        
        plan = engine.plan_operations(
            matches=[match],
            media_type=MediaType.OTHER,
            destination_root=dest_root,
            operation_type="rename_copy",
            is_dry_run=True,
        )
        
        result = engine.execute_plan(plan)
        
        print("\n[PASS] Dry run test:")
        print(f"  Files skipped: {len(result.skipped)}")
        print(f"  Output folder created: {dest_root.exists()}")
        
        assert len(result.skipped) == 1
        assert not dest_root.exists()
        print("  [OK] Dry run made no changes")


def test_batch_with_failures():
    """Test batch operation continues after failures."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Valid file
        source1 = tmpdir / "source" / "valid.mkv"
        source1.parent.mkdir()
        source1.write_text("dummy")
        
        # Missing file
        source2 = Path(tmpdir / "source" / "missing.mkv")
        
        matches = [
            MatchResult(
                source_path=source1,
                filename=source1.name,
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="Valid",
            ),
            MatchResult(
                source_path=source2,
                filename=source2.name,
                provider=MatchProvider.OFFLINE,
                confidence=0.95,
                title="Missing",
            ),
        ]
        
        engine = RenameEngine()
        dest_root = tmpdir / "output"
        
        plan = engine.plan_operations(
            matches=matches,
            media_type=MediaType.OTHER,
            destination_root=dest_root,
            operation_type="rename_copy",
        )
        
        result = engine.execute_plan(plan)
        
        print("\n[PASS] Batch error recovery test:")
        print(f"  Successful: {len(result.successful)}")
        print(f"  Failed: {len(result.failed)}")
        
        # Should continue after first failure
        assert len(result.successful) + len(result.failed) == 2
        assert len(result.failed) >= 1
        print("  [OK] Batch continued after failure")


def test_beast_tamer_folder_normalization():
    """Ensure polluted series names do not create per-episode folders."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        engine = RenameEngine()
        dest_root = tmpdir / "fixed"
        inputs = [
            ("Beast Tamer ] Episode 01 - S01E01 - Meeting of Fate.mkv", 1, "Meeting of Fate"),
            ("Beast Tamer ] Episode 02 - S01E02 - Comrades.mkv", 2, "Comrades"),
            ("Beast Tamer ] Episode 03 - S01E03 - Another Ultimate Species.mkv", 3, "Another Ultimate Species"),
        ]

        matches = []
        for filename, episode, episode_title in inputs:
            source_file = tmpdir / "source" / filename
            source_file.parent.mkdir(parents=True, exist_ok=True)
            source_file.touch()
            matches.append(
                MatchResult(
                    source_path=source_file,
                    filename=filename,
                    provider=MatchProvider.OFFLINE,
                    confidence=0.90,
                    title=filename.replace(".mkv", ""),
                    series_name=filename.replace(".mkv", ""),
                    season=1,
                    episode=episode,
                    episode_title=episode_title,
                )
            )

        plan = engine.plan_operations(
            matches=matches,
            media_type=MediaType.ANIME,
            destination_root=dest_root,
            operation_type="rename_copy",
        )

        folders = {str(op.destination_path.parent) for op in plan.operations}
        assert folders == {str(dest_root / "Beast Tamer" / "Season 01")}
        expected_names = {
            "Beast Tamer - S01E01 - Meeting of Fate.mkv",
            "Beast Tamer - S01E02 - Comrades.mkv",
            "Beast Tamer - S01E03 - Another Ultimate Species.mkv",
        }
        assert {op.destination_path.name for op in plan.operations} == expected_names
        print("\n[PASS] Beast Tamer normalization test")


def test_monster_musume_numbered_files():
    """Ensure numbered anime files map to one series/season folder."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        engine = RenameEngine()
        dest_root = tmpdir / "fixed"
        matches = []
        for episode in [1, 2]:
            filename = f"Monster Musume no Oishasan - {episode:02d}.mkv"
            source_file = tmpdir / "source" / filename
            source_file.parent.mkdir(parents=True, exist_ok=True)
            source_file.touch()
            matches.append(
                MatchResult(
                    source_path=source_file,
                    filename=filename,
                    provider=MatchProvider.OFFLINE,
                    confidence=0.85,
                    title=filename.replace(".mkv", ""),
                    series_name=filename.replace(".mkv", ""),
                    season=1,
                    episode=episode,
                )
            )

        plan = engine.plan_operations(
            matches=matches,
            media_type=MediaType.ANIME,
            destination_root=dest_root,
            operation_type="rename_copy",
        )

        folders = {str(op.destination_path.parent) for op in plan.operations}
        assert folders == {str(dest_root / "Monster Musume No Oishasan" / "Season 01")}
        expected_names = {
            "Monster Musume No Oishasan - S01E01.mkv",
            "Monster Musume No Oishasan - S01E02.mkv",
        }
        assert {op.destination_path.name for op in plan.operations} == expected_names
        print("[PASS] Monster Musume normalization test")


def _plan_from_raw_filenames(tmpdir, filenames):
    """Build a plan the same way the app does: parse each raw filename with
    AdvancedMatcher (no pre-cleaned title/season/episode supplied), then run
    it through RenameEngine. Exercises the real end-to-end path so a
    regression in either matcher.py or rename_engine.py is caught."""
    matcher = AdvancedMatcher()
    engine = RenameEngine()
    dest_root = tmpdir / "output"

    matches = []
    for filename in filenames:
        source_file = tmpdir / "source" / filename
        source_file.parent.mkdir(parents=True, exist_ok=True)
        source_file.touch()
        parsed = matcher.parse_filename(filename) or {}
        matches.append(
            MatchResult(
                source_path=source_file,
                filename=filename,
                provider=MatchProvider.OFFLINE,
                confidence=parsed.get("confidence", 0.5),
                title=parsed.get("title"),
                series_name=parsed.get("title"),
                season=parsed.get("season"),
                episode=parsed.get("episode"),
                year=parsed.get("year"),
            )
        )

    plan = engine.plan_operations(
        matches=matches,
        media_type=MediaType.TV_SHOW,
        destination_root=dest_root,
        operation_type="rename_copy",
    )
    return plan


def test_season_two_dot_separated_no_dash():
    """Regression test: dot-separated season 2+ filenames (no dash before
    the episode title, e.g. scene-release style) must not glue the episode
    title onto the series name/folder. Previously "Breaking.Bad.S02E05.
    Buyout.720p.mkv" produced folder "Breaking Bad Buyout" instead of
    "Breaking Bad"."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        plan = _plan_from_raw_filenames(
            tmpdir,
            [
                "Breaking.Bad.S01E05.Free.Money.720p.mkv",
                "Breaking.Bad.S02E05.Buyout.720p.mkv",
            ],
        )

        folders = {str(op.destination_path.parent) for op in plan.operations}
        assert folders == {
            str(tmpdir / "output" / "Breaking Bad" / "Season 01"),
            str(tmpdir / "output" / "Breaking Bad" / "Season 02"),
        }
        print("\n[PASS] Season 2 dot-separated (no dash) normalization test")


def test_season_two_space_separated_no_dash():
    """Regression test: space-separated season 2+ filenames with no dash
    (e.g. "Show Name S02E05 Episode Title.mkv") must resolve to the plain
    series name/folder, not the series name with the episode title glued
    on."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        plan = _plan_from_raw_filenames(
            tmpdir,
            [
                "Show Name S01E01 Pilot Episode.mkv",
                "Show Name S02E05 Episode Title.mkv",
            ],
        )

        folders = {str(op.destination_path.parent) for op in plan.operations}
        assert folders == {
            str(tmpdir / "output" / "Show Name" / "Season 01"),
            str(tmpdir / "output" / "Show Name" / "Season 02"),
        }
        print("[PASS] Season 2 space-separated (no dash) normalization test")


def test_standalone_season_marker_not_fused_with_episode():
    """Regression test (found via a real operations.json log): anime that
    resets episode numbering per season is often released as
    "Show Title S2 - 01.mkv" - a standalone season marker separate from
    the bare trailing episode number, rather than "S02E01". Previously
    this always defaulted to Season 01 (regardless of the "S2") and even
    corrupted the title with a stray trailing "S". Both season 1 (no
    marker) and season 2 files must land under the same series folder,
    in their respective season subfolders, with a clean series name and
    no extra junk appended to the filename."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        plan = _plan_from_raw_filenames(
            tmpdir,
            [
                "Tsue to Tsurugi no Wistoria - 01.mkv",
                "Tsue to Tsurugi no Wistoria S2 - 01.mkv",
                "Tsue to Tsurugi no Wistoria S2 - 07.mkv",
            ],
        )

        folders = {str(op.destination_path.parent) for op in plan.operations}
        assert folders == {
            str(tmpdir / "output" / "Tsue to Tsurugi No Wistoria" / "Season 01"),
            str(tmpdir / "output" / "Tsue to Tsurugi No Wistoria" / "Season 02"),
        }
        names = {op.destination_path.name for op in plan.operations}
        assert names == {
            "Tsue to Tsurugi No Wistoria - S01E01.mkv",
            "Tsue to Tsurugi No Wistoria - S02E01.mkv",
            "Tsue to Tsurugi No Wistoria - S02E07.mkv",
        }
        print("[PASS] Standalone season marker (S2) normalization test")


def test_mid_position_bare_episode_number():
    """Regression test (found via a real operations.json log): anime
    numbered as "Title - 01 - Episode Title.mkv" (bare episode number in
    the middle, not at the end of the filename) was not recognized as
    having any season/episode info at all, since bare_number requires the
    number to be the very last token. This meant no Season folder was
    created and no SxxExx tag was added to the output filename, even
    though the episode title itself was still (coincidentally) extracted
    correctly by a separate regex."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        plan = _plan_from_raw_filenames(
            tmpdir,
            [
                "Am I Actually the Strongest - 01 - Starting at Rock Bottom After Reincarnation.mkv",
                "Am I Actually the Strongest - 02 - Char Hates Me.mkv",
            ],
        )

        folders = {str(op.destination_path.parent) for op in plan.operations}
        assert folders == {
            str(tmpdir / "output" / "Am I Actually the Strongest" / "Season 01"),
        }
        names = {op.destination_path.name for op in plan.operations}
        assert names == {
            "Am I Actually the Strongest - S01E01 - Starting At Rock Bottom After Reincarnation.mkv",
            "Am I Actually the Strongest - S01E02 - Char Hates Me.mkv",
        }
        print("[PASS] Mid-position bare episode number test")


def test_scoring_rejects_unrelated_candidate():
    """Regression test: a completely unrelated candidate title (simulating
    a fuzzy online search returning the wrong show) must not reach a
    comfortable confidence score just because the source filename happens
    to contain a parseable season/episode number. Previously
    season_match/episode_match/has_episode_info applied unconditionally,
    letting an unrelated candidate score 0.5+ ("Needs Review" or higher)
    purely from the query's own metadata, regardless of title similarity."""
    from src.mediaforge.providers.scoring import ConfidenceScorer, fuzzy_match

    scorer = ConfidenceScorer()
    query = "Am I Actually the Strongest - 01 - Starting at Rock Bottom After Reincarnation.mkv"

    wrong_ratio = fuzzy_match("Cowboy Bebop", query)
    wrong_confidence = scorer.calculate(
        title_match=wrong_ratio > 0.95,
        title_fuzzy_ratio=wrong_ratio if wrong_ratio <= 0.95 else None,
        season_match=True,
        episode_match=True,
        has_episode_info=True,
    )
    assert wrong_confidence < 0.5, f"unrelated candidate scored too high: {wrong_confidence}"

    right_ratio = fuzzy_match("Am I Actually the Strongest?", query)
    right_confidence = scorer.calculate(
        title_match=right_ratio > 0.95,
        title_fuzzy_ratio=right_ratio if right_ratio <= 0.95 else None,
        season_match=True,
        episode_match=True,
        has_episode_info=True,
    )
    assert right_confidence >= 0.5, f"correct candidate scored too low: {right_confidence}"
    print("[PASS] Scoring rejects unrelated candidate test")


def test_ordinal_season_phrasing():
    """Regression test (found via FileBot comparison): "2nd Season"/"3rd
    Season" ordinal phrasing - common in official anime titles - must be
    recognized the same way "S2"/"Season 2" already are, instead of
    defaulting to Season 01."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        plan = _plan_from_raw_filenames(
            tmpdir,
            [
                "Jujutsu Kaisen 2nd Season - 05.mkv",
                "Jujutsu Kaisen - 05.mkv",
            ],
        )

        folders = {str(op.destination_path.parent) for op in plan.operations}
        assert folders == {
            str(tmpdir / "output" / "Jujutsu Kaisen" / "Season 01"),
            str(tmpdir / "output" / "Jujutsu Kaisen" / "Season 02"),
        }
        print("[PASS] Ordinal season phrasing test")


def test_disambiguator_preserved():
    """Regression test (found via FileBot comparison): a trailing
    region/disambiguator marker like "(US)"/"(UK)" must survive series
    name normalization intact, instead of being mangled into "Us"/"Uk" by
    the blanket bracket-stripping step - otherwise "The Office (US)" and
    "The Office (UK)" would collide into the same folder."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        plan = _plan_from_raw_filenames(
            tmpdir,
            [
                "The Office (US) - 3x05.mkv",
                "Being Human (UK) - S02E01.mkv",
                "Show Name (1080p) - S01E01.mkv",
            ],
        )

        folders = {str(op.destination_path.parent) for op in plan.operations}
        assert folders == {
            str(tmpdir / "output" / "The Office (US)" / "Season 03"),
            str(tmpdir / "output" / "Being Human (UK)" / "Season 02"),
            str(tmpdir / "output" / "Show Name" / "Season 01"),
        }
        print("[PASS] Disambiguator preservation test")


def test_absolute_episode_conversion():
    """Regression test: a bare episode number with no season marker at
    all (e.g. "Example Show - 23", simulating long-running anime numbered
    absolutely rather than per-season, like One Piece) must be converted
    to the correct season/episode using the matched show's real
    per-season episode counts - mirroring FileBot's TheTVDB-backed
    behavior confirmed by direct comparison. Season 0 (specials) must be
    excluded from the conversion."""
    from unittest.mock import patch, MagicMock
    from src.mediaforge.providers.tmdb_provider import TMDBProvider

    provider = TMDBProvider()

    fake_response = MagicMock()
    fake_response.raise_for_status = lambda: None
    fake_response.json = lambda: {
        "seasons": [
            {"season_number": 0, "episode_count": 5},
            {"season_number": 1, "episode_count": 10},
            {"season_number": 2, "episode_count": 12},
            {"season_number": 3, "episode_count": 8},
        ]
    }
    item = {"id": 12345, "name": "Example Show", "first_air_date": "2020-01-01"}

    with patch("src.mediaforge.providers.tmdb_provider.requests.get", return_value=fake_response):
        match = provider._build_tv_match(item, "Example Show - 23.mkv", api_key="fake-key")

    assert match.season == 3, f"expected season 3, got {match.season}"
    assert match.episode == 1, f"expected episode 1, got {match.episode}"

    # An explicit SxxExx marker must never be overridden by this - it's
    # not ambiguous, so the absolute-conversion path must not run at all.
    with patch("src.mediaforge.providers.tmdb_provider.requests.get", return_value=fake_response):
        explicit_match = provider._build_tv_match(item, "Example Show - S01E05.mkv", api_key="fake-key")
    assert explicit_match.season == 1 and explicit_match.episode == 5
    print("[PASS] Absolute episode conversion test")


if __name__ == "__main__":
    test_plan_generation_anime()
    test_plan_generation_tv()
    test_plan_generation_movie()
    test_dry_run()
    test_batch_with_failures()
    test_beast_tamer_folder_normalization()
    test_monster_musume_numbered_files()
    test_season_two_dot_separated_no_dash()
    test_season_two_space_separated_no_dash()
    test_standalone_season_marker_not_fused_with_episode()
    test_mid_position_bare_episode_number()
    test_scoring_rejects_unrelated_candidate()
    test_ordinal_season_phrasing()
    test_disambiguator_preserved()
    test_absolute_episode_conversion()
    print("\n[SUCCESS] All tests passed!")
