"""Write docs/results.md from the data files and the check scripts' output.

Usage:
    python scripts/make_results.py [--events CSV] [--investor-rows CSV]
                                   [--cashflow CSV] [--extractions DIR]
                                   [--quote-source TXT] [--out MD]
                                   [--year-check-output TXT]
                                   [--sums-check-output TXT]

Defaults (relative to the repository root, found from this file's location):
    --events         data/events.csv
    --investor-rows  data/investor_rows.csv
    --cashflow       data/cashflow_lines.csv
    --extractions    data/extractions       (one <event_id>.json per event)
    --quote-source   raw/unitree/sse_prospectus_shenbaogao_20260320.txt
                     (the file every event JSON quotes)
    --out            docs/results.md

Inputs read: only the three CSV files above, plus the printed output of
scripts/check_year_totals.py, scripts/check_sums.py and
scripts/check_quotes.py. By default the scripts are run here and their
stdout and exit code are captured. --year-check-output and
--sums-check-output read a saved output file instead of running that
script (used by the tests); the exit code is then reported as "not run".
check_quotes.py is run once per event of events.csv, as
check_quotes.py <extractions>/<event_id>.json <quote-source>; when the
quote source is not on disk it is not run and the event is reported as
SKIP (raw file not on disk). The JSON files themselves are not read here.

Sections written:
  (a) one table per event, from events.csv, with a cross-check of
      amount_total_wan_cny and investor_count against investor_rows.csv;
  (b) the yearly reconciliation: sum of amount_total_wan_cny by
      cash_flow_year vs the primary cash-flow row of that year;
      status OK / MISMATCH / EXCLUDED (reconcile = N). A reconciled year
      with no events and a nil cash-flow line is "OK (trivial: nil = nil)".
      A cash-flow figure stored as 0 whose note contains
      "dash in source = nil" (the rule in docs/data_dictionary.md) is
      shown as "-", the way the source prints it;
  (c) the results of check_sums.py and check_year_totals.py, with counts
      per status;
  (d) the results of check_quotes.py per event, with PASS/FAIL/SKIP counts.

Every figure in the output is either copied from an input file or computed
with decimal.Decimal (never float). No figure is typed into this script.
The status column of events.csv is copied unchanged; this script never
produces a status value.

Before writing, the yearly statuses computed here are compared with the
per-year statuses printed by check_year_totals.py, and the event sums and
counts in events.csv with investor_rows.csv. Any disagreement is printed
and nothing is written.

Exit codes: 0 = results written;
            1 = disagreement found, nothing written;
            2 = usage error, missing input file, or missing column.
"""

import argparse
import csv
import re
import subprocess
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EVENT_COLUMNS = ("event_id", "event_type", "agreement_date", "registration_date",
                 "paid_in_date", "cash_flow_year", "amount_total_wan_cny",
                 "investor_count", "stated_total_wan_cny", "unit_basis", "status")
ROW_COLUMNS = ("event_id", "amount_wan_cny")
CASHFLOW_COLUMNS = ("year", "period_covered", "amount_wan_cny", "source_version",
                    "source_file", "printed_page", "primary", "reconcile", "note")

# Marker defined in docs/data_dictionary.md (data/cashflow_lines.csv): a dash
# in the source is stored as 0 and the note says this.
DASH_MARKER = "dash in source = nil"

YEAR_STATUS_RE = re.compile(r"^(OK|MISMATCH|EXCLUDED)\s+(\d{4}):")
SUMS_STATUS_RE = re.compile(r"^(OK|MISMATCH|NO_TOTAL|ERROR)\s+(\S+?):?(\s|$)")
QUOTE_STATUS_RE = re.compile(r"^(PASS|FAIL|SKIP)\s")
QUOTES_SUMMARY_RE = re.compile(r"^Summary: (\d+) PASS, (\d+) FAIL, (\d+) SKIP$")


class InputError(Exception):
    """Structural input problem (exit code 2)."""


def read_csv(path, required_columns):
    """Return [(line_number, row_dict)] of a UTF-8 CSV."""
    if not path.is_file():
        raise InputError(f"file not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in required_columns if c not in (reader.fieldnames or [])]
        if missing:
            raise InputError(f"{path} is missing column(s): {', '.join(missing)}")
        return list(enumerate(reader, start=2))


def dec(text, where):
    """Parse a plain decimal string (no thousands separators) into Decimal."""
    text = (text or "").strip()
    try:
        value = Decimal(text)
    except InvalidOperation:
        raise InputError(f"{where}: not a plain decimal number: {text!r}")
    if not value.is_finite():
        raise InputError(f"{where}: not a finite number: {text!r}")
    return value


def fmt_diff(diff):
    return "0" if diff == 0 else f"{diff:+}"


def cell(text):
    """Markdown table cell: empty -> (empty), pipes escaped."""
    text = (text or "").strip()
    return "(empty)" if not text else text.replace("|", "\\|")


def run_check(script, args):
    """Run a check script; return (stdout, exit_code)."""
    proc = subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=ROOT)
    out = proc.stdout
    if proc.stderr.strip():
        out += "\n[stderr]\n" + proc.stderr
    return out, proc.returncode


