"""Core implementation for duration parsing and rendering.

The design uses a single Duration class that stores a total number of seconds.
All parsing produces a Duration, and all rendering starts from a Duration.
This avoids floating point drift and keeps the API minimal.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


_UNIT_TO_SECONDS = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
}

# The regex must allow an optional sign at the start, then one or more
# number+unit pairs. Units are case-insensitive single letters.
# The pattern does not use anchors because we want to reject trailing garbage.
_DURATION_PATTERN = re.compile(r"^([+-]?(?:\d+[smhdw])+)$", re.IGNORECASE)
_PART_PATTERN = re.compile(r"([+-]?\d+)([smhdw])", re.IGNORECASE)


@dataclass(frozen=True)
class Duration:
    """An immutable duration stored as an integer number of seconds.

    The value is always normalised to seconds. Negative durations are
    supported and represent a point in time before the reference point.
    """

    seconds: int

    def __str__(self) -> str:
        """Render the duration in a compact human-readable form.

        The output uses the largest possible unit for the magnitude, then
        falls back to smaller units for any remainder. Zero renders as '0s'.
        The sign, if negative, is placed before the first unit.
        """
        if self.seconds == 0:
            return "0s"

        sign = "-" if self.seconds < 0 else ""
        remaining = abs(self.seconds)

        # Order matters: weeks, days, hours, minutes, seconds.
        units = [
            (604800, "w"),
            (86400, "d"),
            (3600, "h"),
            (60, "m"),
            (1, "s"),
        ]

        parts: list[str] = []
        for seconds_per_unit, suffix in units:
            if remaining >= seconds_per_unit:
                count, remaining = divmod(remaining, seconds_per_unit)
                parts.append(f"{count}{suffix}")

        return sign + "".join(parts)


def parse_duration(text: str) -> Duration:
    """Parse a duration string and return a Duration.

    Supported format: one or more number+unit pairs, optionally signed.
    Units are s, m, h, d, w (seconds, minutes, hours, days, weeks).
    Case-insensitive. Examples: '2h30m', '-45s', '1d12h', '2W'.

    Raises ValueError for malformed input, including empty strings,
    unknown units, missing numbers, and leading/trailing junk.
    """
    if not isinstance(text, str):
        raise TypeError("duration must be a string")

    text = text.strip()
    if not text:
        raise ValueError("empty duration")

    match = _DURATION_PATTERN.fullmatch(text)
    if not match:
        raise ValueError(f"invalid duration: {text!r}")

    total_seconds = 0
    for number_str, unit in _PART_PATTERN.findall(text):
        total_seconds += int(number_str) * _UNIT_TO_SECONDS[unit.lower()]

    return Duration(total_seconds)
