# Leads: 宇树科技 (company-slug: unitree)

LEADS ONLY. Nothing here is entered in Rounds/Sources and nothing is
verified. Values are copied exactly as written in the saved pages. Every
quote below is a verbatim substring of the named file in `raw/unitree/`
(checked by script on the access date). Access date for all files:
2026-11-13. Source log: `data/raw_sources.md`.

Tier guess uses docs/data_dictionary.md Rule 1 (1 = company/investor
announcement, regulator filing, 招股书; 2 = major media quoting the company
side; 3 = aggregator/database).

## Tier 1 source used for all rounds: the 招股书

No standalone company or investor announcement was fetchable for any round
(see "Not fetched" below). The only Tier 1 source saved is the SSE STAR
Market prospectus of 宇树科技股份有限公司, in two versions:

- `sse_prospectus_shenbaogao_20260320.txt` — 招股说明书（申报稿）, from
  static.sse.com.cn, dated 2026-03-20 in the URL path.
- `cninfo_prospectus_shanghuigao_20260525.txt` — 招股说明书（上会稿）, from
  cninfo, dated 2026-05-25 in the URL path. Same issuer, later draft; NOT an
  independent second source.

Caveats on the prospectus:

- It lists capital increases (增资) with per-investor 增资款 and a 合计
  line. It never uses round names (B轮, B2轮, C轮). Matching a 增资 to a
  press "round" is a judgment the owner must make; I did not make it.
- Text was extracted with `pdftotext -layout`. Table columns are partly
  misaligned in the .txt (names and numbers on shifted lines). Check table
  values against the PDF in `raw/unitree/pdf/`.
- It was first published 2026-03-20, outside the 2022-2025 period. Per the
  owner decision of 2026-11-13 (docs/data_dictionary.md), it is Tier 1 for
  amount, stage and investors but NOT for announce_date. The dates it
  states (agreement / shareholder meeting / registration) are never used
  as announce_date.

## Owner decisions (2026-11-13)

1. Prospectus: Tier 1 for amount, stage and investors, not for
   announce_date. announce_date comes from the earliest dated Tier 1 or
   Tier 2 public report; with a Tier 2 report the basis is
   media_publish_date. Date matching under Rule 2 applies only between
   sources that report an announcement date.
2. B2 (row 3): no amount is picked. Both figures are kept as written
   (press `近10亿元人民币`, prospectus 合计 `60,034.4827` 万元). Discrepancy
   flagged; row stays unverified.
3. June 2025 C round (row 5): 5b and 5c share one origin and count as ONE
   source. Row stays unverified unless an independent source is found. No
   further searching unless the owner asks.

Scope facts from the prospectus (apply to every round):

- Mainland China: cover page of `sse_prospectus_shenbaogao_20260320.txt`:
  `（浙江省杭州市滨江区西兴街道东流路 88 号 1 幢）`; also
  `公司住所              浙江省杭州市滨江区西兴街道东流路88号1幢306室`.
- Humanoid product date (gray-zone rule): `2023 年 8 月，公司首款自研全尺寸人形机器人 H1 面市，标志着公司正式`
  (same file). So a Tier 1 source shows a humanoid product only from
  2023-08. Before that date, no Tier 1 saved here describes an
  embodied-AI or humanoid product.

## Leads table