def load_output(path):
    if not path.is_file():
        raise InputError(f"file not found: {path}")
    return path.read_text(encoding="utf-8-sig")


def count_prefix(lines, regex):
    counts = {}
    for ln in lines:
        m = regex.match(ln)
        if m:
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return counts


def rel(path):
    """Path relative to the repository root when possible, with / separators."""
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def run_quote_checks(event_ids, extractions, quote_source):
    """Return [(event_id, pass, fail, skip, exit_text, note)] per event."""
    results = []
    for eid in event_ids:
        json_path = extractions / f"{eid}.json"
        if not quote_source.is_file():
            results.append((eid, "-", "-", "all", "not run",
                            "SKIP: raw file not on disk"))
            continue
        if not json_path.is_file():
            results.append((eid, "-", "-", "-", "not run",
                            f"ERROR: no extraction JSON at {rel(json_path)}"))
            continue
        out, rc = run_check("check_quotes.py", [str(json_path), str(quote_source)])
        hits = [QUOTES_SUMMARY_RE.match(ln.strip()) for ln in out.splitlines()]
        hits = [m for m in hits if m]
        if hits:
            p, f, s = hits[-1].groups()
            results.append((eid, p, f, s, str(rc), ""))
        else:
            first_err = next((ln for ln in out.splitlines() if ln.startswith("ERROR")),
                             "no summary line")
            results.append((eid, "-", "-", "-", str(rc), first_err))
    return results


