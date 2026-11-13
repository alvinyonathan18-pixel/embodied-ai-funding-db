# Data dictionary

General rule (from CLAUDE.md): every value must come from a source file in
raw/. If a field is not explicitly stated in a source, it is null. Fields
that would need judgment (classification, entity matching, translation) are
null unless a source in raw/ states them, with a supporting quote_zh.

## Sheet Rounds

- round_id: R001, R002, ... unique, never reused
- company_id: must exist in Companies
- stage_raw: stage text exactly as in the source (e.g. "Pre-A+轮"). Never edited.
  Allowed sources: a Tier 1 announcement by the company or investor, or a
  Tier 2 report that quotes the company side, copied as written with its
  quote. A prospectus (招股书) or other regulator filing is NOT a source for
  stage_raw (it lists capital increases without round names). Never derive
  a stage from the order of capital increases in a prospectus. If sources
  disagree on the stage, the row stays unverified.
- stage: only from the standard list: Seed (种子轮), 天使轮, Pre-A, A轮,
  A+轮, B轮, B+轮, C轮, C+轮, D轮, E轮, F轮 and later letters, Strategic
  (战略融资), Pre-IPO, Other. Surface-form variants of a list value are
  accepted: trailing "融资", with or without "轮", and case differences
  (e.g. "Pre-A轮" = Pre-A). If stage_raw does not match a list value after
  this spelling normalization, stage = Other. Plus-suffixed variants not in
  the list (Pre-A+, A++, D+轮) remain Other. This is spelling normalization,
  not mapping between different stages (e.g. "Pre-A+" is Other, not Pre-A).
- announce_date: YYYY-MM-DD, date of FIRST public announcement, taken from
  the earliest dated public report of the round (a Tier 1 announcement or a
  Tier 2 report; Tier 3 is never used). Prospectuses (招股书) and other
  regulator filings published after the round are NOT used for
  announce_date, and dates they state (agreement, shareholder meeting,
  registration) are never copied into it. If the earliest report's text
  states the announcement date, announce_date uses it. If it only says
  "近日" or gives a partial date, announce_date = publish_date of that
  report. If no dated Tier 1 or Tier 2 public report exists, announce_date
  is null and the row stays unverified.
- announce_date_basis: text_stated, publish_date or media_publish_date.
  text_stated when the earliest report's text states the announcement
  date; publish_date when announce_date is the publish_date of a Tier 1
  announcement; media_publish_date when announce_date is the publish_date
  of a Tier 2 media report.
- amount_raw: text exactly as in the source (e.g. "近5亿元"). Never edited.
- currency: derived from currency_raw by fixed rule: 元 or 人民币 = RMB;
  美元 = USD. Any other currency word: currency = as written, and the row is
  flagged for the project owner's review. No FX conversion.
- amount_qualifier: exact or approx (approx if 近, 超, 约, 逾, etc.). Null
  when amount_status = undisclosed.
- amount_number: digits as written in amount_raw (e.g. 5), copied, never
  computed. Null if amount_raw has no specific number.
- amount_unit: unit as written in amount_raw, copied. Allowed values: 亿,
  千万, 百万, 万, million, billion. Null if no specific number.
- amount_value: Excel formula = amount_number x unit multiplier (see table
  below). Never typed.
- amount_status: disclosed or undisclosed
- status: verified, unverified, or excluded
- scope_basis: one sentence on why the company is in the segment, as of the
  round date. Must be a paraphrase of a quote from a Tier 1 source and must
  end with that source's source_id, e.g. "[S014]".

Pivots use only: status = verified AND amount_status = disclosed AND
amount_qualifier = exact. Approx rows are kept and shown in a separate table.

### Unit multipliers

| amount_unit | Multiplier |
|---|---|
| 亿 | 100,000,000 |
| 千万 | 10,000,000 |
| 百万 | 1,000,000 |
| 万 | 10,000 |
| million | 1,000,000 |
| billion | 1,000,000,000 |

### Approx vs. undisclosed

- A specific number with a qualifier (近, 超, 约, 逾, 余, etc.) is disclosed
  and approx. Examples: "近5亿元", "超10亿元".
- An amount with no specific digit is undisclosed. Examples: "数亿元",
  "数千万美元", "亿元级", "上亿元", "十余亿元" (数, 几, 上, 十余 count as
  no specific number).
- Undisclosed rounds still get a row: amount_status = undisclosed,
  status = excluded. amount_raw keeps the source text.

## Sheet Companies

company_id, name_zh, name_en, subsegment (humanoid / quadruped / embodied
model), city, founded_year, profile_source (source_id from the Sources
sheet).

name_en, subsegment, city, founded_year are null unless a source in raw/
states them. scope_basis lives only in Rounds.

## Sheet Investors

investor_id, name_standard, alias (semicolon-separated), type (VC /
corporate / government / other), possible_duplicate_of.

type is null unless a source in raw/ states it.

possible_duplicate_of (investor_id): a review flag only. Never change
names, aliases or merge based on it.

## Sheet Round_Investor

round_id, investor_id, role (lead / participant / unknown). If the source
does not state the lead, use unknown. Never guess from name order.

## Sheet Sources

source_id, round_id, company_id, url, local_file (path in raw/), sha256
(hash of the local file), tier (1/2/3), publisher, publish_date,
access_date, quote_zh (the exact source sentence supporting the value).

round_id may be blank when the source supports a company profile field.
company_id is nullable.

## Sheet Verification_Log

round_id, field, llm_value, true_value, correct (Y/N), error_type, note.

## Rules

1. Source tiers. Tier 1: official announcements by the company or investor,
   regulator filings, 招股书 prospectuses. Tier 2: major media explicitly
   quoting the company side. Tier 3: aggregators/databases, leads only.
   A prospectus or regulator filing is Tier 1 for amount and investors
   only; it is not a source for stage_raw or announce_date (see those
   fields).
