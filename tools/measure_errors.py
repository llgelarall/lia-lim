"""Compute unnormalized signed error metrics from CSV columns exact,approximate."""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import sys


def measure(path):
    raw = path.read_bytes()
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""))
    if not reader.fieldnames or not {"exact", "approximate"}.issubset(reader.fieldnames):
        raise ValueError("CSV must contain exact and approximate column headers")
    count = total = absolute = squared = different = 0
    minimum = maximum = None
    for line, row in enumerate(reader, 2):
        outputs = [row.get(key) for key in ("exact", "approximate")]
        if any(value is None or not re.fullmatch(r"[+-]?\d+", value.strip(), flags=re.ASCII) for value in outputs):
            raise ValueError(f"CSV row {line}: exact and approximate must be base-10 integers")
        exact, approximate = map(int, outputs)
        error = approximate - exact
        count += 1
        total += error
        absolute += abs(error)
        squared += error * error
        different += error != 0
        minimum = error if minimum is None else min(minimum, error)
        maximum = error if maximum is None else max(maximum, error)
    if not count:
        raise ValueError("CSV contains no output pairs")
    numerators = {"me": total, "mse": squared, "mae": absolute, "pe": different}
    return {"metrics": {**{key: value / count for key, value in numerators.items()}, "max": maximum, "min": minimum},
            "exact_ratios": {key: str(Fraction(value, count)) for key, value in numerators.items()},
            "provenance": {"source_file": str(path), "source_sha256": hashlib.sha256(raw).hexdigest(),
                           "count": count, "sign": "approximate-exact", "units": "integer-output", "pe_unit": "fraction",
                           "coverage": "CSV rows only; exhaustive input coverage is not inferred",
                           "distribution": "one equal weight per CSV row, including duplicates",
                           "toolchain": f"tools/measure_errors.py; Python {platform.python_version()}",
                           "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.output and args.output.resolve() == args.input.resolve():
            raise ValueError("Input and output paths must be different")
        result = json.dumps(measure(args.input), ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(result, encoding="utf-8")
        else:
            print(result, end="")
        return 0
    except (ValueError, OSError, UnicodeError, OverflowError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
