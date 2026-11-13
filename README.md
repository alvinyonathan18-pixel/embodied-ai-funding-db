# Unitree funding history from its STAR Market prospectus

A record of the funding events of Unitree (宇树科技) from 2022 to
2025, built from its STAR Market prospectus (招股书). This is a
single-company case study. Validity matters more than volume.

## Method

1. The prospectus is saved as full text in raw/unitree/. For each saved
   file, the URL, publisher, access date and sha256 hash are recorded.
   raw/ stays local and is not pushed (copyright).
2. Every capital increase (增资) in the prospectus that falls in scope is
   recorded as one row in the Rounds sheet. Investor-level amounts and
   share counts go into the Round_Investor sheet.
3. Every value is copied from the saved file with a verbatim quote. No
   value is filled from memory. Units (亿/万) are never converted; Excel
   formulas do the conversion.
4. scripts/check_quotes.py checks that every quote exists in the saved
   file.
5. Only the project owner sets a row to verified, after manual checking.

Full definitions: docs/scope.md and docs/data_dictionary.md.

## Rules

### What counts as an event

- Counts: a capital increase (增资) that brings cash into the company, as
  recorded in the prospectus, with registration_date between 2022-01-01
  and 2025-12-31.
- Does not count: capital reserve conversion (资本公积转增股本), secondary
  share transfers between shareholders, shareholding reform (整体变更),
  IPO.
- Employee incentive platform capital increases (上海宇翼) are recorded
  with event_type = incentive_platform and excluded from nominal pivots.

### Data fields

- Rounds: event_type (investor_round / incentive_platform),
  agreement_date, registration_date (date of 工商变更登记 stated in the
  prospectus). Pivots group by registration_date.
- stage and stage_raw are optional and not used in pivots.
- announce_date is optional, only from a dated public report, always with
  announce_date_basis, and not used in pivots.
- Round_Investor: amount_wan_cny (the investor's own contribution as
  written in the prospectus table, copied, never computed) and
  share_count_wan (认购股份数). role = unknown, because the prospectus does
  not state a lead investor.

### Verification of prospectus-based rows

Only the project owner may set status = verified, and only after:

1. every quote passes scripts/check_quotes.py;
2. the sum of investor amounts equals the 合计 stated in the prospectus
   for that event;
3. the yearly sum of events reconciles with the cash-flow line
   吸收投资收到的现金, with any gap recorded in Verification_Log.

The Sources sheet states that these rows are single-origin (prospectus).
Press reports are comparison only.

## Limitations

- Single company. The results describe Unitree only and do not
  generalize to the embodied-AI sector.
- Draft prospectus. The prospectus used is a draft (申报稿) and is not
  legally effective. Its figures may change in later versions.
- Registration dates, not announcement dates. Dates are the dates of the
  business registration change (工商变更登记), not the dates the rounds
  were announced to the public.
- No stage data. The prospectus lists capital increases without round
  names (e.g. A轮, B轮), so stage is not reported.
- Single-origin source. All values come from one document. Internal
  checks (investor sums against 合计, yearly sums against the cash-flow
  statement) test its consistency, not its truth. Press reports are used
  for comparison only.
- Selection note. This scope replaced a multi-company scope. The pilot of
  a non-IPO company (穹彻智能) produced 0 of 5 rounds with a specific
  amount, so the project moved to a company with a prospectus. The case
  was chosen because its data is available, which is itself a selection
  effect. The original scope is kept in docs/scope.md.
