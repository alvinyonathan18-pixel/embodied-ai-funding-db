# UNVERIFIED LEADS

Company: 穹彻智能 (company-slug: noematrix)

LEADS ONLY. Nothing here is entered in Rounds/Sources and nothing is
verified. Values are copied exactly as written in the saved pages. Every
backtick quote below is meant to be a verbatim substring of the named file
in `raw/noematrix/` (checked by script on the access date). Access date for
all files: 2026-11-13. Source log: `data/raw_sources.md`.

Tier guess uses docs/data_dictionary.md Rule 1 (1 = company/investor
announcement, regulator filing; 2 = major media quoting the company side;
3 = aggregator/database). Self-media contributor accounts (钛媒体钛度号,
澎湃号, 36氪 reposts of WeChat accounts, 鉅亨號) are guessed Tier 3.

## Tier 1 source: the company website (www.noematrix.ai)

The company's own website has a news page for each in-period round. These
are the Tier 1 files. The company's WeChat posts were NOT fetched (no
article URLs were found).

Caveat on dates: the article pages show no date in their visible text,
except the Pre-A++ page, whose body text states one. The dates come from
the news list on `company_about.txt`. The page metadata (`__NEXT_DATA__`
in the saved HTML) shows the pages were created on the site AFTER their
publish date: for example, the Pre-A+ page has `publish` 2024-12-05 but
`createTime` 2025-05-09, and the Pre-A page has `publish` 2024-09-06 but
`createTime` 2024-09-13. So the company pages may not be the earliest
dated report. The media copies below carry their own publish times.

## Leads table

