# Consolidated Search Campaign — Build Blueprint (PAUSED, pending Leslie's approval)

> **Status:** designed + ready to launch. NOT yet created in the Google Ads account and NOT serving.
> **Gates before go-live:** (1) deploy landing-v2 so the 9 .ca offence pages return 200, (2) set the
> 2 conversion env vars in Vercel, (3) Leslie's explicit approval to use the .ca pages for ads.
> **Author:** Anshul session, 2026-06-26. Replaces the 4 fragmented Search campaigns.

---

## Why we're doing this (the diagnostic, in one line)

The 4 live Search campaigns spend ~$1,000/mo and produce **0 verified calls** — because their
Quality Scores are **1–3**, so they lose **60–72% of every auction to Ad Rank** and only win
**12–18% impression share**. Root cause = a dozen different-intent keywords all dumped onto a
**homepage** (no message-match) → Google scores relevance/landing-experience low → ads barely show.

**The fix:** one consolidated campaign, **single offence per ad group (SKAG)**, each ad group landing
on its **own matching blottman.ca page** → relevance ↑ → QS ↑ → win more auctions → leads. Plus a
**real conversion signal** (the .ca form tag) so bidding optimizes toward leads, not the untrusted
"Contact Us" form-fill.

---

## Campaign settings

| Setting | Value | Why |
|---|---|---|
| **Name** | `Search - Ontario Traffic Tickets (Consolidated)` | one source of truth |
| **Type / Network** | Search only — **Display Network OFF**, Search Partners OFF | search campaigns leak onto Display (we already had to fix this once) |
| **Geo** | **Ontario** (`geoTargetConstants/20121`), **PRESENCE only** | she serves all Ontario; covers GTA + the cheap small-city auctions + Cookstown/Barrie local. PRESENCE (not "presence or interest") stops out-of-province leads |
| **Language** | English | |
| **Bidding** | **Phase 1: Maximize Clicks, max-CPC cap ~$4.** Phase 2 (after the tag logs ~15–30 conversions): switch to **Maximize Conversions**, then tCPA. | a brand-new campaign + brand-new conversion signal has zero data — Max Conversions would flail. Bootstrap on clicks, graduate to conversion bidding once there's data. |
| **Budget** | **$20/day** (down from ~$30/day across the 4 old ones) | frees ~$10/day to move into PMAX (the proven engine). Scale up once QS climbs and the tag proves leads. |
| **Conversion goal** | `Submit Lead Form` (id `7173263227`) as the optimization target once live | this is the real signal the old setup never had |

---

## Ad groups — one offence each → its matching .ca page (SKAG)

Keywords are **phrase** + **exact** only (no broad — broad is what leaked parking/competitor/lawsuit
junk before). All keyword themes are drawn from the **real winning search terms** in the 30-day
diagnostic. Each ad group runs **one RSA** with the offence pinned in Headline 1.

| # | Ad group | Landing page | Keywords (phrase + exact) |
|---|---|---|---|
| 1 | **Speeding** | `/speeding` | "fight speeding ticket", "speeding ticket help", "fight my speeding ticket", [speeding ticket paralegal ontario] |
| 2 | **Careless Driving** | `/careless-driving` | "fight careless driving ticket", "careless driving ticket help", [careless driving paralegal] |
| 3 | **Stunt Driving** | `/stunt-driving` | "fight stunt driving ticket", "stunt driving ticket help", [stunt driving paralegal ontario] |
| 4 | **Cell Phone / Distracted** | `/cell-phone` | "cell phone ticket", "distracted driving ticket", "driving while on phone ticket", "phone in hand ticket", "fight distracted driving ticket" |
| 5 | **Fail to Stop / Stop Sign** | `/fail-to-stop` | "fail to stop at stop sign ticket", "stop sign ticket ontario", "failure to stop ticket", "fight a stop sign ticket" |
| 6 | **Disobey Sign** | `/disobey-sign` | "disobey sign ticket", "disobey sign ticket ontario" |
| 7 | **No Insurance** | `/no-insurance` | "no insurance ticket", "without insurance ticket", "fighting no insurance ticket ontario" |
| 8 | **Driving Under Suspension** | `/driving-under-suspension` | "suspended license ticket ontario", "driving under suspension ticket", "drive while suspended ticket" |
| 9 | **No Licence** | `/no-licence` | "no licence ticket", "driving with no licence ticket", "fail to surrender licence" |
| 10 | **General / Fight Ticket** | `/` (homepage) | "how to fight a traffic ticket", "traffic ticket paralegal", "fight traffic ticket ontario", "traffic ticket defence ontario", "ontario traffic ticket dispute", "traffic ticket legal help" |

> Note on **"how to fight a ticket"** (1,302 impr, QS 1, DIY-leaning): kept in the General group, but
> the homepage's "we fight it *for* you / free case review" message-match should lift it off QS 1.
> Watch it; if it stays QS 1 and only pulls DIY/no-hire clicks, pause it.

---

## RSA copy (proven structure, LSO + policy compliant)

**Rules baked in:** she's a **paralegal, never "lawyer"**; **no "98% win rate" / "#1" / guarantees**
(the exact claims that got the account flagged for clickbait); paralegal-accurate, verified signals
only ("Licensed Ontario Paralegal", "500+ tickets handled" — both confirmed true).

