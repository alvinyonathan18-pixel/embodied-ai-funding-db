"""Check that every evidence_quote in an extraction JSON appears verbatim
in its source text file.

Usage:
    python scripts/check_quotes.py EXTRACTION_JSON SOURCE_TEXT

The JSON follows the schema in docs/extraction_prompt.md:
    {"<field>": {"value": ..., "evidence_quote": ...}, ...,
     "investors": [{"name": ..., "role_raw": ..., "evidence_quote": ...}]}

Rules:
- Exact substring match. Only leading/trailing whitespace of the quote is
  stripped. No fuzzy matching, no Unicode or punctuation normalization.
- The source file is read as UTF-8 with line endings kept as they are on
  disk (a leading UTF-8 BOM, if any, is ignored).
- A non-null value with a missing, null, or empty evidence_quote is a FAIL
  (article_date included, no exemption).
- A field whose value is null is reported as SKIP.
- An investor item is checked if its name or role_raw is non-null.

Exit codes: 0 = all checks passed, 1 = at least one FAIL,
            2 = usage error, missing file, or invalid JSON.
"""

import json
import os
import sys


def check_quote(label, quote, source_text, results):
    """Append (status, label, detail) for one quote to results."""
    if quote is None:
        results.append(("FAIL", label, "value is non-null but evidence_quote is missing/null"))
        return
    if not isinstance(quote, str):
        results.append(("FAIL", label, f"evidence_quote is not a string: {quote!r}"))
        return
    stripped = quote.strip()
    if not stripped:
        results.append(("FAIL", label, "evidence_quote is empty"))
        return
    if stripped in source_text:
        results.append(("PASS", label, ""))
    else:
        results.append(("FAIL", label, f"quote not found verbatim: {stripped!r}"))


def check_field(name, field, source_text, results):
    """Check one {"value": ..., "evidence_quote": ...} field."""
    if not isinstance(field, dict):
        results.append(("FAIL", name, f"expected an object with value/evidence_quote, got {field!r}"))
        return
    if field.get("value") is None:
        results.append(("SKIP", name, "value is null"))
        return
    check_quote(name, field.get("evidence_quote"), source_text, results)


def check_investors(investors, source_text, results):
    """Check each item of the investors list."""
    if investors is None:
        results.append(("SKIP", "investors", "null"))
        return
    if not isinstance(investors, list):
        results.append(("FAIL", "investors", f"expected a list, got {investors!r}"))
        return
    if not investors:
        results.append(("SKIP", "investors", "empty list"))
        return
    for i, item in enumerate(investors):
        if not isinstance(item, dict):
            results.append(("FAIL", f"investors[{i}]", f"expected an object, got {item!r}"))
            continue
        label = f"investors[{i}] ({item.get('name')})"
        if item.get("name") is None and item.get("role_raw") is None:
            results.append(("SKIP", label, "name and role_raw are null"))
            continue
        check_quote(label, item.get("evidence_quote"), source_text, results)


def main():
    # Print UTF-8 so Chinese quotes survive pipes and redirects.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) != 3:
        print("Usage: python scripts/check_quotes.py EXTRACTION_JSON SOURCE_TEXT", file=sys.stderr)
        return 2
    json_path, source_path = sys.argv[1], sys.argv[2]

    for path in (json_path, source_path):
        if not os.path.isfile(path):
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            return 2

    try:
        with open(json_path, "r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {json_path}: {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"ERROR: {json_path} is not valid UTF-8: {exc}", file=sys.stderr)
        return 2

    try:
        # newline="" keeps \r\n as-is so matching is against the exact file text.
        with open(source_path, "r", encoding="utf-8-sig", newline="") as handle:
            source_text = handle.read()
    except UnicodeDecodeError as exc:
        print(f"ERROR: {source_path} is not valid UTF-8: {exc}", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print(f"ERROR: top level of {json_path} must be a JSON object", file=sys.stderr)
        return 2

    results = []
    for key, field in data.items():
        if key.startswith("_"):
            continue  # comment/metadata keys such as "_note" are not fields
        if key == "investors":
            check_investors(field, source_text, results)
        else:
            check_field(key, field, source_text, results)

    for status, label, detail in results:
        line = f"{status:<4}  {label}"
        if detail:
            line += f"  -- {detail}"
        print(line)

    n_pass = sum(1 for r in results if r[0] == "PASS")
    n_fail = sum(1 for r in results if r[0] == "FAIL")
    n_skip = sum(1 for r in results if r[0] == "SKIP")
    print(f"\nSummary: {n_pass} PASS, {n_fail} FAIL, {n_skip} SKIP")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
