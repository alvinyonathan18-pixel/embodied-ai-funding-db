"""Yearly cash-flow reconciliation (Rule 2a(c) in docs/data_dictionary.md).

Usage:
    python scripts/check_year_totals.py [--investor-rows CSV] [--extractions DIR]
                                        [--cashflow CSV] [--raw-dir DIR]

Defaults (relative to the repository root, found from this file's location):
    --investor-rows data/investor_rows.csv
        columns used: event_id, amount_wan_cny
    --extractions   data/extractions
        one JSON per event, named <event_id>.json
    --cashflow      data/cashflow_lines.csv
        columns: year, period_covered, amount_wan_cny, source_version,
                 source_file, printed_page, primary, reconcile,
                 evidence_quote, note
    --raw-dir       raw/unitree
        directory holding the files named in cashflow source_file

What it does:
1. Event amount = sum of amount_wan_cny over the event's rows in the
   investor rows file. Events are the event_ids in that file.
2. Cash-flow year of an event = year of paid_in_date if that field is in
   the event's JSON with a non-null value, otherwise year of
   registration_date. A missing JSON, or no usable date
   (missing, null, or not YYYY-MM-DD), is an ERROR for that event, and the
   event is left out of every year sum.
3. For each year (from events and from cash-flow rows):
   - reconcile = Y: sum of event amounts vs the primary row.
     OK if equal, else MISMATCH (sum, stated, diff, events used).
   - reconcile = N: EXCLUDED, with sum, stated, diff and the note.
   - every non-primary row: CROSS-CHECK, equal or DIFFERS from the primary
     row, with both period labels. A differing cross-check is reported but
     is not a failure.
   - a year with events but no cash-flow row: MISMATCH.
   - a year with cash-flow rows but not exactly one primary row, or with
     different reconcile values across its rows: ERROR.
4. Every evidence_quote must be an exact substring of ONE line of
   <raw-dir>/<source_file> (lines split at \\n, a trailing \\r removed, a
   leading BOM ignored; only leading/trailing whitespace of the quote is
   stripped, as in check_quotes.py). PASS / FAIL, or SKIP when the file is
   not on disk. SKIP is never a PASS.

Arithmetic uses decimal.Decimal only (never float). Amounts are plain
decimal numbers in 万元; thousands separators are rejected, not guessed.
Nothing is written to any data file.

Exit codes: 0 = no MISMATCH, ERROR or quote FAIL;
            1 = at least one MISMATCH, ERROR or quote FAIL;
            2 = usage error, missing input file, or missing column.
"""

import argparse
import csv
import json
import re
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ROW_COLUMNS = ("event_id", "amount_wan_cny")
CASHFLOW_COLUMNS = ("year", "period_covered", "amount_wan_cny", "source_version",
                    "source_file", "printed_page", "primary", "reconcile",
                    "evidence_quote", "note")
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


class InputError(Exception):
    """Structural input problem (exit code 2)."""


def read_csv(path, required_columns):
    """Return [(line_number, row_dict)] of a UTF-8 CSV."""
    if not path.is_file():
        raise InputError(f"file not found: {path}")
    # utf-8-sig drops a leading BOM that Excel often writes.
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in required_columns if c not in (reader.fieldnames or [])]
        if missing:
            raise InputError(f"{path} is missing column(s): {', '.join(missing)}")
        # Line numbers start at 2 because line 1 is the header.
        return list(enumerate(reader, start=2))


def parse_amount(text):
    """Parse a plain decimal string into Decimal, or return None if invalid."""
    text = (text or "").strip()
    if not text:
        return None
    try:
        value = Decimal(text)
    except InvalidOperation:
        return None
    return value if value.is_finite() else None


def parse_date(value):
    """Return a date for a strict YYYY-MM-DD string, else None."""
    if not isinstance(value, str):
        return None
    m = DATE_RE.match(value.strip())
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def field_value(data, name):
    """Return (present, value) for a {"value": ...} field of an extraction JSON."""
    field = data.get(name)
    if field is None:
        return False, None
    if isinstance(field, dict):
        return True, field.get("value")
    return True, field


