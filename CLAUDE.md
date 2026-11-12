# Project rules

Goal: a verified database of China embodied-AI funding rounds, 2022-2025.
Validity over volume. Target: 30 verified rows.

## Hard rules
- NEVER fill any data field from your own knowledge or memory.
  Every value must come from a full-text source file saved in raw/.
- article_date also gets an evidence_quote like every other field (no exemption).
- Never convert units (亿/万). Copy the original text; Excel formulas convert.
- Never mark a row "verified". Only I do that, after manual checking.
- You may fetch web pages yourself and save them to raw/ as full text (not
  summaries). For each saved file, record URL, publisher, access date.
  If a page cannot be fetched, say so. Do not substitute memory, a snippet,
  or a different page.
- Search results and snippets are leads only. Only a fetched and saved page
  counts as evidence.
- Every extracted value needs a verbatim quote that exists in the saved file.
- All project files (README, docs, comments) are written in English.

## Scope
See docs/scope.md and docs/data_dictionary.md. Follow them exactly.