| # | stage_raw as seen | amount_raw as seen | date as seen | url | tier guess | saved_file | notes |
|---|---|---|---|---|---|---|---|
| 1a | B轮系列融资 | 合计数亿元 | 更新于：2022-04-20 10:57 | https://news.pedaily.cn/20220420/33444.shtml | 2 | raw/unitree/pedaily_20220420_33444.txt | 投资界 page; header says `来源：互联网`. Quotes CEO 王兴兴 and investors, i.e. company-side press release. |
| 1b | B轮系列融资 | 数亿元 | 2022-04-21 08:37 | https://www.thepaper.cn/newsDetail_forward_17709140 | 3 | raw/unitree/thepaper_17709140.txt | 澎湃号 post citing `猎云网4月20日消息`. Same press release as 1a → NOT independent. |
| 1c | B轮系列融资 | 合计数亿元 | 2022-04-20 08:10:32 | https://pe.hexun.com/2022-04-20/205758642.html | 3 | raw/unitree/hexun_205758642.txt | 和讯 repost of same press release → NOT independent. |
| 1d | (no round name) 2022 年第一次增资 | 7,150 万元 (经乾二号); 2,000 万元 (海克斯康) | 2021 年 12 月 30 日 (agreement); 2022 年 1 月 5 日 (registration) | https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_QY8F.pdf | 1 | raw/unitree/sse_prospectus_shenbaogao_20260320.txt | No 合计 line for this 增资. Not linked to "B轮" by the source. |
| 1e | (no round name) 2022 年第二次增资 | 5,000 万元 / 2,000 万元 / 1,000 万元 / 500 万元 / 人民币 2,343 万元等值美元 | 2022 年 2 月 28 日 (agreement) | same as 1d | 1 | raw/unitree/sse_prospectus_shenbaogao_20260320.txt | Investors 嘉兴骅茂, 浙江容腾, 江苏疌泉, 深创投集团, Astrend IV. No 合计 line. Not linked to "B轮" by the source. |
| 2 | (no round name) 2022 年第四次增资 | 2,000 万元 | 2022 年 8 月 15 日 (agreement); 2022 年 8 月 23 日 (registration) | same as 1d | 1 | raw/unitree/sse_prospectus_shenbaogao_20260320.txt | 中网投资 only. No press announcement found in 2022. |
| 3a | B2轮融资 | 近10亿元人民币 | 更新于：2024-02-28 16:03 | https://news.pedaily.cn/202402/530406.shtml | 2 | raw/unitree/pedaily_202402_530406.txt | `宇树科技宣布完成B2轮融资` → company-side. |
| 3b | B2 轮融资 | 近 10 亿元 | 2024-02-26 12:50 | https://hub.baai.ac.cn/view/35340 | 3 | raw/unitree/baai_35340.txt | Repost of 极客公园 WeChat post; says `文章部分内容转载自公众号「顺为资本」、「Unitree 宇树科技」` → the company's own WeChat announcement exists but was NOT FETCHED (URL not found). 极客公园's fund 变量资本 is a Unitree investor (page says so). |
| 3c | Series B2 / a new funding round | nearly 1 billion yuan ($139 million) | Feb 24, 2024 05:54 AM | https://www.caixinglobal.com/2024-02-24/unitree-robotics-raises-nearly-139-million-in-series-b2-fundraising-102168284.html | 2 | raw/unitree/caixinglobal_102168284.txt | Says `led by food delivery giant Meituan`; 3a/3b say only `投资方包括美团`, no lead. Likely the same company release → may NOT be independent of 3a. Page may be paywalled; saved text is what was served. |
| 3d | (no round name) 2024 年第一次增资 | 合计 60,034.4827 (单位：万元) | 2024 年 1 月 31 日 (agreement); 2024 年 2 月 2 日 (registration) | same as 1d | 1 | raw/unitree/sse_prospectus_shenbaogao_20260320.txt | 9 new investors incl. 汉海信息 24,802.7586. **DISCREPANCY (flagged, owner decision 2026-11-13: keep both, pick neither):** press says 近10亿元人民币; prospectus 合计 is 60,034.4827 万元. Row stays unverified. A share transfer (经乾二号 → 经纬壹号/经纬叁号, 5,600.6590 万元 and 1,549.3410 万元) happened in Jan 2024 too; I did not combine any numbers. |
| 4a | C轮融资 | 数亿元人民币 | 2024.09.24 20:52 (`9月24日消息`) | https://www.tmtpost.com/7262451.html | 2? | raw/unitree/tmtpost_7262451.txt | `宇树科技对外表示不予置评`; only investor 中关村科学城 confirmed participation (no amount). Tier 2 is doubtful (company did not confirm). |
| 4b | (no round name) 2024 年第二次增资 | 合计 28,470.5173 (单位：万元) | 2024 年 8 月 31 日 (agreement); 2024 年 9 月 13 日 (registration) | same as 1d | 1 | raw/unitree/sse_prospectus_shenbaogao_20260320.txt | Investors incl. 机器人基金, 中关村科学城, 中证投资, 祥峰荣晟. **Naming conflict:** 4a calls Sept 2024 "C轮"; 5a (21jingji_20250619.txt) says the June 2025 C round `完成了去年底开启的C轮融资`. Rows 4 and 5 may be one C round in two closes, or two rounds. Owner decision. |
| 5a | C轮融资 | (none) | 2025年06月19日 17:42 | http://www.21jingji.com/article/20250619/herald/7d8d1812f1b49d121b67d929fc5f8622.html | 2 | raw/unitree/21jingji_20250619.txt | Company insider confirms: `最近确实完成了C轮融资`. No amount from the company side. |
| 5b | C轮融资 | 约7亿元人民币 | 2025年06月23日 08:38 | https://finance.sina.com.cn/roll/2025-06-23/doc-infazmip7551270.shtml | 2? | raw/unitree/sina_infazmip7551270.txt | 长江商报 on 新浪. Amount is attributed to `有消息显示` / `有报道显示`, not to the company. Also `天眼查显示，宇树科技此轮融资金额为数亿元人民币`. |
| 5c | C轮融资 | 近7亿元 | 2025年06月20日 13:03 | https://finance.sina.com.cn/tech/roll/2025-06-20/doc-infasynr2900739.shtml | 3 | raw/unitree/sina_infasynr2900739.txt | `来源：IT桔子` (aggregator). Same origin as existing raw/01_unitree_36kr.txt, which credits 晚点 LatePost (`融资金额接近 7 亿元人民币`). LatePost original NOT FETCHED. |
| 5d | C轮融资 | (none) | 2025年06月19日 17:20 | https://finance.sina.com.cn/tech/discovery/2025-06-20/doc-infaqzvp3786779.shtml | 3 | raw/unitree/sina_infaqzvp3786779.txt | 快科技 on 新浪; `该知情人事表示，“融资最近确实完成了”`. No amount. |
| 5e | (no round name) 2025 年 6 月股权增资 | 合计 69,449.6968 (增资款（万元）) | 2025 年 6 月 6 日 (agreement); 2025 年 6 月 12 日 (registration) | same as 1d | 1 | raw/unitree/sse_prospectus_shenbaogao_20260320.txt | New investors 中移和创, 腾讯科技, 无锡锦秋, 杭州灏月, 上海云玚, 合创投资 + 21 existing holders. Prospectus also: `公司最近一次市场化股权融资投前估值 120 亿元、投后估值 127 亿元`. Separate same-month 上海宇翼 (ESOP platform) 增资 of 14.4668 万元 is NOT third-party financing. |
| 6 | 新一轮融资 / 追加投资 | (none) | 7月3日 (page published 2025-07-07 13:59) | https://news.qq.com/rain/a/20250707A053XA00 | 3 | raw/unitree/qq_20250707A053XA00.txt | IT桔子 on 腾讯新闻: `7月3日，首程控股有限公司发布公告，宣布北京机器人产业发展投资基金对宇树科技进行追加投资。` The 首程控股 (0697.HK) HKEX announcement itself was NOT FETCHED (URL not found). No amount. May be part of 5e (机器人基金 appears there with 3,572.3991). |

