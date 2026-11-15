"""Tests for scripts/make_results.py. SYNTHETIC TEST DATA, NOT REAL.

Run from the repository root:
    python -m unittest discover -s scripts/tests -v

Fixtures are in scripts/tests/synthetic_results/. The check-script output
is read from saved files (--year-check-output / --sums-check-output), so
the test does not depend on the real data or on raw/.

Cases:
  2041: SYN-R01 (0.1 + 0.2, a float trap) + SYN-R02 100.50 = 100.80 -> OK
  2042: SYN-R03 registered 2040, paid in 2042, counted in 2042      -> OK
  2043: SYN-R04 10 vs cash-flow 9.99                               -> MISMATCH (+0.01)
  2044: reconcile = N, no events                                   -> EXCLUDED
  2045: no events, cash-flow 0 with note "dash in source = nil"    -> "-", OK (trivial: nil = nil)

Quotes (check_quotes.py is run for real on synthetic_results/extractions
against synthetic_results/source.txt):
  SYN-R01 2 PASS; SYN-R02 1 FAIL (deliberate); SYN-R03 1 PASS, 1 SKIP
  (null field); SYN-R04 has no JSON -> ERROR row; source absent -> SKIP.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "synthetic_results"
sys.path.insert(0, str(HERE.parent))

import make_results  # noqa: E402


class MakeResultsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.out = self.tmp / "results.md"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_script(self, **overrides):
        paths = {
            "events": FIX / "events.csv",
            "investor-rows": FIX / "investor_rows.csv",
            "cashflow": FIX / "cashflow_lines.csv",
            "year-check-output": FIX / "year_check_output.txt",
            "sums-check-output": FIX / "sums_check_output.txt",
            "extractions": FIX / "extractions",
            "quote-source": FIX / "source.txt",
        }
        paths.update(overrides)
        argv = ["--out", str(self.out)]
        for key, value in paths.items():
            argv += [f"--{key}", str(value)]
        return make_results.main(argv)

    def copy_with(self, name, old, new):
        """Copy a fixture into the temp dir with one text replacement."""
        text = (FIX / name).read_text(encoding="utf-8")
        self.assertIn(old, text)
        path = self.tmp / name
        path.write_text(text.replace(old, new), encoding="utf-8")
        return path

    def test_good_run(self):
        self.assertEqual(self.run_script(), 0)
        md = self.out.read_text(encoding="utf-8")
        # (a) one table per event, status copied unchanged or (empty).
        for eid in ("SYN-R01", "SYN-R02", "SYN-R03", "SYN-R04"):
            self.assertIn(f"### {eid}", md)
        self.assertIn("| status | synthetic-status-kept |", md)
        self.assertIn("| status | (empty) |", md)
        self.assertIn("| investor_rows.csv sum | 0.3 (matches) |", md)
        self.assertNotIn("DOES NOT MATCH", md)
        # Investor rows by event_type: 2 + 1 + 1 investor_round, 1 incentive_platform.
        self.assertIn("| incentive_platform | SYN-R02 | 1 |", md)
        self.assertIn("| investor_round | SYN-R01, SYN-R03, SYN-R04 | 4 |", md)
        self.assertIn("| all | SYN-R02, SYN-R01, SYN-R03, SYN-R04 | 5 |", md)
        # (b) yearly table, Decimal arithmetic.
        self.assertIn("| 2041 | SYN-R01, SYN-R02 | 100.80 | 100.80 |", md)
        self.assertIn("| 0 | OK |", md)
        self.assertIn("| 2042 | SYN-R03 | 50 | 50.00 |", md)
        self.assertIn("| +0.01 | MISMATCH |", md)
        self.assertIn("| 2044 | (none) | 0 | 77 |", md)
        self.assertIn("| -77 | EXCLUDED |", md)
        # (c) counts from the saved outputs.
        self.assertIn("| NO_TOTAL | 1 |", md)
        self.assertIn("| CROSS-CHECK that differs | 1 |", md)
        self.assertIn("| SKIP | 6 |", md)
        self.assertIn("Exit code: not run (saved output read)", md)
        self.assertIn("`4 event(s), 0 failure(s), 1 without stated total`", md)
        # No float artefacts.
        self.assertNotIn("0.30000000000000004", md)

    def test_nil_year_shows_dash_and_trivial_ok(self):
        self.assertEqual(self.run_script(), 0)
        md = self.out.read_text(encoding="utf-8")
        self.assertIn("| 2045 | (none) | 0 | - | 2045 年度, SYN 甲稿, p. 9-9-1 | 0 | "
                      "OK (trivial: nil = nil) |", md)

    def test_zero_without_dash_note_is_shown_as_zero(self):
        cash = self.copy_with("cashflow_lines.csv", "dash in source = nil. synthetic nil year",
                              "synthetic nil year")
        self.assertEqual(self.run_script(cashflow=cash), 0)
        md = self.out.read_text(encoding="utf-8")
        self.assertIn("| 2045 | (none) | 0 | 0 |", md)
        self.assertIn("| OK (trivial: nil = nil) |", md)

    def test_quote_checks_per_event(self):
        self.assertEqual(self.run_script(), 0)
        md = self.out.read_text(encoding="utf-8")
        self.assertIn("## (d) Evidence quotes per event", md)
        self.assertIn("| SYN-R01 | 2 | 0 | 0 | 0 |  |", md)
        self.assertIn("| SYN-R02 | 0 | 1 | 0 | 1 |  |", md)
        self.assertIn("| SYN-R03 | 1 | 0 | 1 | 0 |  |", md)
        self.assertIn("| SYN-R04 | - | - | - | not run | ERROR: no extraction JSON at ", md)

    def test_quote_source_absent_is_skip(self):
        absent = self.tmp / "not_here.txt"
        self.assertEqual(self.run_script(**{"quote-source": absent}), 0)
        md = self.out.read_text(encoding="utf-8")
        for eid in ("SYN-R01", "SYN-R02", "SYN-R03", "SYN-R04"):
            self.assertIn(f"| {eid} | - | - | all | not run | SKIP: raw file not on disk |", md)

    def test_output_is_deterministic(self):
        self.assertEqual(self.run_script(), 0)
        first = self.out.read_bytes()
        self.assertEqual(self.run_script(), 0)
        self.assertEqual(first, self.out.read_bytes())

    def test_disagreement_with_check_year_totals_writes_nothing(self):
        year = self.copy_with("year_check_output.txt", "MISMATCH    2043:", "OK          2043:")
        self.assertEqual(self.run_script(**{"year-check-output": year}), 1)
        self.assertFalse(self.out.exists())

    def test_events_total_not_matching_investor_rows_writes_nothing(self):
        events = self.copy_with("events.csv", ",2043,10,1,", ",2043,11,1,")
        self.assertEqual(self.run_script(events=events), 1)
        self.assertFalse(self.out.exists())

    def test_thousands_separator_is_rejected(self):
        events = self.copy_with("events.csv", ",2041,100.50,1,", ',2041,"1,00.50",1,')
        self.assertEqual(self.run_script(events=events), 2)
        self.assertFalse(self.out.exists())

    def test_year_with_events_but_no_cashflow_row_is_mismatch(self):
        cash = self.copy_with("cashflow_lines.csv",
                              "2043,2043 年度,9.99,SYN 甲稿,synthetic_absent.txt,9-9-1,Y,Y,9.99,"
                              "synthetic deliberate mismatch\n", "")
        year = self.copy_with("year_check_output.txt",
                              "MISMATCH    2043: sum=10 stated=9.99 diff=+0.01",
                              "MISMATCH    2043: sum=10 stated=(no cash-flow row)")
        self.assertEqual(self.run_script(cashflow=cash, **{"year-check-output": year}), 0)
        md = self.out.read_text(encoding="utf-8")
        self.assertIn("| 2043 | SYN-R04 | 10 | (no row) |", md)


if __name__ == "__main__":
    unittest.main()