def event_year(json_path):
    """Return (year, basis, date_text) or raise ValueError with the reason."""
    if not json_path.is_file():
        raise ValueError(f"no extraction JSON at {json_path}")
    try:
        data = json.loads(json_path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"cannot read {json_path}: {exc}")
    if not isinstance(data, dict):
        raise ValueError(f"top level of {json_path} is not an object")
    present, paid_in = field_value(data, "paid_in_date")
    if present and paid_in is not None:
        d = parse_date(paid_in)
        if d is None:
            raise ValueError(f"paid_in_date {paid_in!r} is not YYYY-MM-DD")
        return d.year, "paid_in_date", paid_in
    _, reg = field_value(data, "registration_date")
    if reg is None:
        raise ValueError("no paid_in_date and no registration_date")
    d = parse_date(reg)
    if d is None:
        raise ValueError(f"registration_date {reg!r} is not YYYY-MM-DD")
    return d.year, "registration_date", reg


def load_lines(path, cache):
    """Return the lines of a text file (split at \\n, trailing \\r removed)."""
    if path not in cache:
        text = path.read_text(encoding="utf-8-sig")
        cache[path] = [ln.rstrip("\r") for ln in text.split("\n")]
    return cache[path]


def check_quote(quote, path, cache):
    """Return (status, detail) for one evidence_quote."""
    if not path.is_file():
        return "SKIP", f"file not on disk: {path}"
    quote = (quote or "").strip()
    if not quote:
        return "FAIL", "evidence_quote is empty"
    lines = load_lines(path, cache)
    hits = [i for i, ln in enumerate(lines, start=1) if quote in ln]
    if hits:
        return "PASS", "line " + ", ".join(str(h) for h in hits)
    return "FAIL", f"not found within one line: {quote!r}"


def fmt_diff(diff):
    return "0" if diff == 0 else f"{diff:+}"