## Scope check per round (docs/scope.md)

Common: company is in mainland China per Tier 1 (prospectus quote above).
No round is a loan, grant, IPO or M&A per the saved text.

| # | Period | Amount explicitly stated | Embodied-AI / humanoid as of round date (Tier 1) | Officially announced 2022-2025 | Result |
|---|---|---|---|---|---|
| 1 (2022 B轮系列) | Yes (2022-04-20) | **No** — `本轮系列融资合计数亿元` (pedaily_20220420_33444) is undisclosed | **No Tier 1 basis.** 投资界 text: `专注于消费级、行业级高性能四足机器人，灵巧六轴机械臂等研发、生产及销售`; no embodied-AI wording. Prospectus humanoid date is 2023-08. | Yes (company-side release, Tier 2) | **Fails.** Record as undisclosed → status excluded; gray-zone basis also missing. |
| 2 (2022 第四次增资) | Yes (agreement 2022-08-15) | Yes in prospectus (`新增 3.4288 万元注册资本由中网投资以 2,000 万元现金出资认购`) | No Tier 1 basis before 2023-08 | **No announcement found** in 2022-2025; only the 2026 prospectus | **Fails** (not announced in period; gray zone). Lead only. |
| 3 (2024 B2轮) | Yes | Yes, approx: `融资近10亿元人民币` (pedaily_202402_530406). Prospectus 合计 differs (60,034.4827 万元). | Yes: `2023 年 8 月，公司首款自研全尺寸人形机器人 H1 面市` (prospectus) | Yes (company-side, Tier 2); company WeChat Tier 1 not fetched | **Passes scope.** Amount discrepancy flagged; both figures kept; row stays unverified (owner decision 2026-11-13). |
| 4 (2024-09 C轮) | Yes | **No** — `完成数亿元人民币C轮融资` (tmtpost_7262451) | Yes (H1 2023-08, prospectus) | Doubtful: `宇树科技对外表示不予置评` | **Fails** on amount (undisclosed → excluded). Also "officially announced" not met by company. |
| 5 (2025-06 C轮) | Yes | Media yes (`约7亿元人民币`, `近7亿元`), but not from company side; company insider confirms round only. Prospectus 合计 69,449.6968 万元. | Yes (H1 2023-08, prospectus) | Company confirmed completion via insider (21jingji); no formal announcement fetched | **Passes scope on period/entity/segment.** Amount from company side not in any Tier 1/2 announcement. 5b and 5c count as ONE source (owner decision 2026-11-13); row stays unverified unless an independent source is found. |
| 6 (2025-07 追加投资) | Yes | **No** amount | Yes | Investor (首程控股) announcement reported but NOT FETCHED | **Fails** (no amount; Tier 1 not fetched). |