**Per ad group — Headline 1 (pinned, slot 1)** = the offence, e.g.
`Fight Your Speeding Ticket`, `Fight a Careless Charge`, `Fight a Stunt Driving Charge`, etc.
(pin slot 1 only, for Quality Score — let Google rotate the rest, per best practice).

**Shared headline pool (reused across ad groups, 14 of the 15 slots):**
- Licensed Ontario Paralegal
- 500+ Traffic Tickets Handled
- Free Case Review Today
- Protect Your Driving Record
- Avoid Costly Demerit Points
- Keep Your Insurance Low
- Most Clients Never Go To Court
- We Deal With The Court For You
- Serving All Of Ontario
- Affordable Flat-Fee Defence
- Skilled Ticket Defence Team
- Call For A Free Consultation
- Don't Just Pay The Fine
- Fast, Confidential Help

**Shared descriptions (4):**
1. Licensed Ontario paralegal fighting traffic tickets to protect your record and insurance. Free case review.
2. We handle the paperwork and court so you don't have to. 500+ tickets handled across Ontario.
3. Fight your ticket and the demerit points that raise your insurance for years. Talk to us free.
4. Affordable flat-fee defence. Most clients never set foot in court. Get your free case review today.

> The `/generate-ads` skill validates every line to char limits + editorial rules before publish;
> the build script runs that validation so nothing ships over-length or off-policy.

---

## Negatives & assets (reuse what exists — don't rebuild)

- **Negatives:** attach both shared lists — **Master Negatives** (`12109076551`, ~85 keywords:
  parking, competitors, lawsuit/civil, immigration, DIY) + **neg list** (`11960214627`). These already
  block the junk that leaked before.
- **Lead form:** attach the existing approved asset **`371903420556`** (Free Case Review).
- **Call asset:** the live `(647) 794-7750` call asset.
- **Sitelinks:** the per-offence sitelinks → point at the matching .ca pages (Speeding, Careless,
  Stunt, Cell Phone, Suspended, Free Consultation).
- **Callouts:** "Licensed Ontario Paralegal", "Free Case Review", "500+ Tickets Handled",
  "Serving All Ontario" (no win-rate callouts).

---

## Conversion tracking — already code-complete in landing-v2 ✅

The .ca form already fires the Google Ads conversion on submit (`QuoteForm.tsx`) and loads gtag
(`layout.tsx`). It's **off until two Vercel env vars are set** — that's the entire unlock:

| Vercel env var | Value |
|---|---|
| `NEXT_PUBLIC_GADS_ID` | `AW-11165656868` |
| `NEXT_PUBLIC_GADS_CONVERSION` | `AW-11165656868/RcgyCPuevdwaEKTOmcwp` (= the `Submit Lead Form` action) |

Set those → redeploy → every .ca form submit registers as a real `Submit Lead Form` conversion.
(Optional later: `NEXT_PUBLIC_GADS_CALL_CONVERSION` for website-call tracking + OCI via the captured gclid.)

---

## Launch runbook (the proven order — do NOT reorder)

1. **Deploy landing-v2** → verify each of the 9 offence routes + homepage returns **200**
   (`/speeding`, `/careless-driving`, `/stunt-driving`, `/cell-phone`, `/fail-to-stop`,
   `/disobey-sign`, `/no-insurance`, `/driving-under-suspension`, `/no-licence`, `/`).
2. **Set the 2 Vercel env vars** above → redeploy → test a form submit with `?gclid=test123`,
   confirm the conversion shows "Recording" in Google Ads within a few hours.
3. **Get Leslie's approval** to use the .ca pages for ads (frame: "ad landing pages we fully control,
   LSO-clean — not the SEO branch-out you paused").
4. **Create the campaign** (build script) → it comes up **PAUSED**; ads land on the now-live pages →
   approve clean (no "destination not working").
5. **Enable**, and **pause the 4 old Search campaigns** (Traffic ticket lawyer, broad, Lower Value-New,
   Higher Value-New). Move the freed ~$10/day into PMAX - Blottman Max.
6. **Watch 1 week:** Quality Scores should climb out of 1–3 as the pages match the keywords; the
   `Submit Lead Form` action should start recording. Once it logs ~15–30 conversions → switch bidding
   to Maximize Conversions.

---

## Budget after the swap (total stays at the $100/day target)

| Campaign | Before | After |
|---|---|---|
| PMAX - Blottman Max | $65 | **$75** (the proven engine gets the freed Search $) |
| **Consolidated Search (new)** | — | **$20** |
| Blottman New pM | $5 | $5 |
| ~~Traffic ticket lawyer~~ | $12 | paused |
| ~~TTL broad~~ | $5 | paused |
| ~~Lower Value - New~~ | $8 | paused |
| ~~Higher Value - New~~ | $5 | paused |

⚠️ **Coordination:** the 4 campaigns being retired are Akash's builds — give him a heads-up before
pausing (last-save-wins). Nothing here is destructive: old campaigns are paused (not deleted) and the
new one launches paused, so every step is reversible.