| # | stage_raw as seen | amount_raw as seen | date as seen | url | tier guess | saved_file | attribution as seen | notes |
|---|---|---|---|---|---|---|---|---|
| 1a | 天使轮和Pre-A轮两轮融资 | 累计数亿元人民币 | 9月6日 (body); `2024年9月6日` (news list on company_about.txt) | https://www.noematrix.ai/news/noematrix_pre-a | 1 | raw/noematrix/company_news_pre-a.txt | 穹彻智能…宣布 | Quote: `9月6日，具身智能领域初创公司穹彻智能（Noematrix，上海穹彻智能科技有限公司）宣布完成累计数亿元人民币的天使轮和Pre-A轮两轮融资。` Two rounds announced together with ONE combined amount. Page title says `穹彻智能完成Pre-A轮融资获数亿元`. |
| 1b | 天使轮和Pre-A轮两轮融资 | 累计数亿元人民币 | 9月6日消息; page `更新于：2024-09-06 09:50` | https://news.pedaily.cn/202409/539673.shtml | 2 | raw/noematrix/pedaily_202409_539673.txt | 穹彻智能…宣布; `来源：投资界讯` | Quote: `投资界（ID：pedaily2012）9月6日消息，具身智能领域初创公司穹彻智能（Noematrix，上海穹彻智能科技有限公司）宣布完成累计数亿元人民币的天使轮和Pre-A轮两轮融资。` Text is near-identical to 1a, so it likely copies the same release: NOT independent of 1a. (An earlier copy of this page exists as raw/05_noematrix_pedaily.txt; the files differ in extraction, not checked further.) |
| 1c | 天使轮和Pre-A轮两轮融资 | 累计数亿元人民币 | `新华财经上海9月6日电`; URL path 20240906 | https://www.cnfin.com/gs-lb/detail/20240906/4100432_1.html | 2 | raw/noematrix/cnfin_20240906_4100432.txt | `记者6日获悉` | Quote: `新华财经上海9月6日电（记者 郭慕清）记者6日获悉，具身智能领域初创公司穹彻智能已完成累计数亿元人民币的天使轮和Pre-A轮两轮融资。` Own reporter, own wording: best candidate for an independent second source. |
| 1d | 天使轮加Pre-A轮融资 | 数亿元 | page date `2024-09-11` | https://www.36kr.com/p/2944184307374722 | 3 | raw/noematrix/36kr_2944184307374722.txt | `本文来自微信公众号“铅笔道”（ID：pencilnews）` | Quote: `近日，上海穹彻智能科技有限公司（下称穹彻智能）宣布完成数亿元天使轮加Pre-A轮融资。` Repost of a WeChat account. |
| 1e | Pre-A轮 (title); 天使轮和Pre-A轮两轮融资 (body) | 累计数亿元人民币 | `2024.09.06 10:59` | https://www.tmtpost.com/7240663.html | 3 | raw/noematrix/tmtpost_7240663.txt | `钛媒体消息`; `本内容来源于钛媒体钛度号` | Title: `穹彻智能完成数亿元Pre-A轮融资`. Self-media account; text copies the release. |
| 1f | 天使轮 | `具体金额未披露` | `2024年3月27日` | https://www.cls.cn/detail/2173531 | 2 | raw/noematrix/cls_2173531.txt | `根据公开信息` | Background in the Oct 2025 article: `穹彻智能首轮天使轮融资，发生于2024年3月27日，具体金额未披露`. No standalone 2024-03 announcement found. Says when the angel round happened, not when it was announced. |
| 2a | Pre-A+轮 | 数亿元人民币 | 12月5日 (body); `2024年12月5日` (news list on company_about.txt) | https://www.noematrix.ai/news/noematrix_pre-a+ | 1 | raw/noematrix/company_news_pre-a-plus.txt | 穹彻智能（Noematrix）宣布 | Quote: `12月5日，具身智能初创公司穹彻智能（Noematrix）宣布完成数亿元人民币Pre-A+轮融资` Lead: `本轮融资由红杉中国领投`. |
| 2b | Pre-A+轮 | 数亿元人民币 | `2024-12-05 16:38:48` | https://m.chinaventure.com.cn/news/108-20241205-384170.html | 2 | raw/noematrix/chinaventure_20241205_384170.txt | 穹彻智能（Noematrix）宣布 | Same headline and text as 2a: NOT independent of 2a. |
| 2c | Pre-A+轮 | 数亿元人民币 | page date `2024-12-05` | https://www.36kr.com/p/3065605732541830 | 2 | raw/noematrix/36kr_3065605732541830.txt | 穹彻智能近日宣布; `本文由「胡依婷」原创出品` | Quote: `穹彻智能近日宣布完成了数亿元人民币Pre-A+轮融资，由红杉中国领投` 36氪 staff article with own wording: candidate independent second source. |
| 2d | Pre-A+轮 | 数亿元 | `2024-12-05 15:17` | https://m.thepaper.cn/newsDetail_forward_29556165 | 3 | raw/noematrix/thepaper_29556165.txt | `可靠信息显示`; 新智元 (澎湃号) | Quote: `穹彻智能再次完成数亿元Pre-A+轮融资` Self-media. |
| 2e | Pre-A+轮 | 数亿元 | `2024-12-06 12:50` | https://hub.baai.ac.cn/view/41612 | 3 | raw/noematrix/baai_41612.txt | `以下文章来源于mp.weixin.qq.com`; `可靠信息显示` | Repost of the same 新智元 article as 2d: one source with 2d. |
| 3a | Pre-A++轮 | 数亿元 | `2025年4月10日` (stated in body) | https://www.noematrix.ai/news/noematrix-pre-a++ | 1 | raw/noematrix/company_news_pre-a-plusplus.txt | 穹彻智能宣布 | Quote: `2025年4月10日，穹彻智能宣布，公司成功完成数亿元Pre-A++轮融资。` No lead investor named (`新晋吸引了盛宇投资、清科创投、嘉御资本、云启资本、上海科创集团等`). |
| 3b | Pre-A++轮 | 数亿元 | 4月10日消息; `更新于：2025-04-10 09:36` | https://news.pedaily.cn/202504/548157.shtml | 2 | raw/noematrix/pedaily_202504_548157.txt | 穹彻智能近日宣布; `来源：投资界讯` | Quote: `穹彻智能近日宣布，公司成功完成数亿元Pre-A++轮融资。` Copies the release: NOT independent of 3a. |
| 3c | Pre-A++輪 (traditional characters) | 數億元 | `2025/04/10` | https://hao.cnyes.com/post/144373 | 3 | raw/noematrix/cnyes_144373.txt | `硬氪獲悉` | Quote: `硬氪獲悉，具身智能企業「穹徹智能」近日完成數億元Pre-A++輪融資` Traditional-Chinese repost of a 硬氪 (36氪) article on 鉅亨號. The 硬氪 original was not found; this could be an independent second source but it is a repost. |
| 4 | Pre A+++轮 | (none) | (none) | https://www.noematrix.ai/news/noematrix-alibaba | 1 | raw/noematrix/company_news_alibaba.txt | company page (background) | Mentioned only as history: `此前完成了数亿元Pre-A++轮及Pre A+++轮融资`. That `数亿元` is shared with Pre-A++, so no amount is attributed to Pre A+++ alone. No announcement, date or investors were found. |
| 5a | 新一轮融资 | (none) | `2025年10月17日` (news list on company_about.txt); page metadata `publish` 2025-10-17 | https://www.noematrix.ai/news/noematrix-alibaba | 1 | raw/noematrix/company_news_alibaba.txt | 穹彻智能于近日宣布 | Quote: `穹彻智能于近日宣布完成新一轮融资，由阿里巴巴集团投资，多位老股东追投。` No amount and no stage. Company says `投资` (not 领投). |
| 5b | 新一轮融资 | (none) | 10月17日消息; `更新于：2025-10-17 09:22` | https://news.pedaily.cn/202510/555985.shtml | 2 | raw/noematrix/pedaily_202510_555985.txt | 穹彻智能于近日宣布; `来源：投资界讯` | Copies 5a: NOT independent. |
| 5c | 新一轮融资 | (none) | page date `2025-10-17` | https://www.36kr.com/p/3512926271806337 | 2 | raw/noematrix/36kr_3512926271806337.txt | 穹彻智能于近日宣布; `本文由「36氪产业创新」原创出品` | Text identical to 5a: NOT independent. |
| 5d | 新一轮融资 | (none) | `2025-10-18 17:27`; `《科创板日报》10月18日讯` | https://www.cls.cn/detail/2173531 | 2 | raw/noematrix/cls_2173531.txt | 上海穹彻智能科技有限公司…宣布; `（记者 李佳怡）` | Headline says `阿里领投`; body says `由阿里巴巴集团投资`. Disagreement on the lead role, not on amount (no amount in either). |
| 5e | 新一轮融资; `第六轮融资` | (none for the round); `累计融资额已超过10亿元人民币` (cumulative) | `2025.10.23 11:12` | https://www.tmtpost.com/7735591.html | 3 | raw/noematrix/tmtpost_7735591.txt | `本内容来源于钛媒体钛度号` | Says `由阿里巴巴集团领投`. The 10亿元 figure is cumulative (累计), not this round; never use it as the round amount. |

