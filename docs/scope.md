# Scope

Single-company case study: the funding history of Unitree (宇树科技), taken
from its STAR Market prospectus (招股书) saved in raw/unitree/.

| Item | Decision |
|---|---|
| Company | Unitree (宇树科技) only |
| Source | The STAR Market prospectus in raw/unitree/ (single origin). Press reports are comparison only. |
| Period | registration_date (date of 工商变更登记 stated in the prospectus) between 2022-01-01 and 2025-12-31 |
| Unit of record | One funding event = one capital increase (增资) = one row in Rounds |

## What counts as an event

- Counts as an event: a capital increase (增资) that brings cash into the
  company, as recorded in the prospectus.
- Does not count:
  - capital reserve conversion (资本公积转增股本);
  - secondary share transfers between shareholders (股权转让);
  - shareholding reform (整体变更);
  - IPO.
- Employee incentive platform capital increases (上海宇翼) are recorded with
  event_type = incentive_platform and excluded from nominal pivots.
  Investor capital increases are recorded with event_type = investor_round.

## Original scope (retired 2026-11-13)

Reason for retirement: the pilot of a non-IPO company (穹彻智能) produced
0 of 5 rounds with a specific amount.

The original scope is kept below unchanged for reference. It no longer
applies.

| Item | Decision |
|---|---|
| Segment | Embodied AI (具身智能, jùshēn zhìnéng) |
| Included | Humanoid robot makers; quadruped robot makers that position themselves as embodied AI; companies building models/platforms that act as the robot "brain" (具身大脑) |
| Excluded | Conventional industrial robot arms, autonomous vehicles, drones, surgical/medical robots, pure components (reducers, sensors, motors) |
| Period | First announcement date between 2022-01-01 and 2025-12-31 |
| Round criteria | Company based in mainland China, round officially announced, amount explicitly stated |
| Target | 30 rows with status "verified". No per-year quota. |

### What counts as a round

- Counts as a round: equity financing announced by the company or an
  investor.
- Does not count: bank loans, government grants or subsidies, IPOs, M&A,
  and pure debt financing.
- Convertible instruments: excluded in v1 unless a Tier 1 source calls it
  an equity round.

### Mainland China

"Mainland China" means: a Tier 1 source states the operating company is
registered or headquartered in mainland China. Otherwise the row is
excluded with the reason noted. Overseas holding structures are excluded in
v1 and counted in the limitations section.

### Gray-zone rule

The gray-zone rule applies to EVERY company, not only pivoted ones (e.g.
industrial robot makers that pivoted): include only if a Tier 1 source
describes an embodied-AI or humanoid product as of the round date. Record
the basis in scope_basis (sheet Rounds).

Wheeled logistics or service robots and dexterous-hand makers are included
only if the Tier 1 source itself uses embodied-AI or humanoid positioning;
otherwise excluded.

### Notes

- 2022-2023 will likely be thin and 2024-2025 dense. Do not force balance.
  Report as-is in limitations.
- Rounds with undisclosed or vague amounts are still recorded in Rounds with
  amount_status = undisclosed and status = excluded, so the size of this
  bias can be measured. See docs/data_dictionary.md.

### Known bias (README limitations)

State each of these in the limitations section of the README:

- Undisclosed amounts: requiring an explicit amount excludes undisclosed
  rounds (e.g. "数亿元").
- Companies that disclose amounts skew larger and more PR-active.
- Failed or quiet companies are invisible.
- The sample is small and descriptive only.