## Not fetched (URLs/leads that could not be saved)

- Company WeChat account 「Unitree 宇树科技」 B2 announcement (Feb 2024):
  referenced in raw/unitree/baai_35340.txt; article URL not found.
- 晚点 LatePost original C-round report (June 2025): credited in
  raw/01_unitree_36kr.txt; URL not found.
- 首程控股 HKEX announcement of 2025-07-03: URL not found on hkexnews.
- https://cn.technode.com/post/2022-04-20/unitree-robotics-series-b/ —
  HTTP 403.
- https://m.rccaijing.com/news-7246049458143294993.html (2024 C轮 lead) —
  no response.
- https://mqjwb.tidenews.com.cn/epaper/article/2025-06-25/4379734 (2025 C轮
  lead) — HTTP 405.
- https://www.fromgeek.com/retail/626569.html (B2 lead) — no response.
- https://www2.yicaiglobal.com/news/chinese-smart-robot-maker-unitree-bags-nearly-usd139-million-in-b2-fundraiser
  (B2 lead) — no response.
- Final registered prospectus (招股说明书, 2026-08-14 per search lead) — not
  fetched; the 申报稿 and 上会稿 were used instead.
- https://www.unitree.com/mobile/news/ — fetched but lists no financing
  news; not saved.

## Open questions for the owner

Former questions 1-2 and the two-source question for row 5 are resolved
(see "Owner decisions (2026-11-13)"). Still open:

1. Is Sept 2024 (增资 合计 28,470.5173 万元) part of the same C轮 as
   June 2025 (合计 69,449.6968 万元)?
2. 2022 rounds: Unitree was quadruped-only per saved sources; does it pass
   the "quadruped makers that position themselves as embodied AI" test?
   No saved Tier 1 says so for 2022.
3. Stage from the prospectus: decision 1 makes the prospectus Tier 1 for
   stage, but it never names a stage (no 轮 names in any 增资 section).
   stage_raw can therefore only come from press reports (Tier 2/3).