### Out of period (reference only, not leads for 2022-2025)

- A轮, company page dated `2026年2月10日` on company_about.txt
  (`本轮融资金额达数亿元人民币，由C资本领投`). Not saved as its own file.
- 2026-06 round led by 无锡数据集团: raw/noematrix/163_KVMQ0ES005118DFD.txt
  (硬氪, `2026-06-18 09:30`), and listed on company_about.txt
  (`2026年6月18日`). Out of the period; saved before the date was known.

## Scope check per round (docs/scope.md)

Common facts:

- Segment (embodied-AI "brain" company): Tier 1 quotes as of each round
  date are listed per row below.
- Mainland China: **met by a Tier 1 quote.** Owner decision 2026-11-13: a
  legal name containing 上海 is NOT enough; an explicit registration or HQ
  statement is needed. The company's privacy policy (company_privacy.txt,
  https://www.noematrix.ai/legal/privacy) states the registered address:
  `上海穹彻智能科技有限公司为穹彻智能官方网站的运营主体，亦是您个人信息的控制者，注册地址为上海市闵行区东川路555号丙楼4089室。`
  The policy is dated before all in-period rounds:
  `本政策制定于2024年6月28日，于2024年6月30日正式生效。` Caveat: this is
  the page as fetched on 2026-11-13; the address as of each round date is
  not shown separately. The contact page (company_contact.txt) shows no
  address. The `上海穹彻智能科技有限公司` name alone (company_news_pre-a.txt)
  is not used as the basis.