def main(argv=None):
    # Print UTF-8 so Chinese text survives pipes and redirects on Windows.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Yearly cash-flow reconciliation (Rule 2a(c)).")
    ap.add_argument("--investor-rows", type=Path, default=ROOT / "data" / "investor_rows.csv")
    ap.add_argument("--extractions", type=Path, default=ROOT / "data" / "extractions")
    ap.add_argument("--cashflow", type=Path, default=ROOT / "data" / "cashflow_lines.csv")
    ap.add_argument("--raw-dir", type=Path, default=ROOT / "raw" / "unitree")
    args = ap.parse_args(argv)

    try:
        investor_rows = read_csv(args.investor_rows, ROW_COLUMNS)
        cashflow_rows = read_csv(args.cashflow, CASHFLOW_COLUMNS)
        if not args.extractions.is_dir():
            raise InputError(f"directory not found: {args.extractions}")
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = []  # (scope, message)

    # 1. Event amounts.
    event_sums = {}
    event_bad = set()
    for line, row in investor_rows:
        event_id = (row["event_id"] or "").strip()
        amount = parse_amount(row["amount_wan_cny"])
        event_sums.setdefault(event_id, Decimal(0))
        if amount is None:
            event_bad.add(event_id)
            errors.append((event_id, f"{args.investor_rows} line {line}: invalid "
                                     f"amount_wan_cny {row['amount_wan_cny']!r}"))
            continue
        event_sums[event_id] += amount

    # 2. Cash-flow year per event.
    year_events = {}  # year -> [(event_id, amount, basis, date_text)]
    for event_id, amount in event_sums.items():
        if event_id in event_bad:
            continue
        try:
            year, basis, date_text = event_year(args.extractions / f"{event_id}.json")
        except ValueError as exc:
            errors.append((event_id, str(exc)))
            continue
        year_events.setdefault(year, []).append((event_id, amount, basis, date_text))

    ignored = sorted(p.name for p in args.extractions.glob("*.json")
                     if p.stem not in event_sums)

    # Cash-flow rows by year.
    year_rows = {}
    parsed_rows = []
    for line, row in cashflow_rows:
        label = f"{args.cashflow} line {line}"
        year_text = (row["year"] or "").strip()
        amount = parse_amount(row["amount_wan_cny"])
        primary = (row["primary"] or "").strip()
        reconcile = (row["reconcile"] or "").strip()
        problems = []
        if not re.fullmatch(r"\d{4}", year_text):
            problems.append(f"invalid year {row['year']!r}")
        if amount is None:
            problems.append(f"invalid amount_wan_cny {row['amount_wan_cny']!r}")
        if primary not in ("Y", "N"):
            problems.append(f"primary must be Y or N, got {row['primary']!r}")
        if reconcile not in ("Y", "N"):
            problems.append(f"reconcile must be Y or N, got {row['reconcile']!r}")
        if problems:
            errors.append((f"cash-flow row {line}", f"{label}: " + "; ".join(problems)))
            continue
        rec = dict(row, _line=line, _amount=amount, _year=int(year_text))
        parsed_rows.append(rec)
        year_rows.setdefault(rec["_year"], []).append(rec)

    # 3. Year checks.
    counts = {"OK": 0, "MISMATCH": 0, "EXCLUDED": 0, "CROSS-CHECK": 0, "DIFFERS": 0}
    excluded_years = []
    print("== Yearly reconciliation (吸收投资收到的现金)")
    for year in sorted(set(year_events) | set(year_rows)):
        events = year_events.get(year, [])
        total = sum((e[1] for e in events), Decimal(0))
        used = ", ".join(f"{e[0]}={e[1]} ({e[2]} {e[3]})" for e in events) or "(none)"
        rows = year_rows.get(year, [])
        if not rows:
            counts["MISMATCH"] += 1
            print(f"MISMATCH    {year}: sum={total} stated=(no cash-flow row)")
            print(f"            events: {used}")
            continue
        primaries = [r for r in rows if r["primary"] == "Y"]
        recs = {r["reconcile"] for r in rows}
        if len(primaries) != 1:
            errors.append((str(year), f"{len(primaries)} primary rows (exactly 1 required)"))
            continue
        if len(recs) != 1:
            errors.append((str(year), "rows disagree on reconcile (Y and N)"))
            continue
        p = primaries[0]
        stated = p["_amount"]
        diff = total - stated
        where = f"[{p['period_covered']}, {p['source_version']}, p. {p['printed_page']}]"
        if p["reconcile"] == "Y":
            # Decimal equality ignores trailing zeros: 88505.0000 == 88505.00.
            status = "OK" if diff == 0 else "MISMATCH"
            counts[status] += 1
            print(f"{status:<11} {year}: sum={total} stated={stated} diff={fmt_diff(diff)} {where}")
            print(f"            events: {used}")
        else:
            counts["EXCLUDED"] += 1
            excluded_years.append(year)
            print(f"EXCLUDED    {year}: sum={total} stated={stated} diff={fmt_diff(diff)} {where}")
            print(f"            events: {used}")
            print(f"            note: {p['note']}")
        for r in rows:
            if r is p:
                continue
            counts["CROSS-CHECK"] += 1
            same = r["_amount"] == stated
            if not same:
                counts["DIFFERS"] += 1
            verdict = "equals primary" if same else f"DIFFERS from primary (diff={fmt_diff(r['_amount'] - stated)})"
            print(f"CROSS-CHECK {year}: {r['_amount']} [{r['period_covered']}, {r['source_version']}] "
                  f"{verdict} {stated} [{p['period_covered']}, {p['source_version']}]")

    # Errors.
    if errors:
        print("\n== Errors")
        for scope, msg in errors:
            print(f"ERROR       {scope}: {msg}")

    # 4. Quotes.
    print("\n== Evidence quotes (exact substring of one line)")
    qcounts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    cache = {}
    for r in parsed_rows:
        status, detail = check_quote(r["evidence_quote"], args.raw_dir / r["source_file"], cache)
        qcounts[status] += 1
        print(f"{status:<4}  {args.cashflow.name} line {r['_line']} ({r['_year']}, "
              f"{r['source_version']}): {r['source_file']} {detail}")

    if ignored:
        print(f"\nINFO: extraction JSON without investor rows, not treated as events: "
              f"{', '.join(ignored)}")

    excl = ", ".join(str(y) for y in excluded_years) or "none"
    print(f"\nSummary: {counts['OK']} OK, {counts['MISMATCH']} MISMATCH, "
          f"{counts['EXCLUDED']} EXCLUDED (years: {excl}), "
          f"{counts['CROSS-CHECK']} CROSS-CHECK ({counts['DIFFERS']} differ), "
          f"{len(errors)} ERROR; quotes: {qcounts['PASS']} PASS, "
          f"{qcounts['FAIL']} FAIL, {qcounts['SKIP']} SKIP")
    failed = counts["MISMATCH"] or errors or qcounts["FAIL"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
