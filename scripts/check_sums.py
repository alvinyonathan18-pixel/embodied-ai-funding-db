"""Check that per-investor amounts add up to the stated round total.

Usage:
    python scripts/check_sums.py [INVESTOR_ROWS_CSV] [EVENT_TOTALS_CSV]

Defaults:
    INVESTOR_ROWS_CSV = data/investor_rows.csv
        columns: event_id, investor_name_as_written, amount_wan_cny
    EVENT_TOTALS_CSV  = data/event_totals.csv
        columns: event_id, stated_total_wan_cny

For each event_id, amount_wan_cny is summed over all investor rows and
compared with stated_total_wan_cny. Arithmetic uses decimal.Decimal (never
float), so values like 0.1 + 0.2 compare exactly.

Rules:
- Amounts are parsed as plain decimal numbers in 万元 (no unit conversion
  happens here). Surrounding whitespace is stripped; thousands separators
  are NOT accepted, so a malformed value is reported instead of guessed.
- An event_id present in only one of the two files is a MISMATCH.
- A blank or unparseable amount is an ERROR for that event (counts as a
  failure).
- Duplicate event_id rows in the totals file are an ERROR.

Exit codes: 0 = every event OK, 1 = at least one MISMATCH or ERROR,
            2 = usage error, missing file, or missing required column.
"""

import csv
import os
import sys
from decimal import Decimal, InvalidOperation

DEFAULT_ROWS = os.path.join("data", "investor_rows.csv")
DEFAULT_TOTALS = os.path.join("data", "event_totals.csv")

ROW_COLUMNS = ("event_id", "investor_name_as_written", "amount_wan_cny")
TOTAL_COLUMNS = ("event_id", "stated_total_wan_cny")


def read_csv(path, required_columns):
    """Return the rows of a UTF-8 CSV as dicts; exit 2 on a structural problem."""
    if not os.path.isfile(path):
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    # utf-8-sig drops a leading BOM that Excel often writes.
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in required_columns if c not in (reader.fieldnames or [])]
        if missing:
            print(f"ERROR: {path} is missing column(s): {', '.join(missing)}", file=sys.stderr)
            sys.exit(2)
        # Line numbers start at 2 because line 1 is the header.
        return [(i, row) for i, row in enumerate(reader, start=2)]


def parse_amount(text):
    """Parse a decimal string into Decimal, or return None if invalid."""
    if text is None:
        return None
    text = text.strip()
    if not text:
        return None
    try:
        value = Decimal(text)
    except InvalidOperation:
        return None
    # Reject NaN / Infinity, which Decimal accepts as input.
    if not value.is_finite():
        return None
    return value


def main(argv):
    if len(argv) > 3:
        print(__doc__, file=sys.stderr)
        return 2
    rows_path = argv[1] if len(argv) > 1 else DEFAULT_ROWS
    totals_path = argv[2] if len(argv) > 2 else DEFAULT_TOTALS

    investor_rows = read_csv(rows_path, ROW_COLUMNS)
    total_rows = read_csv(totals_path, TOTAL_COLUMNS)

    # Per-event errors (bad amounts, duplicates) collected before comparing.
    errors = {}

    # Sum investor amounts per event, keeping first-seen order for output.
    sums = {}
    for line, row in investor_rows:
        event_id = (row["event_id"] or "").strip()
        amount = parse_amount(row["amount_wan_cny"])
        if amount is None:
            errors.setdefault(event_id, []).append(
                f"{rows_path} line {line}: invalid amount_wan_cny "
                f"{row['amount_wan_cny']!r} for {row['investor_name_as_written']!r}"
            )
            sums.setdefault(event_id, Decimal(0))
            continue
        sums[event_id] = sums.get(event_id, Decimal(0)) + amount

    # Read stated totals, one per event.
    totals = {}
    for line, row in total_rows:
        event_id = (row["event_id"] or "").strip()
        if event_id in totals:
            errors.setdefault(event_id, []).append(
                f"{totals_path} line {line}: duplicate event_id"
            )
            continue
        amount = parse_amount(row["stated_total_wan_cny"])
        if amount is None:
            errors.setdefault(event_id, []).append(
                f"{totals_path} line {line}: invalid stated_total_wan_cny "
                f"{row['stated_total_wan_cny']!r}"
            )
        totals[event_id] = amount

    # Union of event ids: investor-file order first, then totals-only ids.
    event_ids = list(sums) + [e for e in totals if e not in sums]

    failures = 0
    for event_id in event_ids:
        if event_id in errors:
            failures += 1
            print(f"ERROR     {event_id}")
            for msg in errors[event_id]:
                print(f"          {msg}")
            continue
        if event_id not in totals:
            failures += 1
            print(f"MISMATCH  {event_id}: sum={sums[event_id]} stated=(missing in {totals_path})")
            continue
        if event_id not in sums:
            failures += 1
            print(f"MISMATCH  {event_id}: sum=(no investor rows) stated={totals[event_id]}")
            continue
        total_sum = sums[event_id]
        stated = totals[event_id]
        diff = total_sum - stated
        # Decimal equality ignores trailing zeros: 100 == 100.00.
        if diff == 0:
            print(f"OK        {event_id}: sum={total_sum} stated={stated} diff=0")
        else:
            failures += 1
            print(f"MISMATCH  {event_id}: sum={total_sum} stated={stated} diff={diff:+}")

    print(f"\n{len(event_ids)} event(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
