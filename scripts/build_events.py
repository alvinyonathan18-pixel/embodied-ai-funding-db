"""Build data/events.csv, one row per event, from the extraction JSONs,
data/investor_rows.csv and data/event_totals.csv.

Usage:
    python scripts/build_events.py [--investor-rows CSV] [--totals CSV]
                                   [--extractions DIR] [--out CSV]
                                   [--status-from CSV]

Defaults (relative to the repository root, found from this file's location):
    --investor-rows data/investor_rows.csv
    --totals        data/event_totals.csv
    --extractions   data/extractions      (one <event_id>.json per event)
    --out           data/events.csv
    --status-from   same as --out         (existing file whose status is kept)

Events are the event_ids in the investor rows file, in first-seen order.
Other JSON files in the extractions directory (e.g. the unitree_5* press
extractions) are ignored.

Columns written:
    event_id, event_type, agreement_date, registration_date, paid_in_date,
    cash_flow_year, amount_total_wan_cny, investor_count,
    stated_total_wan_cny, unit_basis, status

- event_type, agreement_date, registration_date, paid_in_date: the "value"
  of the field in <event_id>.json; empty when the field is absent or null.
  event_type is required and must be investor_round or incentive_platform.
- cash_flow_year (Rule 2a(c)): year of paid_in_date if present, otherwise
  year of registration_date. No usable date is an ERROR.
- amount_total_wan_cny: Decimal sum of amount_wan_cny over the event's
  investor rows (never float), without thousands separators.
- investor_count: number of investor rows of the event.
- stated_total_wan_cny: the value in event_totals.csv (a number or NONE).
  An event missing from that file is an ERROR.
- unit_basis: share_count_wan or registered_capital_wan, the quantity
  column filled in the event's rows. A row with both or neither filled, or
  an event whose rows mix the two, is an ERROR.
- status: owned by the project owner. If --status-from exists, the status
  of each event_id is copied from it unchanged; a new event_id gets an
  empty status. The script itself never produces a status value. An
  event_id in --status-from that is no longer an event is an ERROR (so a
  human status is never dropped silently).

All-or-nothing: on any ERROR nothing is written.

Exit codes: 0 = file written, 1 = at least one ERROR (nothing written),
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

OUT_COLUMNS = ["event_id", "event_type", "agreement_date", "registration_date",
               "paid_in_date", "cash_flow_year", "amount_total_wan_cny",
               "investor_count", "stated_total_wan_cny", "unit_basis", "status"]
ROW_COLUMNS = ("event_id", "amount_wan_cny", "share_count_wan", "registered_capital_wan")
TOTAL_COLUMNS = ("event_id", "stated_total_wan_cny")
STATUS_COLUMNS = ("event_id", "status")
EVENT_TYPES = ("investor_round", "incentive_platform")
UNIT_COLUMNS = ("share_count_wan", "registered_capital_wan")
NONE_MARKER = "NONE"
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


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
    m = DATE_RE.match(value)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def json_value(data, name):
    """Return the stripped string value of a {"value": ...} field, or ""."""
    field = data.get(name)
    value = field.get("value") if isinstance(field, dict) else field
    return "" if value is None else str(value).strip()


def build_event(event_id, rows, totals, extractions_dir, errors):
    """Return the output row for one event, appending problems to errors."""
    out = {"event_id": event_id}
    n_errors = len(errors)

    def err(msg):
        errors.append(f"{event_id}: {msg}")

    # Extraction JSON.
    path = extractions_dir / f"{event_id}.json"
    data = {}
    if not path.is_file():
        err(f"no extraction JSON at {path}")
    else:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            err(f"cannot read {path}: {exc}")
        if not isinstance(data, dict):
            err(f"top level of {path} is not an object")
            data = {}
    if data:
        out["event_type"] = json_value(data, "event_type")
        if out["event_type"] not in EVENT_TYPES:
            err(f"event_type must be one of {', '.join(EVENT_TYPES)}, "
                f"got {out['event_type'] or '(missing)'!r}")
        for name in ("agreement_date", "registration_date", "paid_in_date"):
            out[name] = json_value(data, name)
            if out[name] and parse_date(out[name]) is None:
                err(f"{name} {out[name]!r} is not YYYY-MM-DD")
        basis = "paid_in_date" if out["paid_in_date"] else "registration_date"
        d = parse_date(out[basis]) if out[basis] else None
        if d is None and not out[basis]:
            err("no paid_in_date and no registration_date (cash_flow_year unknown)")
        out["cash_flow_year"] = str(d.year) if d else ""

    # Investor rows: amount sum, count, unit basis.
    total = Decimal(0)
    bases = set()
    for line, row in rows:
        amount = parse_amount(row["amount_wan_cny"])
        if amount is None:
            err(f"investor rows line {line}: invalid amount_wan_cny {row['amount_wan_cny']!r}")
        else:
            total += amount
        filled = [c for c in UNIT_COLUMNS if (row[c] or "").strip()]
        if len(filled) != 1:
            err(f"investor rows line {line}: exactly one of {', '.join(UNIT_COLUMNS)} "
                f"must be filled, found {len(filled)}")
        bases.update(filled)
    if len(bases) > 1:
        err(f"rows mix unit bases ({', '.join(sorted(bases))})")
    out["amount_total_wan_cny"] = str(total)
    out["investor_count"] = str(len(rows))
    out["unit_basis"] = bases.pop() if len(bases) == 1 else ""

    # Stated total.
    stated = totals.get(event_id)
    if stated is None:
        err("not in event totals file")
        stated = ""
    elif stated != NONE_MARKER and parse_amount(stated) is None:
        err(f"invalid stated_total_wan_cny {stated!r}")
    out["stated_total_wan_cny"] = stated

    return out if len(errors) == n_errors else None


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Build data/events.csv.")
    ap.add_argument("--investor-rows", type=Path, default=ROOT / "data" / "investor_rows.csv")
    ap.add_argument("--totals", type=Path, default=ROOT / "data" / "event_totals.csv")
    ap.add_argument("--extractions", type=Path, default=ROOT / "data" / "extractions")
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "events.csv")
    ap.add_argument("--status-from", type=Path, default=None)
    args = ap.parse_args(argv)
    status_path = args.status_from or args.out

    try:
        investor_rows = read_csv(args.investor_rows, ROW_COLUMNS)
        total_rows = read_csv(args.totals, TOTAL_COLUMNS)
        if not args.extractions.is_dir():
            raise InputError(f"directory not found: {args.extractions}")
        status_rows = read_csv(status_path, STATUS_COLUMNS) if status_path.is_file() else []
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = []

    rows_by_event = {}
    for line, row in investor_rows:
        rows_by_event.setdefault((row["event_id"] or "").strip(), []).append((line, row))

    totals = {}
    for line, row in total_rows:
        event_id = (row["event_id"] or "").strip()
        if event_id in totals:
            errors.append(f"{event_id}: duplicate in totals file (line {line})")
        totals[event_id] = (row["stated_total_wan_cny"] or "").strip()

    # Existing human-owned status, copied unchanged.
    status = {}
    for line, row in status_rows:
        event_id = (row["event_id"] or "").strip()
        if event_id in status:
            errors.append(f"{event_id}: duplicate in {status_path} (line {line})")
        status[event_id] = row["status"] or ""
    for event_id in status:
        if event_id not in rows_by_event:
            errors.append(f"{event_id}: in {status_path} (status {status[event_id]!r}) "
                          f"but has no investor rows; not dropped silently")

    out_rows = []
    for event_id, rows in rows_by_event.items():
        built = build_event(event_id, rows, totals, args.extractions, errors)
        if built is not None:
            built["status"] = status.get(event_id, "")
            out_rows.append(built)

    if errors:
        for msg in errors:
            print(f"ERROR  {msg}")
        print(f"\n{len(rows_by_event)} event(s), {len(errors)} ERROR; nothing written to {args.out}")
        return 1

    # Write atomically (temp file, then replace) with LF line endings.
    tmp = args.out.with_name(args.out.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)
    tmp.replace(args.out)

    kept = sum(1 for r in out_rows if r["event_id"] in status)
    print(f"{len(out_rows)} event(s) written to {args.out}; status kept for {kept}, "
          f"empty for {len(out_rows) - kept} new event(s); 0 ERROR")
    return 0


if __name__ == "__main__":
    sys.exit(main())
