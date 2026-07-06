"""Advanced filename matching and parsing."""

import re
from typing import Optional, Dict, Any
from pathlib import Path


class AdvancedMatcher:
    """Parse complex filenames to extract metadata."""
    
    # Common patterns for episode numbering
    PATTERNS = {
        # S01E01 format
        "s_e_format": re.compile(r's(\d{1,2})e(\d{1,2})', re.IGNORECASE),
        
        # 1x01 format
        "x_format": re.compile(r'(\d{1,2})x(\d{1,2})', re.IGNORECASE),
        
        # Episode 01 format
        "ep_format": re.compile(r'(?:episode|ep|ep\.)\s*(\d{1,3})', re.IGNORECASE),
        
        # Bare trailing episode number: "Title - 01" (common simple anime numbering,
        # no season/episode keyword at all). Anchored to end of string and requires
        # a dash separator so it doesn't misfire on years, resolutions, or other
        # embedded numbers - those are handled by more specific patterns above.
        "bare_number": re.compile(r'-\s*(\d{1,3})\s*$'),

        # Same simple anime numbering as bare_number, but with an episode
        # title trailing afterwards instead of the number being the very
        # last token, e.g. "Title - 01 - Episode Title.mkv".
        "bare_number_mid": re.compile(r'-\s*(\d{1,3})\s*-'),

        # Standalone season marker not fused with an episode number, e.g.
        # "Show S2 - 01", "Show Season 2 - 01", or "Show 2nd Season - 01"
        # (ordinal phrasing is common in official/CR-style anime titles).
        # Many second-season anime releases reset episode numbering per
        # season instead of using SxxExx, so the season lives here instead
        # of in s_e_format/x_format.
        "season_only": re.compile(
            r'\bseason\s*(?P<season1>\d{1,2})\b'
            r'|\b(?P<season2>\d{1,2})(?:st|nd|rd|th)\s*season\b'
            r'|\bs(?P<season3>\d{1,2})\b',
            re.IGNORECASE,
        ),

        # Year in brackets or parentheses
        "year": re.compile(r'\((\d{4})\)|\[(\d{4})\]'),
        
        # Fansub/release group [Name]
        "fansub": re.compile(r'\[([^\]]+)\]'),
        
        # Resolution tags
        "resolution": re.compile(r'(480p|720p|1080p|2160p|4k|uhd)', re.IGNORECASE),
        
        # Codec tags
        "codec": re.compile(r'(x264|x265|h\.?264|h\.?265|hevc|avc)', re.IGNORECASE),
        
        # Audio tags
        "audio": re.compile(r'(aac|ac3|dts|flac|opus|vorbis)', re.IGNORECASE),
        
        # Quality indicators
        "quality": re.compile(r'(dvdrip|bdrip|webrip|hdtv|web-dl|bluray)', re.IGNORECASE),
        
        # Subtitle tags
        "subtitle": re.compile(r'(subbed|dubbed|dual audio)', re.IGNORECASE),
    }
    
    def parse_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """Parse filename to extract metadata.
        
        Args:
            filename: Filename to parse (can include path)
            
        Returns:
            Dict with title, season, episode, year, confidence, or None
        """
        # Remove extension
        if isinstance(filename, (str, Path)):
            filename_clean = Path(filename).stem
        else:
            filename_clean = filename
        
        # Remove common junk patterns first
        working_str = self._remove_junk(filename_clean)
        
        # Extract episode info
        season, episode, season_explicit = self._extract_episode_info(working_str)

        # Extract year
        year = self._extract_year(working_str)

        # Clean title (remove tags and numbers)
        title = self._extract_title(working_str, season, episode, year)

        if not title:
            return None

        # Calculate confidence
        confidence = self._calculate_confidence(season, episode, year)

        return {
            "title": title,
            "season": season,
            "episode": episode,
            "year": year,
            "confidence": confidence,
            # False when season was defaulted to 1 with no marker present at
            # all (a bare episode number like "Title - 45") rather than
            # found explicitly (SxxExx, NxNN, "S2"/"Season 2"/"2nd Season").
            # Lets providers know when a bare number might actually be an
            # absolute episode count instead of a per-season one.
            "season_explicit": season_explicit,
        }
    
    def _remove_junk(self, s: str) -> str:
        """Remove common junk patterns."""
        # Remove resolution, codec, audio, quality tags
        for pattern in [
            self.PATTERNS["resolution"],
            self.PATTERNS["codec"],
            self.PATTERNS["audio"],
            self.PATTERNS["quality"],
            self.PATTERNS["subtitle"],
        ]:
            s = pattern.sub("", s)
        
        # Remove fansub tags [Group Name]
        s = self.PATTERNS["fansub"].sub("", s)
        
        # Remove version tags like v2, v3
        s = re.sub(r'\bv\d+\b', "", s, flags=re.IGNORECASE)
        
        # Remove extra spaces
        s = re.sub(r'\s+', " ", s).strip()
        
        return s
    
    def _extract_episode_info(self, s: str) -> tuple[Optional[int], Optional[int], bool]:
        """Extract season and episode numbers.

        Returns (season, episode, season_explicit) - season_explicit is
        False whenever season had to be defaulted to 1 with no marker
        present at all, so callers can tell a genuine "season 1" apart
        from "we have no idea, so we guessed 1".
        """
        season = None
        episode = None

        # Try S01E01 format
        match = self.PATTERNS["s_e_format"].search(s)
        if match:
            season = int(match.group(1))
            episode = int(match.group(2))
            return season, episode, True

        # Try 1x01 format
        match = self.PATTERNS["x_format"].search(s)
        if match:
            season = int(match.group(1))
            episode = int(match.group(2))
            return season, episode, True

        # A standalone season marker (e.g. "S2", "Season 2") separate from
        # the episode number - used as a fallback below rather than always
        # defaulting to season 1.
        season_match = self.PATTERNS["season_only"].search(s)
        season_from_marker = None
        if season_match:
            season_from_marker = int(
                season_match.group("season1")
                or season_match.group("season2")
                or season_match.group("season3")
            )

        # Try Episode format
        match = self.PATTERNS["ep_format"].search(s)
        if match:
            episode = int(match.group(1))
            season = season_from_marker if season_from_marker is not None else 1
            return season, episode, season_from_marker is not None

        # Try bare number sandwiched between dashes with an episode title
        # trailing afterwards: "Title - 01 - Episode Title" (as opposed to
        # bare_number below, where the number is the very last token).
        match = self.PATTERNS["bare_number_mid"].search(s)
        if match:
            episode = int(match.group(1))
            season = season_from_marker if season_from_marker is not None else 1
            return season, episode, season_from_marker is not None

        # Try bare trailing number format: "Title - 01" (simple anime numbering
        # with no S/E or "Episode" keyword at all).
        match = self.PATTERNS["bare_number"].search(s)
        if match:
            episode = int(match.group(1))
            season = season_from_marker if season_from_marker is not None else 1
            return season, episode, season_from_marker is not None

        return None, None, False
    
    def _extract_year(self, s: str) -> Optional[int]:
        """Extract year from string."""
        match = self.PATTERNS["year"].search(s)
        if match:
            year_str = match.group(1) or match.group(2)
            try:
                year = int(year_str)
                if 1900 <= year <= 2100:
                    return year
            except (ValueError, TypeError):
                pass
        return None
    
    def _extract_title(
        self,
        s: str,
        season: Optional[int],
        episode: Optional[int],
        year: Optional[int],
    ) -> str:
        """Extract clean title.

        Truncates at the earliest season/episode/year marker rather than
        just substituting the marker text out, so trailing text (episode
        title, leftover release tags) doesn't stay glued to the series
        name when there's no dash separating them - e.g.
        "Breaking.Bad.S02E05.Buyout.720p" must yield "Breaking Bad", not
        "Breaking Bad Buyout".
        """
        working = s
        cut_at: Optional[int] = None

        def earliest(pattern) -> None:
            nonlocal cut_at
            match = pattern.search(working)
            if match and (cut_at is None or match.start() < cut_at):
                cut_at = match.start()

        if season is not None and episode is not None:
            earliest(self.PATTERNS["s_e_format"])
            earliest(self.PATTERNS["x_format"])

        if episode is not None:
            earliest(self.PATTERNS["ep_format"])
            earliest(self.PATTERNS["bare_number_mid"])
            earliest(self.PATTERNS["bare_number"])
            earliest(self.PATTERNS["season_only"])

        if year:
            earliest(re.compile(rf'\({year}\)|\[{year}\]'))

        if cut_at is not None:
            working = working[:cut_at]

        # Remove leading/trailing numbers and dashes
        working = re.sub(r'^[\d\s\-_\.]+', "", working)
        working = re.sub(r'[\d\s\-_\.]+$', "", working)
        
        # Remove extra spaces and special chars at edges
        working = re.sub(r'[\s\-_.]+', " ", working).strip()
        
        # Capitalize properly
        title = " ".join(word.capitalize() for word in working.split())
        
        return title if title else None
    
    def _calculate_confidence(
        self,
        season: Optional[int],
        episode: Optional[int],
        year: Optional[int],
    ) -> float:
        """Calculate match confidence score."""
        confidence = 0.7  # Base confidence from offline parse
        
        if season is not None:
            confidence += 0.1  # Season info
        
        if episode is not None:
            confidence += 0.1  # Episode info
        
        if year is not None:
            confidence += 0.1  # Year info
        
        return min(confidence, 1.0)
    
    def sanitize_filename(self, title: str) -> str:
        """Sanitize title for use as filename.
        
        Args:
            title: Title to sanitize
            
        Returns:
            Safe filename (no invalid characters)
        """
        # Remove invalid Windows/Unix characters
        invalid_chars = r'[<>:"/\\|?*\0]'
        sanitized = re.sub(invalid_chars, "", title)
        
        # Replace leading/trailing dots and spaces
        sanitized = sanitized.strip(". ")
        
        # Limit length
        max_len = 200  # Leave room for extensions
        if len(sanitized) > max_len:
            sanitized = sanitized[:max_len].rsplit(" ", 1)[0]
        
        return sanitized or "Unknown"