def build(events, investor_rows, cashflow, year_out, year_rc, sums_out, sums_rc,
          quote_results, quote_source):
    """Return (markdown_text, problems)."""
    problems = []

    # Investor rows: Decimal sum and count per event.
    row_sum, row_count = {}, {}
    for line, row in investor_rows:
        eid = (row["event_id"] or "").strip()
        amount = dec(row["amount_wan_cny"], f"investor_rows line {line}")
        row_sum[eid] = row_sum.get(eid, Decimal(0)) + amount
        row_count[eid] = row_count.get(eid, 0) + 1

    # (a) Events.
    a = ["## (a) Events", "",
         "One table per event, copied from data/events.csv. The last two rows "
         "are recomputed here from data/investor_rows.csv (Decimal) as a "
         "consistency check. amount_total_wan_cny is a check value (sum of "
         "investor rows), not a sourced figure.", ""]
    year_events = {}
    type_events, type_rows = {}, {}
    seen = set()
    for line, ev in events:
        eid = (ev["event_id"] or "").strip()
        if eid in seen:
            raise InputError(f"events.csv line {line}: duplicate event_id {eid!r}")
        seen.add(eid)
        total = dec(ev["amount_total_wan_cny"], f"events.csv line {line}")
        count_text = (ev["investor_count"] or "").strip()
        if not count_text.isdigit():
            raise InputError(f"events.csv line {line}: invalid investor_count {count_text!r}")
        year_text = (ev["cash_flow_year"] or "").strip()
        if not re.fullmatch(r"\d{4}", year_text):
            raise InputError(f"events.csv line {line}: invalid cash_flow_year {year_text!r}")
        year_events.setdefault(int(year_text), []).append((eid, total))
        etype = (ev["event_type"] or "").strip() or "(empty)"
        type_events.setdefault(etype, []).append(eid)
        type_rows[etype] = type_rows.get(etype, 0) + row_count.get(eid, 0)

        rsum = row_sum.get(eid)
        rcount = row_count.get(eid, 0)
        sum_ok = rsum is not None and rsum == total
        count_ok = rcount == int(count_text)
        if not sum_ok:
            problems.append(f"{eid}: events.csv amount_total_wan_cny {total} != "
                            f"investor_rows sum {rsum if rsum is not None else '(no rows)'}")
        if not count_ok:
            problems.append(f"{eid}: events.csv investor_count {count_text} != "
                            f"investor_rows count {rcount}")

        a += [f"### {eid}", "", "| field | value |", "|---|---|"]
        for col in EVENT_COLUMNS:
            a.append(f"| {col} | {cell(ev[col])} |")
        a.append(f"| investor_rows.csv sum | {rsum if rsum is not None else '(no rows)'}"
                 f" ({'matches' if sum_ok else 'DOES NOT MATCH'}) |")
        a.append(f"| investor_rows.csv count | {rcount}"
                 f" ({'matches' if count_ok else 'DOES NOT MATCH'}) |")
        a.append("")
    for eid in row_sum:
        if eid not in seen:
            problems.append(f"{eid}: in investor_rows.csv but not in events.csv")

    a += ["### Investor rows by event_type", "",
          "Number of rows in data/investor_rows.csv for the events of each "
          "event_type in data/events.csv (counted here).", "",
          "| event_type | events | investor rows |", "|---|---|---|"]
    for etype in sorted(type_events):
        a.append(f"| {etype} | {', '.join(type_events[etype])} | {type_rows[etype]} |")
    a.append(f"| all | {', '.join(e for t in sorted(type_events) for e in type_events[t])} "
             f"| {sum(type_rows.values())} |")
    a.append("")

    # (b) Yearly reconciliation.
    year_rows = {}
    for line, row in cashflow:
        y = (row["year"] or "").strip()
        if not re.fullmatch(r"\d{4}", y):
            raise InputError(f"cashflow line {line}: invalid year {y!r}")
        year_rows.setdefault(int(y), []).append(
            (line, row, dec(row["amount_wan_cny"], f"cashflow line {line}")))

    b = ["## (b) Yearly reconciliation (Rule 2a(c))", "",
         "Sum of amount_total_wan_cny by cash_flow_year (data/events.csv) "
         "against the primary row of the line 吸收投资收到的现金 "
         "(data/cashflow_lines.csv, primary = Y). reconcile = N years are "
         "EXCLUDED. diff = sum - cash-flow line. A cash-flow line shown as "
         f"\"-\" is stored as 0 in data/cashflow_lines.csv with the note "
         f"\"{DASH_MARKER}\"; the source prints a dash.", "",
         "| year | events | sum of events | cash-flow line | period, source, page | diff | status |",
         "|---|---|---|---|---|---|---|"]
    my_status = {}
    for year in sorted(set(year_events) | set(year_rows)):
        evs = year_events.get(year, [])
        total = sum((t for _, t in evs), Decimal(0))
        names = ", ".join(e for e, _ in evs) or "(none)"
        rows = year_rows.get(year, [])
        primaries = [r for r in rows if (r[1]["primary"] or "").strip() == "Y"]
        if not rows:
            status, shown, where, diff = "MISMATCH", "(no row)", "", ""
        elif len(primaries) != 1:
            problems.append(f"{year}: {len(primaries)} primary cash-flow rows (exactly 1 required)")
            continue
        else:
            _, p, stated = primaries[0]
            is_dash = stated == 0 and DASH_MARKER in (p["note"] or "")
            shown = "-" if is_dash else str(stated)
            where = f"{p['period_covered']}, {p['source_version']}, p. {p['printed_page']}"
            diff = fmt_diff(total - stated)
            if (p["reconcile"] or "").strip() == "N":
                status = "EXCLUDED"
            elif total != stated:
                status = "MISMATCH"
            elif not evs and stated == 0:
                status = "OK (trivial: nil = nil)"
            else:
                status = "OK"
        my_status[year] = status.split()[0]
        b.append(f"| {year} | {names} | {total} | {shown} | {cell(where)} | {diff} | {status} |")
    b.append("")

    # Agreement with check_year_totals.py.
    year_lines = year_out.splitlines()
    script_status = {}
    for ln in year_lines:
        m = YEAR_STATUS_RE.match(ln)
        if m:
            script_status[int(m.group(2))] = m.group(1)
    for year in sorted(set(my_status) | set(script_status)):
        if my_status.get(year) != script_status.get(year):
            problems.append(f"{year}: status here {my_status.get(year)} vs "
                            f"check_year_totals.py {script_status.get(year)}")

    # (c) Check results.
    def rc_text(rc):
        return "not run (saved output read)" if rc is None else str(rc)

    def summary_line(lines, marker):
        hits = [ln for ln in lines if marker in ln]
        return hits[-1] if hits else "(no summary line found)"

    sums_lines = sums_out.splitlines()
    ycounts = count_prefix(year_lines, YEAR_STATUS_RE)
    cross = sum(1 for ln in year_lines if ln.startswith("CROSS-CHECK"))
    differs = sum(1 for ln in year_lines if ln.startswith("CROSS-CHECK") and "DIFFERS" in ln)
    yerr = sum(1 for ln in year_lines if ln.startswith("ERROR"))
    qcounts = count_prefix(year_lines, QUOTE_STATUS_RE)
    scounts = count_prefix(sums_lines, SUMS_STATUS_RE)

    c = ["## (c) Check results", "",
         "Counts are taken from the printed output of each script.", "",
         "### scripts/check_sums.py (Rule 2a(b))", "",
         "| status | count |", "|---|---|"]
    for k in ("OK", "MISMATCH", "NO_TOTAL", "ERROR"):
        c.append(f"| {k} | {scounts.get(k, 0)} |")
    c += ["", f"Exit code: {rc_text(sums_rc)}", "",
          f"Summary line: `{summary_line(sums_lines, 'event(s),')}`",
          "", "### scripts/check_year_totals.py (Rule 2a(c))", "",
          "| status | count |", "|---|---|"]
    for k in ("OK", "MISMATCH", "EXCLUDED"):
        c.append(f"| {k} | {ycounts.get(k, 0)} |")
    c += [f"| CROSS-CHECK | {cross} |", f"| CROSS-CHECK that differs | {differs} |",
          f"| ERROR | {yerr} |", "",
          "Cash-flow evidence quotes:", "", "| status | count |", "|---|---|"]
    for k in ("PASS", "FAIL", "SKIP"):
        c.append(f"| {k} | {qcounts.get(k, 0)} |")
    c += ["", "SKIP means the prospectus text file is not on disk (raw/ is not "
          "in the repository); SKIP is never a PASS.", "",
          f"Exit code: {rc_text(year_rc)}", "",
          f"Summary line: `{summary_line(year_lines, 'Summary:')}`", ""]

    # (d) Evidence quotes per event.
    d = ["## (d) Evidence quotes per event (scripts/check_quotes.py, Rule 2a(a))", "",
         f"Each event's extraction JSON checked against `{rel(quote_source)}`. "
         "When that file is not on disk, check_quotes.py is not run and the "
         "event is reported as SKIP (raw file not on disk). A SKIP printed by "
         "check_quotes.py itself is a field whose value is null. SKIP is "
         "never a PASS.", "",
         "| event_id | PASS | FAIL | SKIP | exit code | note |",
         "|---|---|---|---|---|---|"]
    for eid, p, f, s, rc, note in quote_results:
        d.append(f"| {eid} | {p} | {f} | {s} | {rc} | {cell(note) if note else ''} |")
    d.append("")

    head = ["# Results", "",
            "Generated by scripts/make_results.py. Do not edit by hand; re-run "
            "the script. Figures are in 万元 (CNY 10,000) as in the source "
            "files; nothing is converted.", "",
            "Inputs: data/events.csv, data/investor_rows.csv, "
            "data/cashflow_lines.csv, and the output of scripts/check_sums.py, "
            "scripts/check_year_totals.py and scripts/check_quotes.py.", "",
            "status is set by the project owner only. (empty) means not set.", ""]
    return "\n".join(head + a + b + c + d), problems


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Write docs/results.md.")
    ap.add_argument("--events", type=Path, default=ROOT / "data" / "events.csv")
    ap.add_argument("--investor-rows", type=Path, default=ROOT / "data" / "investor_rows.csv")
    ap.add_argument("--cashflow", type=Path, default=ROOT / "data" / "cashflow_lines.csv")
    ap.add_argument("--extractions", type=Path, default=ROOT / "data" / "extractions")
    ap.add_argument("--quote-source", type=Path,
                    default=ROOT / "raw" / "unitree" / "sse_prospectus_shenbaogao_20260320.txt")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "results.md")
    ap.add_argument("--year-check-output", type=Path)
    ap.add_argument("--sums-check-output", type=Path)
    args = ap.parse_args(argv)

    try:
        events = read_csv(args.events, EVENT_COLUMNS)
        investor_rows = read_csv(args.investor_rows, ROW_COLUMNS)
        cashflow = read_csv(args.cashflow, CASHFLOW_COLUMNS)
        if args.year_check_output:
            year_out, year_rc = load_output(args.year_check_output), None
        else:
            year_out, year_rc = run_check("check_year_totals.py",
                                          ["--investor-rows", str(args.investor_rows),
                                           "--extractions", str(args.extractions),
                                           "--cashflow", str(args.cashflow)])
        if args.sums_check_output:
            sums_out, sums_rc = load_output(args.sums_check_output), None
        else:
            sums_out, sums_rc = run_check("check_sums.py", [str(args.investor_rows)])
        event_ids = [(ev["event_id"] or "").strip() for _, ev in events]
        quote_results = run_quote_checks(event_ids, args.extractions, args.quote_source)
        text, problems = build(events, investor_rows, cashflow, year_out, year_rc,
                               sums_out, sums_rc, quote_results, args.quote_source)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if problems:
        print("Disagreement found; nothing written:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"Wrote {rel(args.out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