2. Two-source rule: amount and date must match in at least two INDEPENDENT
   sources, at least one Tier 1 or 2. The date-match requirement applies
   only between sources that report an announcement date; a source that
   reports no announcement date (e.g. a prospectus) counts toward the
   amount match only. Several outlets quoting one press
   release count as ONE source. Otherwise status = unverified and the row
   is excluded from pivots. Meeting this rule does not make a row verified;
   only the project owner sets status = verified, after manual checking.
3. Never guess or take a midpoint for vague amounts: use undisclosed.
4. Store original amount and currency as-is. Never overwrite the original.
   FX conversion is out of scope for now: RMB and USD rounds are reported
   separately.
5. One entity = one standard investor name; keep variants in alias. Merge
   name variants only when a source in raw/ links them; otherwise keep them
   as separate investors.
6. One round = one row in Rounds, even if reported by many outlets.
7. Per-investor pivots count number of rounds joined or led, never sum the
   round amount per investor (that double-counts).
8. raw/ stays local and is not pushed (copyright). The repo stores URL, a
   short quote, access date, and the sha256 of the local file.

## Decision log

Resolved 2026-11-12, before any data was collected:

- Judgment fields (Investors.type, alias merging, Companies.name_en /
  subsegment / city / founded_year): null unless sourced.
- FX conversion: dropped for now (Rule 4 amended).
- Undisclosed or vague amounts: kept as rows with status = excluded.
- Stages: added Seed (种子轮) and Other; added stage_raw; no mapping.
- Approx vs. undisclosed: specific number + qualifier = approx; no specific
  number = undisclosed.
- scope_basis: removed from Companies; lives only in Rounds.
- Extraction prompt: article_date now requires an evidence_quote.

Changed 2026-11-12:

- Rounds: amount_value split into amount_number and amount_unit (both
  copied from amount_raw) plus amount_value (Excel formula only).
- Rounds: amount_qualifier is null when amount_status = undisclosed.
- Companies: added profile_source (source_id).
- Sources: round_id may be blank for company profile sources; added
  nullable company_id.
- scope_basis: must paraphrase a Tier 1 quote and end with its source_id,
  e.g. "[S014]".
- Investors: added possible_duplicate_of (review flag only, never used to
  merge or rename).
- Stages: surface-form variants of list values accepted (trailing "融资",
  with or without "轮", case). List extended to E轮, F轮 and later letters.
  Plus-suffixed variants not in the list stay Other. Spelling
  normalization only, no mapping between stages.

Changed 2026-11-12 (second revision):

- Rounds.currency: derived from currency_raw by fixed rule (元/人民币 = RMB,
  美元 = USD); any other currency word is kept as written and flagged for
  review. No FX conversion.
- Rounds: added announce_date_basis (text_stated / publish_date). Vague or
  partial dates fall back to the publish_date of the earliest Tier 1
  announcement; with no Tier 1 announcement, announce_date is null and the
  row stays unverified.
- amount_unit: allowed values 亿, 千万, 百万, 万, million, billion; added
  the unit multiplier table.
- Extraction prompt: added prompt-injection rule, this-round-only rule
  (no 累计融资), multiple_rounds_in_text field (with evidence_quote), currency_raw and
  date_in_text copy rules; lead_stated is true or null only.
- Scope: defined what counts as a round, what "mainland China" means, the
  gray-zone rule for every company, and the known bias list.

Changed 2026-11-13:

- Rule 1: a prospectus (招股书) or regulator filing is Tier 1 for amount,
  stage and investors, but not for announce_date.
- announce_date: taken from the earliest dated public report of the round
  (Tier 1 announcement or Tier 2 report), never from a prospectus or
  filing. A Tier 1 announcement is no longer required; with no dated Tier 1
  or Tier 2 report, announce_date is null and the row stays unverified.
- announce_date_basis: added media_publish_date (publish_date of a Tier 2
  media report).
- Rule 2: the date-match requirement applies only between sources that
  report an announcement date.

Changed 2026-11-13 (second revision):

- Rule 1 corrected: a prospectus (招股书) or regulator filing is Tier 1 for
  amount and investors only, not for stage_raw (the earlier 2026-11-13
  entry said "amount, stage and investors").
- stage_raw: may come from a Tier 1 company/investor announcement or a
  Tier 2 report quoting the company side, copied as written with its
  quote. Never derived from the order of capital increases in a
  prospectus. If sources disagree on the stage, the row stays unverified.

Changed 2026-11-13 (third revision):

- Extraction prompt: added an optional "Target round" input line above
  <source> (short description, no amounts, dates or investor names). If
  given, only that round is extracted, even when it is background in the
  text; if it is not in the text, all fields are null.
- Extraction prompt: multiple_rounds_in_text is true only when the text
  announces or reports more than one round as news; an earlier round
  mentioned as history does not count.
- Extraction prompt: added attribution field (words saying who the
  information comes from, copied as written, e.g. "有媒体报道",
  "公司表示"; null if none), with evidence_quote.
- Extraction prompt: amounts with spaces between digits and units
  (e.g. "7 亿元") are copied exactly as written.

Changed 2026-11-13 (fourth revision):

- Extraction prompt: the Target round line now defaults to
  "Target round (optional): NONE" so the template can be copied as-is;
  NONE is treated as no target line.
- Extraction prompt: the target line may not contain amounts, exact dates
  or investor names; a rough period such as "around June 2025" is
  allowed. Values are never copied from the target line.
- Extraction prompt: if the target round is not in the text, every round
  field is null, but company_name (the company the article is about) and
  article_date are still filled, each with its evidence_quote, if the
  text shows them. Neither is round data.