- No round is a loan, grant, IPO or M&A per the saved text.

| # | Round | Period (2022-2025) | Amount explicitly stated | Embodied-AI basis (Tier 1, as of round date) | Result |
|---|---|---|---|---|---|
| 1 | 天使轮 + Pre-A轮 (2024-09-06) | Yes: `2024年9月6日` (company_about.txt) | **No**: `累计数亿元人民币` = no specific number, so undisclosed. It is also one combined figure for two rounds. | `致力于研发具身智能系统及其相关工具与平台` (company_news_pre-a.txt) | **Fails on amount.** Record as undisclosed, status excluded. Two rounds in one announcement: owner to decide if this is one row or two. |
| 2 | Pre-A+轮 (2024-12-05) | Yes: `2024年12月5日` | **No**: `数亿元人民币` | `穹彻智能专注具身智能基础模型和系统的研发` (company_news_pre-a-plus.txt) | **Fails on amount.** Undisclosed, so excluded. |
| 3 | Pre-A++轮 (2025-04-10) | Yes: `2025年4月10日` | **No**: `数亿元` | `穹彻智能的核心产品——穹彻具身大脑（Noematrix Brain）` (company_news_pre-a-plusplus.txt) | **Fails on amount.** Undisclosed, so excluded. |
| 4 | Pre A+++轮 (date unknown) | Unknown: no date found | **No** | (same company pages) | **Fails**: not officially announced as a round in any saved file; no date, no amount. Lead only. |
| 5 | Alibaba 新一轮融资 (2025-10-17) | Yes: `2025年10月17日` | **No**: no amount at all | `公司以基于力的具身智能大脑技术为核心` (company_news_alibaba.txt) | **Fails on amount.** Undisclosed, so excluded. |

Result: 穹彻智能 adds **0 rows that could count toward the 30-row target**.
All in-period rounds are 数亿元 or have no amount. Under docs/scope.md
they are still recorded as rows with amount_status = undisclosed and
status = excluded (rows 1, 2, 3, 5; row 4 has no announcement).

## Independent second source per round

| Round | Tier 1 | Best independent candidate | Same-origin copies (count as one with Tier 1) |
|---|---|---|---|
| 1 | 1a | 1c 新华财经 (own reporter) | 1b, 1e (release text); 1d is a WeChat repost |
| 2 | 2a | 2c 36氪 (staff article, own wording) | 2b; 2d and 2e are one 新智元 article |
| 3 | 3a | 3c 硬氪 via 鉅亨號 (repost) | 3b |
| 4 | (background only) | none | 5b, 5c repeat the same sentence |
| 5 | 5a | 5d 科创板日报 (own reporter) | 5b, 5c |

## Not fetched

- Company WeChat account posts for all rounds: no article URLs found.
- The 硬氪 / 36氪 original of 3c: URL not found (only the 鉅亨號 repost was
  saved).
- Investor announcements (红杉中国, Prosperity7, 广发信德, 小苗朗程,
  阿里巴巴): none found. https://www.hongshan.com/news returned 404; the
  newsroom was not searched further.
- A standalone announcement of the angel round (2024-03, per 1f): none
  found.
- https://www.noematrix.com/ is a placeholder page, not the company site;
  not saved.

## Open questions for the owner

1. (Resolved 2026-11-13: an explicit HQ or registration statement is
   needed. One was found in company_privacy.txt; see Scope check.)
2. Round 1 is two rounds (天使轮, Pre-A轮) announced together with one
   combined amount. One row or two? The angel round may have closed
   2024-03-27 (1f), but it was first announced 2024-09-06.
3. The company pages were created after their stated publish dates (page
   metadata). For announce_date, is the company page date usable, or
   should the earliest dated media report be used? Here they agree: 1b
   `2024-09-06 09:50`, 2b `2024-12-05 16:38:48`, 3b `2025-04-10 09:36`,
   5b `2025-10-17 09:22`.
