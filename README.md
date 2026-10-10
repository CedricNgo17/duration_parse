# Duration Parse

Parse human-readable durations like `2h30m` and render them back readably.

```python
from duration_parse import parse_duration, Duration

# Parse a duration string
d = parse_duration("2h30m")
print(d.seconds)   # 9000

# Render a duration back to a string
print(str(d))      # "2h30m"
```

## Why this library exists

Durations appear in configuration files, CLI arguments, and APIs, but Python's
standard library has no direct parser for strings like `1d12h`. This library
fills that gap with a tiny, dependency-free API. It stores durations as integer
seconds, which avoids floating point drift and makes equality checks trivial.

The main trade-off is that the supported unit set is deliberately small:
seconds, minutes, hours, days, and weeks. Months and years are not included
because their lengths vary; adding them would require a calendar reference and
introduce ambiguity.

## Edge cases

- The parser accepts an optional leading sign (`-` or `+`) and rejects anything
  else, including empty strings, whitespace, unknown units, and missing numbers.
- Rendering never emits zero-valued units; `Duration(3600)` renders as `1h`,
  not `1h0m0s`.
- Round-tripping works for all valid inputs: `str(parse_duration(x)) == x`
  when `x` is already in canonical form.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Contributing

Issues and pull requests are welcome. Please keep the dependency list empty —
that constraint is the point of the project, not an oversight.

