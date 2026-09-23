"""Tests for the duration_parse package."""

import unittest

from duration_parse import Duration, parse_duration


class ParseDurationTests(unittest.TestCase):
    def test_parses_seconds(self):
        self.assertEqual(parse_duration("30s"), Duration(30))

    def test_parses_minutes(self):
        self.assertEqual(parse_duration("5m"), Duration(300))

    def test_parses_hours(self):
        self.assertEqual(parse_duration("2h"), Duration(7200))

    def test_parses_compound_durations(self):
        self.assertEqual(parse_duration("2h30m"), Duration(9000))

    def test_parses_multiple_units(self):
        self.assertEqual(parse_duration("1d2h3m4s"), Duration(93784))

    def test_parses_weeks(self):
        self.assertEqual(parse_duration("1w"), Duration(604800))

    def test_parses_negative_duration(self):
        self.assertEqual(parse_duration("-45s"), Duration(-45))

    def test_parses_positive_sign(self):
        self.assertEqual(parse_duration("+10m"), Duration(600))

    def test_parses_case_insensitive_units(self):
        self.assertEqual(parse_duration("2H30M"), Duration(9000))

    def test_rejects_empty_string(self):
        with self.assertRaises(ValueError):
            parse_duration("")

    def test_rejects_whitespace_only(self):
        with self.assertRaises(ValueError):
            parse_duration("   ")

    def test_rejects_missing_unit(self):
        with self.assertRaises(ValueError):
            parse_duration("10")

    def test_rejects_missing_number(self):
        with self.assertRaises(ValueError):
            parse_duration("h")

    def test_rejects_unknown_unit(self):
        with self.assertRaises(ValueError):
            parse_duration("10x")

    def test_rejects_trailing_garbage(self):
        with self.assertRaises(ValueError):
            parse_duration("10sfoo")

    def test_rejects_leading_garbage(self):
        with self.assertRaises(ValueError):
            parse_duration("foo10s")

    def test_rejects_non_string_input(self):
        with self.assertRaises(TypeError):
            parse_duration(42)  # type: ignore[arg-type]


class DurationRenderTests(unittest.TestCase):
    def test_renders_zero(self):
        self.assertEqual(str(Duration(0)), "0s")

    def test_renders_seconds_only(self):
        self.assertEqual(str(Duration(45)), "45s")

    def test_renders_minutes_and_seconds(self):
        self.assertEqual(str(Duration(90)), "1m30s")

    def test_renders_hours_and_minutes(self):
        self.assertEqual(str(Duration(9000)), "2h30m")

    def test_renders_days(self):
        self.assertEqual(str(Duration(86400)), "1d")

    def test_renders_weeks(self):
        self.assertEqual(str(Duration(604800)), "1w")

    def test_renders_compound(self):
        self.assertEqual(str(Duration(93784)), "1d2h3m4s")

    def test_renders_negative(self):
        self.assertEqual(str(Duration(-45)), "-45s")

    def test_renders_negative_compound(self):
        self.assertEqual(str(Duration(-9000)), "-2h30m")

    def test_renders_does_not_use_zero_units(self):
        # Only units that contribute should appear.
        self.assertEqual(str(Duration(3600)), "1h")


class RoundTripTests(unittest.TestCase):
    def test_parse_then_render(self):
        original = "2h30m"
        parsed = parse_duration(original)
        self.assertEqual(str(parsed), original)

    def test_render_then_parse(self):
        duration = Duration(93784)
        rendered = str(duration)
        self.assertEqual(parse_duration(rendered), duration)


if __name__ == "__main__":
    unittest.main()
