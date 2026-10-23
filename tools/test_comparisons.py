"""Checks for sign conversion and traceability of the actual comparison plots."""
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import unittest

from import_comparisons import normalized_errors, numeric, validate_row

ROOT = Path(__file__).resolve().parent.parent


class ComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data/comparisons.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))

    def test_sign_conversion_swaps_extrema(self):
        row = {"ME": "2", "MSE": "9", "MAE": "2.5", "PE": "0.75", "MIN": "-1", "MAX": "5"}
        self.assertEqual(normalized_errors(row), {"me": -2, "mse": 9, "mae": 2.5, "pe": .75, "min": -5, "max": 1})

    def test_methodology_provenance_and_counts_match_saved_rtl_checks(self):
        path=ROOT/self.data["methodology_source"]
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),self.data["methodology_sha256"])
        methodology=json.loads(path.read_text(encoding="utf-8"))
        for domain in methodology["verified_functional_domains"]:
            report=json.loads((ROOT/domain["report"]).read_text(encoding="utf-8"))
            self.assertEqual(domain["ordered_pairs_per_architecture"],1<<(2*domain["operand_bits"]))
            self.assertEqual(domain["operand_bits"],report["width"])
            self.assertEqual(report["status"],"passed")
            for record in report["configurations"]:
                self.assertEqual(record["pairs_checked"],domain["ordered_pairs_per_architecture"])
                self.assertEqual(record["mismatches"],0)
        for record in self.catalog["components"]:
            if record.get("source_comparison"):
                self.assertIn(self.data["methodology_source"],record["provenance"]["source_files"])
                self.assertIsNone(record["ppa"]["delay"])
                self.assertEqual(record["provenance"]["ppa"]["voltage_v"],"not recorded")

    def test_missing_values_stay_missing_and_nonfinite_is_rejected(self):
        self.assertIsNone(numeric(""))
        self.assertEqual(numeric("-0.135"), -.135)
        for value in ("nan", "inf", "-inf"):
            with self.assertRaises(ValueError):
                numeric(value)

    def test_raw_source_hashes_and_error_relationships(self):
        for benchmark in self.data["benchmarks"]:
            source = ROOT / benchmark["source_file"]
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), benchmark["source_sha256"])
            with source.open(encoding="utf-8-sig", newline="") as stream:
                raw = list(csv.DictReader(stream))
            self.assertEqual(raw, [row["raw"] for row in benchmark["rows"]])
            for row in raw:
                validate_row(row, benchmark["operand_width"])
            bad = copy.deepcopy(raw[0])
            bad["MAX_ABS"] = str(float(bad["MAX_ABS"]) + 1)
            with self.assertRaises(ValueError):
                validate_row(bad, benchmark["operand_width"])

    def test_plot_points_retain_source_values_and_percentiles(self):
        with (ROOT / "data/comparison-plot-points.csv").open(encoding="utf-8", newline="") as stream:
            points = list(csv.DictReader(stream))
        expected = 0
        for benchmark in self.data["benchmarks"]:
            for metric, plot in benchmark["plots"].items():
                for library, count in plot["counts"].items():
                    included = sorted((r for r in benchmark["rows"] if r["library"] == library and r["values"][metric] is not None), key=lambda r: (r["values"][metric], r["module"]))
                    actual = [p for p in points if p["source_file"] == benchmark["source_file"] and p["metric"] == metric and p["library"] == library]
                    self.assertEqual(len(actual), count)
                    expected += count
                    for rank, (point, row) in enumerate(zip(actual, included)):
                        self.assertEqual(point["module"], row["module"])
                        self.assertEqual(int(point["source_row"]), row["source_row"])
                        self.assertEqual(float(point["value"]), row["values"][metric])
                        self.assertAlmostEqual(float(point["percentile"]), 100 * rank / (count - 1) if count > 1 else 0)
                for fmt in ("png", "svg"):
                    self.assertTrue((ROOT / plot[fmt]).is_file())
        self.assertEqual(len(points), expected)

    def test_published_benchmarks_match_c_and_do_not_claim_physical_delay(self):
        for benchmark in self.data["benchmarks"]:
            report = ROOT / f'result/validation/{benchmark["kind"]}{benchmark["operand_width"]}-lpl8-c-python.json'
            baseline = {r["id"]: r["c"]["metrics"] for r in json.loads(report.read_text(encoding="utf-8"))["configurations"]}
            records = {r["architecture"]: r for r in self.catalog["components"] if r.get("source_comparison") == benchmark["id"]}
            self.assertEqual(set(records), set(baseline))
            for row in benchmark["rows"]:
                if row["library"] != benchmark["library"]:
                    continue
                record = records[row["module"]]
                for key, value in normalized_errors(row["raw"]).items():
                    self.assertTrue(math.isclose(value, baseline[row["module"]][key], abs_tol=1e-10, rel_tol=1e-10))
                self.assertEqual(record["error"], baseline[row["module"]])
                self.assertEqual(record["reported_timing_ns"], row["values"]["timing"])
                self.assertIsNone(record["ppa"]["delay"])


if __name__ == "__main__":
    unittest.main()
