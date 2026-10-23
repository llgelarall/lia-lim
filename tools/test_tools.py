"""Numerical/provenance/packaging checks; fixtures never become published data."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

import catalog
from measure_errors import measure


class ErrorMeasurementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "pairs.csv"

    def test_signed_metrics_and_probability(self):
        self.path.write_text("exact,approximate\n2,0\n2,1\n2,2\n2,5\n", encoding="utf-8")
        result = measure(self.path)
        self.assertEqual(result["metrics"], {"me": 0, "mse": 3.5, "mae": 1.5, "pe": .75, "min": -2, "max": 3})
        self.assertEqual(result["exact_ratios"]["pe"], "3/4")
        self.assertEqual(result["provenance"]["count"], 4)
        self.assertEqual(len(result["provenance"]["source_sha256"]), 64)

    def test_large_integer_outputs_do_not_lose_low_bits(self):
        self.path.write_text(f"exact,approximate\n{2**100},{2**100 + 1}\n", encoding="utf-8")
        self.assertEqual(measure(self.path)["metrics"]["me"], 1)

    def test_invalid_or_empty_pairs_are_rejected(self):
        for content in ("exact,approximate\n", "exact,approximate\n1,1.5\n", "exact,approximate\n1,\n", "x,y\n1,1\n"):
            with self.subTest(content=content):
                self.path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    measure(self.path)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "models").mkdir()
        (self.root / "models/fixture.c").write_bytes(b"/* Test fixture only. */\r\n")
        (self.root / "models/support.h").write_bytes(b"/* Test header only. */\n")
        (self.root / "report.txt").write_text("Unit-test evidence fixture, not research data.")
        self.record = {"id": "test-only-A", "architecture": "test-only", "kind": "adder", "width": 8, "signed": False, "lpl": 4,
                       "parameters": {"WIDTH": 8, "LPL": 4}, "implementations": {"c": ["models/fixture.c", "models/support.h"]},
                       "error": {"me": 0, "mse": 3.5, "mae": 1.5, "pe": .75, "min": -2, "max": 3},
                       "ppa": {"area": 1, "power": 2, "delay": 3},
                       "provenance": {"source_files": ["report.txt"],
                           "error": {"sign": "approximate-exact", "units": "integer-output", "pe_unit": "fraction", "domain": "test only", "coverage": "test workload", "distribution": "uniform test rows", "count": 4, "toolchain": "test harness"},
                           "ppa": {"units": {"area": "um2", "power": "uW", "delay": "ns"}, "platform": "fixture", "corner": "fixture", "voltage_v": 1, "temperature_c": 25, "constraints": "fixture", "activity": "fixture", "toolchain": "fixture", "area_definition": "fixture", "power_definition": "fixture", "delay_definition": "fixture"}},
                       "benchmark_group": "test-only-group"}

    def dataset(self, *records):
        return {"schema_version": 1, "site": {"url": None, "repository_url": None}, "components": list(records)}

    def test_verified_shape_is_accepted(self):
        self.assertEqual(catalog.validate(self.dataset(self.record), self.root)["errors"], [])

    def test_unknown_measurement_is_not_zero(self):
        self.assertIsNone(catalog.metric({"error": {"min": None, "max": 2}}, "wce"))
        self.assertIsNone(catalog.metric({"ppa": {}}, "power"))
        self.assertEqual(catalog.metric(self.record, "wce"), 3)

    def test_units_and_missing_provenance_are_rejected(self):
        for change in ("units", "source", "sign"):
            record = copy.deepcopy(self.record)
            if change == "units":
                record["provenance"]["ppa"]["units"]["power"] = "mW"
            elif change == "source":
                record["provenance"]["source_files"] = []
            else:
                record["provenance"]["error"]["sign"] = "exact-approximate"
            self.assertTrue(catalog.validate(self.dataset(record), self.root)["errors"])

    def test_inconsistent_metrics_are_rejected(self):
        for error in ({"me": 10, "mae": 1}, {"mae": 3, "mse": 1}, {"min": 5, "max": 2}, {"pe": 25}, {"mse": float("nan")}):
            record = copy.deepcopy(self.record)
            record["error"] = error
            self.assertTrue(catalog.validate(self.dataset(record), self.root)["errors"])

    def test_chart_groups_reject_different_conditions(self):
        other = copy.deepcopy(self.record)
        other["id"] = "test-only-B"
        other["provenance"]["ppa"]["corner"] = "different"
        self.assertTrue(any("mixes" in e for e in catalog.validate(self.dataset(self.record, other), self.root)["errors"]))

    def test_missing_files_and_path_escape_are_rejected(self):
        for path in ("missing.c", "../outside.c", str(self.root / "report.txt")):
            with self.assertRaises(ValueError):
                catalog.local_file(self.root, path)

    def test_archives_preserve_bytes_parameters_and_hashes(self):
        url = catalog.archive(self.root, "downloads/test.zip", [self.record])
        first_bytes = (self.root / url).read_bytes()
        catalog.archive(self.root, url, [self.record])
        self.assertEqual(first_bytes, (self.root / url).read_bytes())
        with zipfile.ZipFile(self.root / url) as bundle:
            self.assertEqual(bundle.read("sources/models/fixture.c"), (self.root / "models/fixture.c").read_bytes())
            manifest = json.loads(bundle.read("MANIFEST.json"))
            self.assertEqual(manifest["configurations"][0]["parameters"], {"WIDTH": 8, "LPL": 4})
            self.assertEqual(set(manifest["sha256"]), {"models/fixture.c", "models/support.h"})
        self.assertIsNone(catalog.archive(self.root, "downloads/no-python.zip", [self.record], "python"))
        self.assertFalse((self.root / "downloads/no-python.zip").exists())

    def test_empty_build_advertises_no_downloads_or_fake_rows(self):
        source = catalog.ROOT / "index.html"
        (self.root / "index.html").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        catalog.build(self.dataset(), self.root)
        page = (self.root / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("data-record-id=", page)
        self.assertNotIn("href=\"downloads/", page)
        self.assertIn("No released configurations", page)


if __name__ == "__main__":
    unittest.main()
