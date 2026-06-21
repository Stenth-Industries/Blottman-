# CLAUDE.md — Blottman Law Google Ads

> Shared project context for **Kushagra (info@stenth.com)** and **Akash**, working the
> Blottman Law Google Ads account together from separate computers on the same Claude account.
> Keep this file in a synced folder (Google Drive / OneDrive / private Git) so both of our
> Claude Code instances read the same context. **When something material changes in the
> account, update this file** — it is the single source of truth, not either machine's local memory.

## How we work as a team

- **Same Claude login ≠ shared memory.** Each computer's Claude has its own local memory. This
  `CLAUDE.md` is what keeps us in sync — update it after meaningful changes.
- **Google Ads access:** both of us are users on the account (Admin/Standard). Google Ads has no
  edit-lock — last save wins. So we split lanes to avoid undoing each other.
- **Lane split (adjust as needed):**
  - **Kushagra:** PMAX campaigns, budgets, bidding strategy.
  - **Akash:** conversion tracking, stenth $500 tracker, creative/assets.
  - Use Google Ads **change history** to see who changed what.
- **Billing/limits:** usage limits are per Claude account (shared pool). Heavy simultaneous use
  burns the shared rate limit faster — coordinate big batch jobs.
- **Log changes here** with date + who, so the other person (and the other Claude) stays current.

## The client

**Blottman Law** — traffic-ticket lawyer, Ontario Canada.
- **Converting geos (GTA):** Toronto, Brampton, Mississauga, Hamilton.
- **Dead geos (spend, 0 conv):** Vaughan, Markham, London, Cambridge, Orillia → trim these.
- **Office location: Cookstown** (Innisfil/Barrie area, ~60–70km N of Toronto, NOT in GTA). Current Search
  geo targeting does NOT cover her local area; nearby Orillia (north) is a dead geo. As a paralegal she
  serves all Ontario, so office ≠ targeting limit. **Open Q: add a local Cookstown/Barrie radius, or stay GTA-only?**
- **Practice areas:** careless driving, speeding, stunt driving, cell phone, suspended license.
  **NOT parking** (parking leads are off-target — see Parking note below).
- **Google Ads customer ID:** `8586214705`
- **Project dir:** `E:\Blottman-law` (this folder). Not a git repo. Google Ads API creds in `.env`.

## Account state (as of 2026-06-10)

- **30-day:** ~$3,099 spend, 27 conversions, **$114.77 CPA**.
- Bidding: Max Conversions (count-based, conv_value $0).
- **Budget target: ~$75/day (~$2.3K/mo).** User flagged prior >$100/day spend (inflated by
  now-paused search campaigns + multiple PMAX + PMAX 2x daily overspend), hence the cap.
  Budgets are monthly averages (daily budget × 30.4).

### Live PMAX campaigns (3, after consolidation)
| Campaign | Campaign ID | Budget res | Daily |
|---|---|---|---|
| **PMAX - Blottman Max** (the winner, ~$50 CPA) | `22979153470` | `14910424501` | $50 |
| PMAX #2 | `23753177178` | `15507596328` | $15 |
| PMAX #3 | `23757095274` | `15505656719` | $10 |

- **Paused 2026-06-10:** "Blottman New pM" (`23712330618`) — the dog, $139 CPA, 46k impr, 0.96% CTR.
- **Search/SKAG campaigns** (Higher Value, Lower Value, Traffic ticket lawyer): built but **PAUSED**.
- Mobile = 25 of 27 conv. Tablet burns ~28k impr for $0 (candidate to trim).

### Winner asset group `6607110351` (PMAX - Blottman Max)
- Text is strong (21 headlines, 8 long, 6 desc). Fixed typo → "500+ Car Ticket Cases Handled".
- **Added 2026-06-10:** 20 search themes (traffic/speeding/careless/stunt driving etc. — also the
  durable fix for parking wandering) + 1 audience signal (search-intent custom segment
  `customAudiences/985953263` → audience `350072492`).
- **Deliberately excluded** 'Customer List Aug 25' CRM list (`9192269431`) — unknown provenance, unused.
- Brand assets (business name, logos, sitelinks, callouts) live at **campaign level** via Brand
  Guidelines, not asset-group level.
- **STILL MISSING:** marketing images are thin (1 landscape + 1 square, 0 portrait, 0 video).
  **Need brand creative files from client.**

## Conversion tracking (it's a junk drawer)

- ~25 actions, a dozen enabled, overlapping (6+ call actions), inconsistent values (0/1/10/$500).
- Only **`Calls from Smart Campaign Ads`** (27) counts as "Conversions."
- 165 "Contact Us"/mo (codeless, CONTACT category) treated as secondary.
- **⚠️ The real money signal — `Inbound call - Blottman (stenth)` $500 call tracker — is NOT firing
  (0 in 30d)** despite being wired 2026-06-09. Brand-new or misconfigured. **Get this firing.**
  - Open question: does stenth fire on *every* call or only *booked* consults? The $500 value
    should attach to **booked consults only**.

## Strategy / blueprint

User wants to optimize toward **calls + form submits + booked consults** (downstream → needs
Offline Conversion Import + value-based bidding). The stenth $500 tracker is intentional.

**~~Website / landing pages are being rebuilt — ready ~July 1–5 2026.~~ CANCELLED 2026-06-12 —
client backed off the rebuild (unhappy with results). Phase 1 re-scoped to the EXISTING blottman.com:
conversion cleanup is Google-Ads-side anyway; form/call tracking + gclid capture = small GTM/tag edits
to the current site (need site access); SKAGs can launch against existing `/traffic-tickets` pages.**

- **Phase 0 (now → ~Day 25, no site needed):** consolidate PMAX for learning density, reallocate
  budget to winner, trim dead geos + tablet, **get stenth firing**, stay count-based.
- **Phase 1 (site live):** clean conversion spec (call + form primary, Contact Us secondary $0) +
  gclid capture for OCI; launch Search/SKAG per `prompts.md` playbook.
- **Phase 2 (a campaign >30 conv/mo):** switch to Max Conversion Value / tROAS with $500-weighted
  booked-consult values.

### Next actions (from 2026-06-10)
1. Watch **PMAX - Blottman Max** 5–7 days — does it hold ~$50 CPA at the new $50 budget?
2. Step 3: taper #2/#3 budgets into Max.
3. Step 4: geo trim (drop Vaughan/Markham/London/Cambridge/Orillia).
4. Get the stenth $500 tracker firing.
- Reminder set ~Jun 15 in `REMINDER.md` (Google Calendar MCP was offline).

## Parking-leads issue (resolved 2026-06-10)

Client saw parking-ticket leads from PMAX - Blottman Max. Root cause was **~90% historical** —
parking negatives added Jun 7, but the client's screenshot was a May 13–Jun 9 report (mostly
pre-fix). Post-fix (Jun 8–10): **0 parking conversions.**
- All live campaigns have parking negatives (direct + shared lists
  'Master Negatives - Blottman (Stenth)' `12109076551` + 'neg list' `11960214627`).
- blottman.com has no parking content.
- Residual "parking ticket lawyer toronto" appears because PMAX search-term **insight categories**
  are Google semantic groupings, not literal queries — negatives can't block a category.
- True fix for residual = turn OFF Final URL Expansion (**UI only** — `url_expansion_opt_out` was
  removed from the Campaign resource in google-ads lib v31 / API v24, can't set via API).

## Scripts in this folder

| File | Purpose |
|---|---|
| `audit.py` | Account audit via Google Ads API |
| `today.py` | Today's performance pull |
| `impr_diag.py` | Impression diagnostics |
| `stenth_watch.py` | Daily call-conversion monitor (watch for the $500 tracker firing) |
| `test_connection.py` | API connection check |
| `get_refresh_token.py` | OAuth refresh token helper |
| `prompts.md` | Search/SKAG launch playbook |
| `build-your-first-skag.md`, `campaigns.md` | Campaign build notes |
| `SETUP.md` | Environment / API setup |
| `REMINDER.md` | Follow-up reminders (Calendar MCP fallback) |
| `credentials.json`, `.env` | API creds — **do not commit to any public repo** |

> ⚠️ If you sync this folder to share context, **exclude `.env` and `credentials.json`** from any
> public/Git location. Keep secrets out of shared cloud links that aren't private.

## ⚠️ INCIDENT — calls went dark Jun 9–11 (diagnosed + fixed 2026-06-11)

Client reported no calls for ~3 days. Root cause confirmed (API + UI screenshot):
- Delivery collapsed: impr Jun 9 **721** → Jun 10 **66** → Jun 11 **0**. Clicks 67→17→2. NOT a
  tracking glitch — real delivery stopped. Account itself is ENABLED (no billing/suspension).
- All 3 live PMAX = `primary=LIMITED`, reasons **BUDGET_CONSTRAINED + HAS_ASSET_GROUPS_LIMITED_BY_POLICY**.
  Note: Jun 10 spent only $14 of $75 cap → budget was NOT the binding limit; the policy limit was.
- Winner asset group `6607110351` = `ASSET_GROUP_LIMITED`. Policy topic on assets:
  **`COMMISSION_OF_A_CRIME_IN_PERSONALIZED_ADS`** (Google personalized-ads policy for legal/criminal
  content). UI message: *"Remove either the content related to this topic, or the personalized targeting."*
- **Trigger = the Jun 10 audience signal.** Adding personalized targeting to a legal/"crime" asset
  group walked us into the exact policy that throttles personalized delivery → asset group limited →
  delivery cliff. Compounded by 3 bid-strategy learning resets in 48h (conv-goal Jun 9, budget cut +
  asset edits Jun 10).
- **FIX (2026-06-11): removed the audience signal** `audiences/350072492` from asset group `6607110351`
  (kept all 20 search themes). Can't remove the legal content (it's the business), so removed the
  personalized targeting per Google's own remediation. Did NOT appeal (policy is correctly applied).
- **Status right after removal: still reads LIMITED — propagation lag (hrs→~24h), expected.** Assets
  keep the policy-topic label (harmless content classification); what matters is the throttle trigger
  is gone.
- **NOW: FREEZE all edits 48–72h** to let it exit learning. Recheck with `campaign_status.py`,
  `calls_diag.py`, `stenth_watch.py`. Open follow-up still pending: stenth $500 action is a *primary*
  conversion but fires 0 — consider de-prioritizing it once calls recover (separate change, don't
  stack it now).
- Diagnostic scripts added this session: `calls_diag.py`, `conv_actions.py`, `campaign_status.py`,
  `asset_policy.py`, `remove_audience_signal.py`.

## Change log
- **2026-06-10** (Kushagra): Consolidation steps 1–2 — paused "Blottman New pM"; raised
  PMAX - Blottman Max $36→$50; set #2 $15, #3 $10 ($75/day cap). Asset-group fixes (search themes,
  audience signal, headline typo). Parking issue diagnosed as historical.
- **2026-06-11** (Kushagra): Created this CLAUDE.md for shared Kushagra/Akash team context.
- **2026-06-11** (Kushagra): Diagnosed the no-calls incident (above) and removed the audience signal
  from asset group `6607110351` to lift the policy limit. Freeze in effect through ~Jun 13–14.
- **2026-06-11** (Kushagra + Akash): Client messaged needing leads NOW; PMAX recovery takes days, so
  enabled paused Search campaign **`Traffic ticket lawyer broad`** (id `23039650759`) as an emergency
  lead tap (Search sidesteps the personalized-ads policy that throttled PMAX). Config applied before
  enabling: budget $10.10→**$30/day** (budget res `14945220177`); added geo targeting (had NONE) =
  Toronto/Brampton/Mississauga/Hamilton, **PRESENCE-only**; CPC ceiling $0→**$10**; both negative
  shared lists already attached; 1 RSA approved; call asset (647) 794-7750 live. **NEXT: taper this
  $30/day down as PMAX recovers to keep total ≤ ~$75/day; watch CPC/quality on the single RSA.**
  Scripts added: `search_campaigns.py`, `inspect_ttlb.py`, `geo_and_ad.py`, `enable_ttlb.py`.
- **2026-06-11** (Kushagra): Added `/generate-ads` skill (`.claude/skills/generate-ads/SKILL.md`) — generates
  policy-compliant RSAs + assets from `anatomy-of-a-good-ad.md` + `ad-assets-best-practices.md`,
  validates to Google's editorial rules, never publishes without human approval. Both Akash and Kushagra
  can run it via `/generate-ads`.
- **2026-06-11** (Kushagra): Published **RSA #2** (ad `812451424746`, ENABLED) to ad group `186398312300`
  in `Traffic ticket lawyer broad` — 15 headlines (3 keyword pinned slot1) + 4 descriptions, angle =
  record/points/insurance protection, final URL **`blottman.com/traffic-tickets`** (better message-match
  than homepage; site has dedicated per-ticket pages). Added 6 campaign sitelinks (Careless Driving,
  Speeding, Stunt Driving, Cell Phone, Suspended Licence, Free Consultation). NOTE: campaign already had
  5 sitelinks → now 11 total, with a **duplicate "Cell Phone Ticket"** to dedupe. Existing RSA #1 still
  has issues (14 headlines, none pinned, "98% Win Rate" claim, DUI off-area) — rebuild later. Scripts:
  `existing_rsa.py`, `validate_rsa.py`, `publish_rsa_sitelinks.py`, `verify_publish.py`.
- **2026-06-11** (Kushagra): Rebuilt RSA #1 → new ENABLED ad `812451172230` (court/defence angle: "we attend
  court for you / don't just plead guilty", final URL `/traffic-tickets`); **PAUSED** old ad `774748697421`
  (98% Win Rate + DUI). Removed the duplicate empty "Cell Phone Ticket" sitelink. Ad group now runs 2 clean
  RSAs (record angle 812451424746 + court angle 812451172230) on distinct angles; campaign has 10 sitelinks.
  **STILL TO CLEAN: "Hov Ticket" + "Traffic Violations" sitelinks contain the "98% Win Rate" claim** in
  their descriptions (asset ids 322570766588, 322570766597). Scripts: `inspect_sitelinks.py`, `rebuild_rsa1.py`.
- **2026-06-11** (Kushagra): Checked the now-live `Traffic ticket lawyer broad` Search campaign. It IS serving
  & eligible but **converting weak**: ~$141 spent / ~50 clicks / **1 conv** over ~2wk (history runs back to
  ~May 28, NOT freshly enabled today as the earlier log implied — verify in change history). Not budget-bound
  (lost-budget 0.4%) — losing **83% impr share to RANK** (low QS, mostly 0/2–4). Search terms leaking
  **parking + competitor-name** queries past the negatives → add as negatives (staged, not yet applied).
  Scripts: `ttlb_perf.py`, `ttlb_now.py`.
- **2026-06-11** (Kushagra): Ad-group `186398312300` cleanup. Found old **`774748697421` (98% Win Rate + DUI)
  was ENABLED again** — the Jun-11 pause had been reverted (last-save-wins; likely Akash). Re-paused it.
  Ran `/generate-ads` to lift the Average court/defence RSA to Excellent: **created new ENABLED RSA
  `812455198290`** (court/defence, `/traffic-tickets`, 15 H w/ 3 pinned slot-1, 4 D, 6/6 patterns, no
  superlatives/DUI) and **PAUSED** the old Average ad `812451172230`. Enabled RSAs now = `812451424746`
  (record angle) + `812455198290` (court angle); both in editorial review. ‹VERIFY› LSO-licence claim +
  "500+ ticket cases" wording. Script: `publish_rsa_refresh.py` (validates char limits + pin count locally).
  **VERIFY RESOLVED (Kushagra confirmed): she IS LSO-licence verified and HAS handled 500+ ticket cases →
  both claims true, no copy change.**
- **2026-06-11** (Kushagra): Closed competitor search-term leaks on `Traffic ticket lawyer broad`. Parking was
  already broad-covered (`[BRO] parking` blocks all parking queries; earlier leaked impr were pre-fix), so
  left as-is. Real leak = competitor brands listed EXACT-only (variants slipped) or absent. Added 5
  **campaign-level PHRASE negatives**: `amar traffic tickets`, `benito zappia`, `x copper`, `ex copper`,
  `xcopper`. Scripts: `dump_negatives.py`, `add_competitor_negs.py`. (Option later: promote these to the
  shared `Master Negatives` list so PMAX benefits too.)
- **2026-06-11** (Kushagra): Both enabled RSAs in ad group `186398312300` cleared review but came back
  **Average** (not the projected Excellent) — Google docking on keyword coverage, not format. Audited
  ad-group keywords by real impressions (`strength_audit.py`): top missing terms were **traffic ticket
  defence (219 impr, #1 kw)**, **dispute (140)**, **speeding (112)**, **suspended licence (32)**, careless
  (5). Did ~5 in-place headline swaps per ad (out: redundant paralegal/pricing/brand lines) to add those
  keywords while keeping 3 pins + conversion/trust headlines. Court ad `812455198290` + record ad
  `812451424746` both updated in place → re-review (strength reads PENDING until it clears). Kept the 3
  slot-1 pins deliberately (QS > Ad-Strength badge), which may cap just under Excellent — acceptable.
  Note: this ad group mixes 5+ intents (traffic/speeding/careless/suspended/points); the durable fix is the
  SKAG split, deferred to Phase 1 (~July, site live). Script: `rebuild_both_rsas.py`.
- **2026-06-11** (Kushagra): Keyword rebuild did NOT lift strength — both still **Average** after recompute,
  confirming the **3 pins** were the cap (not keyword coverage). Dropped both RSAs from **3 pins → 1 pin**
  (keep "…Traffic Ticket Lawyer" pinned slot 1 for QS; unpin the other two to let Google rotate). This is
  the documented best practice (pin slot 1 only), so it's not a QS sacrifice — expected to lift Average→Good.
  In-place update, re-review pending, strength to recompute. **This is the final ad-copy touch on this
  ad group** — after this, hands off; next priority is conversion tracking. Script: `single_pin.py`.
  **OUTCOME: still AVERAGE after both the keyword rebuild AND single-pin.** Conclusion: with a broad,
  keyword-heavy ad group, keyword coverage and headline diversity pull against each other ("traffic ticket"
  now repeats across ~7/15 headlines), so Average is the equilibrium — Ad Strength won't move without the
  SKAG split. STOP chasing the badge; ads are approved/serving/clean. Real lever = conversion tracking.
- **2026-06-12** (Kushagra): **Audited `Traffic ticket lawyer` (23002273381 — enabled by Akash) vs broad**
  (`ttl_audit.py`, read-only) + applied 2 fixes (`apply_audit_fixes.py`): **(1) TTL CPC ceiling $0→$10**
  (was uncapped on TARGET_SPEND at the new $15/day); **(2) broad Display Network ON→OFF** (search
  campaign was leaking onto display; note: bool-False needs explicit update_mask path). KEY AUDIT FACTS:
  TTL targets **Kingston/Ottawa/Niagara Falls/St. Catharines/Sarnia/Niagara-on-the-Lake (PRESENCE)** —
  NOT GTA! Its cheap leads come from uncontested small-city auctions (CPC $2.49 vs broad $4.31) + old
  ads with history (strength GOOD, both APPROVED). **No DUI keywords live** (old warning stale). 19
  parking keywords enabled but 0 impr (neutralized by shared neg lists) — housekeeping later. Both
  campaigns have both shared neg lists. STRATEGY INSIGHT: small-city Ontario auctions are an
  uncontested market (she serves all Ontario) — consider expanding this play instead of only GTA.
- **2026-06-12** (Kushagra): **Budget swap applied (total unchanged):** `Traffic ticket lawyer broad`
  $30→**$20**/day (worst $/lead, ~$35) and `Traffic ticket lawyer` $5.01→**$15**/day (best $/lead
  ~$3 on Jun 11, was "Limited by budget"; budget res `14912690384`). Kushagra's split, agreed risk:
  the star's $3/lead is a 1-day sample — **watch 3-4 days; if its $/lead blows past ~$15-20, walk
  back to $10.** Live daily budgets now: Max $50 + broad $20 + TTL $15 + #2 $15 + #3 $10 = $110.
  Script: `budget_swap.py`.
- **2026-06-12** (Kushagra): **LEAD FORM LIVE on both Search campaigns** (asset `371903420556`,
  "Fight Your Traffic Ticket / Get your free case review"): HIGH_INTENT quality filter, required
  phone+name+email, "we do not handle parking tickets" in the copy. Custom qualifying question
  rejected by API (vertical restriction) — optionally add a preset one via UI. Kushagra accepted the
  account-wide Lead Form ToS (one-time, was blocking API). **⚠️ NEW DAILY CHORE: download leads at
  Assets → Lead forms (they auto-delete after 30 days, NO auto-email to client)** — forward to
  client same-day; webhook automation = future improvement. Context: **website access is LOST
  (nobody has it)**, so the form-tag install (`form-tracking-setup.md`) is blocked. GA4 property
  **"Blottman Law" id `409838286`** (linked to Ads Oct 6 2023) also inaccessible — Ansh's login has
  no Analytics perms (Ads access ≠ GA4 access). RECOVERY PATHS: client/Akash logins at
  analytics.google.com; the fall-2023 web person adds info@stenth.com as GA4 admin; or Google
  support recovery via domain-registrar proof (ask client where blottman.com is registered). GA4
  matters because its enhanced measurement likely already records form_submit (importable as Ads
  conversion, zero site access). Auto-tagging confirmed ON (gclids flowing — good for future OCI).
  `Traffic ticket lawyer` campaign id = `23002273381`. Scripts: `build_lead_form.py`, `ga4_link.py`.
- **2026-06-12** (Kushagra): **Form-conversion build + canonical leads report.** Discovery: a proper
  **`Submit Lead Form` action (id `7173263227`, WEBPAGE, SUBMIT_LEAD_FORM, primary) already exists
  but fired 0 in 30d — its tag was never installed on blottman.com.** Don't create a duplicate.
  Pulled its gtag snippets (`code/form_tag_snippet.py`) and wrote **`form-tracking-setup.md`** —
  hand to whoever manages the site (Google tag `G-GJSGF3MX1J` is already live sitewide; only the
  event snippet + thank-you page/submit hook is missing; doc includes the gclid hidden-field step
  for future OCI). Also built **`code/leads.py` = THE standard daily report** — always reads
  all_conversions (never the misleading primary-only column), shows today/yesterday by
  campaign×action + 7d by action + 10 recent calls. ⚠️ **stenth default value is now $150, not
  $500** (someone changed it — Akash?) — also "Contact Us" stays SECONDARY deliberately until the
  client confirms she receives the form emails (it's WEBPAGE_CODELESS, 171/30d, may be noise;
  flipping it primary would point bidding at an unverified signal + reset learning). Budgets
  unchanged per Kushagra ("budget is good, don't lift") — the broad$30→25/TTL$5→10 neutral swap is
  proposed but NOT applied. NOTE the $5/day `Traffic ticket lawyer` shows "Limited by budget" in
  UI (Google asking for more room on the cheapest lead source, ~$3/lead Jun 11).
- **2026-06-12** (Kushagra): Added **10 PHRASE negatives to the shared `Master Negatives` list**
  (`12109076551`, now 65 keywords) — attached to ALL 5 live campaigns incl. PMAX: competitors from
  Jun-11 search terms (`kaelah mizzi`, `nextlaw`, `ontario legal ltd`, `ott legal`, `nikbakht law`,
  `brian mcleod`) + DIY/self-serve intent (`early resolution`, `paying`, `pay ticket`,
  `lost my ticket`). Kept "how to fight…" queries (converted 2x Jun 11). **Jun-11 review findings**
  (`yesterday_review.py`): $/lead = PMAX Max ~$9 (7 leads/$66), `Traffic ticket lawyer` ~$3
  (3 leads/$10!), pM #2 $27, broad $35 (worst). **GEO-TRIM PLAN CANCELLED — Vaughan ($13.50→1 conv)
  and Markham ($1.07→2 conv) BOTH converted Jun 11**; Schomberg (near Cookstown) converted too →
  supports adding the local Barrie-area radius. Tablet waste gone (4 impr/$0). Plan for Jun 13
  (post-freeze) rebalance to client's $3K/mo: Max $50→60, TTL $5→10, broad $30→20 (worst $/lead),
  #2 stay $15, #3 stay $10. Scripts: `yesterday_review.py`, `add_shared_negs.py`.
- **2026-06-12** (Kushagra): **STENTH FIRED FOR THE FIRST TIME** 🎉 — Jun 11 (account day) closed at
  977 impr / 33 clicks / $137.25 / **1 primary conv = `Inbound call - Blottman (stenth)`** on
  Blottman New pM #2 (the 102s call, 5:15pm, area 226). Tracker was never broken — it's wired to
  PMAX call assets and PMAX was throttled; recovery → 30s+ call → fired. (Still stamps $500 on any
  30s call — booked-consult refinement stays on roadmap, Akash's lane.) Yesterday's leads: 12 total
  (10 Contact Us forms [6 PMAX Max, **3 from the mystery-enabled `Traffic ticket lawyer`** on $2.75
  spend — earning its keep, leaning keep-enabled, still confirm who enabled it], 1 from broad] +
  1 phone click + the stenth call). `today_leads.py` now takes a period arg (TODAY/YESTERDAY).
- **2026-06-12** (Kushagra): **CLIENT UPDATES:** (1) Client says spend the FULL **$3,000/mo (~$98/day)**
  and demands leads NOW — plan: raise PMAX Max $50→$55-60 after freeze (~Jun 13), keep broad $30,
  taper #3 into Max; (2) **website rebuild CANCELLED** (client unhappy with results) — Phase 1
  re-scoped to existing site (see Strategy section); (3) client claims "no leads" but account counted
  **7 Contact Us forms + 1 phone click TODAY** (6 forms from PMAX Max) — CRITICAL open question:
  does she actually RECEIVE the form submissions? Check her inbox/spam vs form backend. Call_view
  shows real calls during the "dark" days too (102s call Jun 11 5:15pm area 226; 513s call Jun 8 from
  437) — most were <30s so they never counted as conversions. New script: `today_leads.py`
  (today's conv by campaign×action + call_view detail with timestamps/durations).
- **2026-06-12** (Kushagra): **RECOVERY CONFIRMED** — day-after check: impr 837 / clicks 28 / spend $127
  (vs 66 impr Jun 10). PMAX - Blottman Max serving again (521 impr, $63). Campaign/asset-group still
  read LIMITED + policy label = expected residual classification, throttle itself is lifted. 0 primary
  conv yet (calls lag delivery; 7 Contact Us + 1 Phone Click secondary today). Freeze still ON through
  ~Jun 13–14 — no mutations made. ⚠️ FOUND: old **`Traffic ticket lawyer`** campaign (TARGET_SPEND,
  $5.01/day) is **ENABLED** ($2.75 spent today) though our notes say SKAGs are paused — check change
  history for who/when before pausing. Spend pacing ~$110/day in enabled budgets vs $75 target; taper
  broad's $30 after freeze as PMAX stabilizes.
- **2026-06-11** (Kushagra): Diagnosed why the stenth $500 action (`7638369752`) shows 0. It's a plain Google
  **AD_CALL** action (fires on tap-to-call ≥30s, no external upload). Live call-asset wiring: the **Search
  campaign's active asset `82358852814` → "Calls from Smart Campaign Ads"** (that's the 27 conv), while the
  **PMAX winner's asset `370852648512` → stenth** but PMAX was throttled → ~0. So calls land on a different
  action, not stenth. TRAP: stenth is `always_use_default=$500` → would stamp $500 on every 30s call (wrong;
  $500 should = booked consults only). AD_CALL physically can't tell a booked consult from a hang-up. **Do
  NOT force-fire it** — those calls are already counted by "Calls from Smart Campaign Ads"; re-pointing adds
  no info and injects fake $500s. Real fix = **offline conversion import** (gclid capture on new site →
  stenth uploads only booked consults at $500), a Phase-1 (~July) build. This is **Akash's lane** — coordinate
  before changing asset wiring/values. Diagnostic only this session (no mutations).
- **2026-06-14** (Kushagra): **CLIENT COMPLAINT (Les, WhatsApp 3:29am)** — "whatever was done to the
  ads must be retracted… activate old ads as im still getting calls for parking tickets and irrelevant
  questions." Diagnosed source (read-only, LAST_14_DAYS): the parking/junk **calls trace to PMAX, NOT
  the new Search ads.** **PMAX - Blottman Max** insight categories: `parking ticket lawyer toronto`
  (45 impr / **5 clk**), `parking ticket lawyer` (6 impr / 1 clk / **1 conv**), `parking tickets`.
  **Blottman New pM #2** = the "irrelevant" source (`immigration lawyers`, `black legal aid clinic`,
  `24 hour free legal advice`, competitors). The 2 Search campaigns show parking **impr but 0 clicks**
  → clean, do NOT retract them. Did NOT do a blanket retraction (would kill clean traffic + the policy
  fix). FIX APPLIED (API): added `[BRO] parking` (catch-all; only multi-word parking negs existed) +
  `[BRO] immigration` to shared **Master Negatives** (`12109076551`, now 67, attached to all 5 enabled
  campaigns). FIX PENDING (UI-only, can't script): **turn OFF Final URL Expansion on all 3 PMAX**
  campaigns — the real lever for the insight-category leak — step-by-step in `fix-parking-pmax-UI.md`.
  Consider pausing/cutting **pM #2** ($22/day, worst junk). Do NOT re-enable old "98% Win Rate"/DUI ad
  `774748697421`. NOTE: enabled budgets now ~$117/day (pM #2 at $22, not $15 as previously logged).
  Scripts: `add_parking_broad.py`. Effect re-learns over 24–48h.
- **2026-06-14** (Kushagra): **`blottman.com/traffic-tickets` is BROKEN** (client checked it live). Repointed
  ALL live ad click-destinations to the **homepage** `https://blottman.com/`. Changed final_urls on 3 RSAs
  in `Traffic ticket lawyer broad`: `812451424746` (ENABLED), `812455198290` (ENABLED), `812451172230`
  (PAUSED) — were all → /traffic-tickets, now → homepage. Other enabled RSAs (`773055112233`,
  `794266232108`) + all 3 PMAX asset groups were ALREADY on homepage. Only /traffic-tickets sitelink on a
  live campaign (`322570766591` Cell Phone Ticket) is already REMOVED/not serving — no action needed.
  **NOTE:** topical subpage sitelinks (`/careless-driving-ticket/`, `/stunt-driving-ticket/`,
  `/traffic-violations/`, `/criminal-defense/` etc.) were left as-is — client only confirmed /traffic-tickets
  is broken; verify the others before touching. **Also turned OFF Final URL Expansion on PMAX (UI, by
  Akash/Kushagra)** — so PMAX now serves only to the homepage final URL. Script: `repoint_to_home.py`.
- **2026-06-14** (Kushagra): **Fixed BMX geo.** `PMAX - Blottman Max` (`22979153470`) had **NO geo
  targeting** (served anywhere) — a likely source of Les's "irrelevant/out-of-area calls." Set geo =
  **Ontario** (`geoTargetConstants/20121`) + **PRESENCE-only** (`positive_geo_target_type=PRESENCE`),
  since she's an Ontario paralegal serving all ON — keeps GTA + Barrie/Cookstown local + small cities,
  drops only un-serviceable out-of-province traffic. ⚠️ **FOUND: pM #2 & #3 target only Sarnia+Windsor**
  (tiny SW-Ontario, NOT her converting GTA market) — looks misconfigured; decide fix-or-pause (#2 is the
  junk offender anyway). Search campaigns' geo is fine (broad=GTA; TTL=small-city play). Script:
  `fix_pmax_geo.py`. Minor PMAX re-learning expected.
- **2026-06-14** (Kushagra): **PMAX CONSOLIDATION (user-approved).** Paused **pM #2** (`23753177178`)
  + **pM #3** (`23757095274`) — near-duplicates of BMX (same 12 themes, no audience signal, homepage)
  but mis-geo'd to Sarnia+Windsor and generating legal-aid/immigration **junk reach** = a source of Les's
  "irrelevant calls." Diagnosis: PMAX search themes are *hints not limits*; PMAX auto-expands across
  Search/Display/YT/Gmail/Discover to "legal-interested" audiences — can't be fully fenced by negatives,
  so the fix is to NOT run redundant PMAX. Raised **BMX** budget $50→**$60** (+20% safe step; BMX was
  delivery-limited not budget-limited, so it'll scale into the room over days, not instantly). **Enabled
  budgets now: BMX $60 + broad $20 + TTL $15 = $95/day (~$2,888/mo ≈ client's $3K target).** Short-term
  spend may dip until BMX absorbs the volume; Search ($35/day) keeps leads flowing meanwhile. Next: step
  BMX toward $75-80 once it stabilizes (watch CPA). Script: `consolidate_pmax.py`.
- **2026-06-14** (Kushagra): **JUN-13 REVIEW + call-quality check — consolidation CONFIRMED right, HOLD it.**
  Jun 13 closed: **269 impr / 19 clk / $92.30 / 7 leads** (≈ client's $98/day target). stenth fired **3×**
  (2 on pM #2, 1 on pM #3) — firing consistently now. BUT all 7 Jun-13 leads came from **pM #2/#3 + TTL**;
  **BMX produced 0 that day** (still spinning up post-throttle). First read looked like "we cut our best
  campaigns" — it wasn't. Ran `code/call_quality.py` (read-only, call_view can't filter by date → pull-all +
  client-side 7-day filter; area-code GTA set = 416/647/437/905/289/365). Result:
  **BMX = 5 calls, 0 out-of-area, incl. a 513s (8.5-min) GTA consult Jun 8 + 32s GTA** → the clean quality
  source. **pM #2 = 6 calls, 3 out-of-area** (519, 226 SW-Ont, **942 = invalid/spam area code**).
  **pM #3 = 7 calls, 3 out-of-area** (**236 = British Columbia**, 613 Ottawa ×2). So pM's stenth "$500
  conversions" were padding the count with out-of-area/junk calls — exactly Les's complaint. **DECISION:
  keep pM #2/#3 PAUSED, let BMX run at $60 for 3–4 days (it's the clean horse, just needs to absorb budget).
  If volume sags, bump Search (broad/TTL), NOT the PMAX duplicates. Re-check ~Jun 16–17.** Caveat: she serves
  all Ontario, so 519/613 aren't strictly unserviceable — but BMX's all-GTA profile + the 513s consult make
  it the right bet. (Reminder: stenth still stamps its default on any ≥30s call — count ≠ booked consults.)
  Script: `call_quality.py`.
- **2026-06-14** (Akash): **New SKAG campaigns created** in response to client frustration (Leslie
  demanding more volume and old campaigns reinstated). Created: `Higher Value - New` ($5/day),
  `Lower Value - New` ($5/day), `Higher Value - New #3` ($5.01/day), `Traffic Ticket Lawyers Near You`
  ($4.50/day — Smart Campaign). Also re-enabled `Blottman New pM` ($5/day, the old paused PMAX)
  at low budget to satisfy client's "bring back old campaigns" request. NOTE: all original old campaigns
  (Higher Value - clicks, Lower Value - clicks, Calls etc.) are REMOVED — cannot be re-enabled;
  these new campaigns are the rebuilt equivalents.
- **2026-06-14** (Akash + Claude): **Full account review session.** Pulled today's live data
  (653 impr / 19 clk / $31.38 / 1 lead mid-day) + yesterday confirmed 7 leads + stenth 3x.
  Investigated why Leslie was getting out-of-province leads (NY, Massachusetts). Conducted full
  geo audit across all enabled campaigns — all confirmed Ontario-only EXCEPT:
  **(1) pM #2 = PRESENCE_OR_INTEREST → fixed to PRESENCE via API.**
  **(2) Traffic Ticket Lawyers Near You = Smart Campaign with no location criteria → paused**
  (API blocks geo edits on Smart Campaigns). Added legal aid negatives to Master Negatives:
  `[PHR] legal aids` + `[PHR] free lawyer` (legal aid/free legal/pro bono were already present; now 69 total).
  FUE toggle investigated — could not locate in UI during this session (note: Kushagra's earlier
  session confirmed it was turned OFF — see Jun-14 Kushagra entry on blottman.com/traffic-tickets).
  Budget adjustments applied: PMAX Max $60→$50, pM #2 $22→$15, TTL broad $20→$10. ⚠️ NOTE:
  these changes were applied before reading Kushagra's Jun-14 consolidation notes — Kushagra had
  already set BMX to $60 and budgets to $95/day. Recommend verifying live budget state and
  restoring BMX to $60 / TTL broad to $20 if needed to match Kushagra's consolidation plan
  (BMX $60 + broad $20 + TTL $15 = $95/day).
- **2026-06-14** (Akash + Claude): **Contact Us form audit.** Pulled last 7 days (Jun 7–13):
  **35 Contact Us submissions** across all campaigns. Breakdown: Jun 8 = 9 (best day), Jun 11 = 10,
  Jun 13 = 4. Leslie to be asked whether she received these — if no/unknown, form emails are broken
  or going to spam. NOTE: Contact Us is WEBPAGE_CODELESS (no tag installed) — count may include
  bots/partial fills; true quality only confirmed by Leslie's inbox count.
- **2026-06-14** (Akash + Claude): **Call volume analysis.** call_view (all-time): 1,116 total calls,
  604 qualifying (≥30s), 512 short/missed. All qualifying calls from PMAX campaigns only — zero
  calls from Search (TTL, TTL broad) despite call assets being attached. Search campaigns converting
  via Contact Us form, not phone. Speed-to-answer flagged as a key issue for Leslie — many short
  calls are likely missed/voicemail hang-ups. Call asset audit: pM #2 and #3 had one REMOVED +
  one ENABLED entry each (ENABLED is the active one, REMOVED = old deleted version — no action needed).
- **2026-06-14** (Akash + Claude): **Professional work summary PDF generated** —
  `Blottman-Law-Google-Ads-Report.pdf` (12 sections, covers all work Jun 2026). Includes:
  exec summary, account ownership transfer (Joshua → Leslie Rivas), initial audit findings,
  campaign consolidation, delivery incident, search campaigns + RSAs, negative keywords,
  geo fixes, lead form + conversion tracking, scripts built, performance table, open items.
  Script: `generate_report.py`. Logos: `STENTH LOGO.png` + `BLOTTMAN LOGO.png`.
- **2026-06-14** (Akash): **GitHub repo created and all files pushed** to
  `https://github.com/Stenth-Industries/Blottman-.git` (main branch). Secrets (.env,
  credentials.json) excluded via .gitignore. All scripts, CLAUDE.md, report, and logos committed.
- **2026-06-15** (Akash + Claude): **6-campaign budget split applied** — exact $100/day:
  BMX $45 + TTL $20 + Lower Value-New $15 + TTL broad $10 + Higher Value-New $5 + Blottman New pM $5.
  pM #2, pM #3, Higher Value-New #3 remain PAUSED. Goal = 2-3 qualifying calls/day.
- **2026-06-15** (Akash + Claude): **Call quality — today's only call was lawsuit inquiry.**
  One 647 call (43s, qualifying) was someone asking about filing a lawsuit — completely off-target
  for a traffic ticket paralegal. Immediate action: added 16 PHRASE negatives to Master Negatives
  covering lawsuits, civil litigation, personal injury, criminal law, divorce, family law, immigration
  lawyer, notary. These block both the lawsuit-seeker intent AND other practice areas that have
  historically triggered misdials. Total negatives in Master Negatives now ~85+.
- **2026-06-15** (Akash + Claude): **Contact Us tracking gap CONFIRMED + full conversion audit.**
  Leslie confirmed she received only 5-10 Contact Us submissions last week (not the 35 our data showed).
  Ran full conversion action audit. KEY FINDINGS:
  **(1) Contact Us (WEBPAGE_CODELESS) is ALREADY demoted** — include_in_conversions_metric=False,
  primary=False. It shows 0 bid-conversions. The campaigns are NOT optimizing for it. The 35 number
  was just what we reported to Leslie — we should stop quoting it as a "lead" metric entirely.
  **(2) 30-day conversion breakdown (May 15–Jun 14):**
    - Contact Us: 169 all-conv, 0 bid-conv (correctly demoted)
    - Calls from Smart Campaign Ads: 25 all-conv, 25 bid-conv (Smart Campaign internal)
    - Phone Click: 12 all-conv, 0 bid-conv (correctly demoted)
    - Inbound call - Blottman (stenth): 5 all-conv, 5 bid-conv ← our only real quality signal
    - Lead form - Submit: 0 conversions (no lead form submissions in 30 days)
  **(3) CRITICAL INSIGHT:** PMAX and Search campaigns have only 5 stenth quality conversions in 30
  days to learn from. This is far too thin for Max Conversions bidding. The algorithm is essentially
  learning blind. This is the root cause of inconsistent results. Fix = install real form tag +
  increase volume of real conversions so algorithm can optimize properly.
  **(4) Lead Form = 0 submissions in 30 days.** Either the lead form ad extension isn't getting
  impressions or users aren't filling it out. Needs investigation.
- **2026-06-17** (Kushagra): **CLICKBAIT policy violation fixed on PMAX - Blottman Max / Asset Group 1**
  (`6607110351`). UI showed 2 violations on the asset group: (1) **Clickbait** (red — Google
  Investigation / automated check; does NOT name the asset) and (2) Commission-of-a-crime (the known
  harmless residual). Root cause of clickbait = **unsubstantiated "98% Win Rate" stat (×6 assets) + a
  "#1 Lawyer" superlative** — double-violation in a legal vertical (clickbait + outcome guarantee).
  Note: the API never surfaced clickbait as a `policy_topic_entry` (it's a pending editorial check),
  only the crime topic showed — so this was diagnosed from the UI screenshot + asset text scan.
  **FIX (API, published):** replaced all 7 flagged assets via `/generate-ads` (validated to char
  limits + editorial rules) with policy-safe copy that fills pattern gaps: HEADLINES → `Skilled Ticket
  Defence Team`, `Fight Auto Fines & Keep Points`, `Avoid Costly Demerit Points`, `Experienced Ticket
  Paralegal`; LONG_HEADLINE → `Fight Your Car Ticket & Keep Your Licence · Free Case Review With
  Blottman`; DESCRIPTIONS → `Fight your car ticket with 24/7 legal help. 500+ cases handled. Free case
  review.` + `Ontario traffic ticket specialists. Fight your ticket with a free case review today.`
  Kept the verified "500+ cases handled" signal; dropped every win-rate stat. Verified: **0 clickbait
  assets enabled** post-change. Old assets unlinked (not deleted); 1 of the 7 old links was already
  REMOVED (someone removed "98% Win Rate, Fight Tickets" earlier). New assets in editorial review —
  recheck the asset-group "Clickbait" flag clears in a few hrs/24h. Script: `fix_clickbait_assets.py`.
  ⚠️ NOTE (creative = Akash's lane). OPEN follow-ups spotted, NOT changed: (a) other BMX headlines
  still say "Lawyer" though Leslie is a **paralegal** = misrepresentation risk; (b) typo headline
  "500+ Cases Car Cases Handled" (`283882668010`). Also re-confirmed the `COMMISSION_OF_A_CRIME_IN_
  PERSONALIZED_ADS` flag is harmless residual (assets APPROVED_LIMITED, still serving, NO audience
  signal attached — the real throttle trigger from Jun-11 stays removed). Scripts: `asset_policy.py`,
  `campaign_status.py`.
- **2026-06-17** (Kushagra): **Lead form now APPROVED + expanded to all 4 Search campaigns.** The
  lead form asset `371903420556` ("Lead Form - Free Case Review (Stenth)", CTA GET_QUOTE) finally
  cleared review → **APPROVED / REVIEWED** (was stuck behind the account-wide Lead Form ToS/review).
  It started serving for the first time: **11 impressions Jun 16** on `Traffic ticket lawyer` (0 clk
  yet — day one). Resolves the eligibility half of the Jun-15 "Lead Form = 0 submissions" open item.
  **Attached the same asset to the 2 Search SKAGs that lacked it** — `Lower Value - New`
  (`22780000236`) + `Higher Value - New` (`22780001277`) — so all 4 ENABLED Search campaigns now
  carry it (the other 2 already had it). **Skipped both PMAX** (Blottman Max, Blottman New pM): PMAX
  doesn't take campaign-level lead-form extensions and they're policy-touchy — left to calls.
  Note: broad shows 0 form impr in 14d (loses ~83% IS to rank → no room to attach the extension);
  volume will come mainly from the small-city `Traffic ticket lawyer`. Script: `attach_lead_form.py`.
  ⚠️ Reinforces the **daily lead-form download chore** (submissions don't email Leslie + auto-delete
  after 30d) — more campaigns now = more submissions to catch same-day. Consider the `leads.py`
  lead-form-submission add-on / webhook.
- **2026-06-18** (Akash + Claude): **JUN-17 REVIEW — best day in weeks, consolidation validated.**
  Jun 17 closed: **~800 impr / 40 clk / ~$143 / 11 all-conv.** **stenth $500 fired 4× — ALL on
  PMAX - Blottman Max, ALL GTA:** 647 (33s), 416 (92s), 416 (63s), 416 (43s). Zero out-of-area, zero
  junk → exactly the clean-horse outcome the Jun-14 PMAX consolidation bet on. Contact Us = 7 (4 PMAX
  Max, 2 `Traffic ticket lawyer`, 1 Higher Value-New). One 2s misdial didn't qualify. **Geo clean:**
  Toronto $77/3conv, Brampton $13/2, Mississauga, Richmond Hill, Oshawa — GTA-dominant, small cheap
  Ottawa tail, **no out-of-province leak** (geo fixes holding). **Search terms clean** — all
  traffic/speeding/careless/cell-phone/stop-sign/suspended intent, no parking/competitor/lawsuit/
  immigration leakage (negative-list buildup working). Search SKAGs (Lower/Higher Value-New, TTL
  broad) click but produce 0 stenth calls — they convert via form only, consistent with prior pattern.
  ⚠️ **SPEND PACING HOT: $143 vs $100/day target (+43%)**, driven by **BMX spending $70 on its $45
  budget** (PMAX can run up to ~2× on a day; watch the monthly average). Recommendation: lean into BMX
  since it's the verified quality source — either formally raise its budget or rein the day in. Per-day
  campaign table: BMX $70/8conv, TTL $28.84/2conv, Lower Value-New $16.78/0, TTL broad $12.29/0,
  Blottman New pM $9.93/0, Higher Value-New $5.12/1conv. Read-only review; no mutations. Scripts:
  `yesterday_review.py`, `today_leads.py YESTERDAY`.
- **2026-06-15** OPEN ITEMS (carried forward):
  - [ ] Get site access from Leslie → install proper form conversion tag (form-tracking-setup.md ready)
  - [ ] Investigate Lead Form submissions = 0: check if lead form is attached + getting impressions
  - [ ] Re-check account Jun 18-19 to see if 2-3 calls/day target is being hit post-budget-split
  - [ ] Get GA4 access (property id 409838286)
  - [ ] Phase 2: Offline Conversion Import for booked consults at $500
  - [ ] Get brand creative from Leslie: 4+ landscape, 4+ square, 2+ portrait + 1 video for PMAX
- **2026-06-16** (Akash + Claude): **COMPROMISED-SITE cleanup (done) + CLICKBAIT policy diagnosis
  (ON HOLD pending Kushagra coord).**
  **(A) DONE — detached all compromised `blottmanlaw.com` assets.** Found the OLD domain
  `blottmanlaw.com` (NOT the live `blottman.com`) flagged `COMPROMISED_SITE`+`ONLINE_GAMBLING` —
  hacked/repurposed. 24 disapproved sitelinks + 1 disapproved PROMOTION asset were still in the
  account. Source campaigns ("IGNORE"/"IGNOREE") are REMOVED, BUT the PROMOTION asset (`108881683961`)
  was still ENABLED-linked to **2 LIVE campaigns** (`Lower Value - New` 22780000236, `Higher Value -
  New` 22780001277) + paused `Higher Value - New #3` (23692507381) — all 3 links REMOVED via API.
  All 24 compromised sitelinks now only link to REMOVED campaigns → fully orphaned, cannot serve.
  ⚠️ Orphaned assets DON'T show in Assets→Sitelinks UI (that view only lists attached assets), so
  they can't be hand-deleted; they're harmless and Google auto-GCs them. No script saved (ad-hoc
  inline API). Verified 0 compromised assets on any ENABLED/PAUSED campaign.
  **(B) ON HOLD — Clickbait violation on PMAX - Blottman Max (+ shared assets).** The asset group's
  2nd policy violation (UI "Clickbait"; the API does NOT expose a CLICKBAIT topic, only the separate
  `COMMISSION_OF_A_CRIME_IN_PERSONALIZED_ADS` label which is benign/unfixable = the legal content).
  Clickbait trigger = **unverifiable claims "98% Win Rate" / "#1" / "100%"**. ⚠️ "98% Win Rate" is
  ACCOUNT-WIDE (~30 RSAs across Higher Value-New, Lower Value-New, Traffic ticket lawyer, Higher
  Value-New #3, Blottman New pM + PMAX). 10 claim-bearing assets feed live PMAX:
  asset-group HEADLINES `283878683260` ("Fight Auto Fines, 98% Win Rate"), `283878683272` ("98% Win
  Rate, Fight Auto Fines"), `283882668013` ("#1 Lawyer For Car Tickets"); LONG_HEADLINE `283878683284`;
  DESCRIPTIONS `283811294381` + `373198526544`; plus SHARED campaign-level callouts "98% Win Rate" &
  "100% Representation", a campaign sitelink ("Contact Us" w/ 98% desc) + an account sitelink ("Fight
  Your Car Tickets" w/ 98% desc). NOTE `500+ Cases`, `4.8 Star/300+ Reviews`, `500+ Car Ticket Cases
  Handled` are TRUE/verified → KEEP. Proposed compliant replacements drafted (see chat). **NOT
  APPLIED** — Akash to coordinate with Kushagra first because #7-10 are shared assets that also touch
  the Search campaigns (Kushagra's lane). Mechanism note: GAds text assets are IMMUTABLE → fix =
  create new asset + relink + remove old (not in-place edit). Timing guidance: do the copy swap on a
  day with NO budget/bid changes (asset re-review ≈1-2 days, does NOT reset bid-strategy learning;
  the campaign keeps serving on its other ~20 approved assets). The clickbait claims are ALREADY a
  drag (asset group reads LIMITED-by-policy) so removing them likely HELPS delivery + avoids a harder
  disapproval/account strike. Don't bundle with a budget reshuffle.
- **2026-06-21** (Akash + Claude): **Pulse check + impression-spike diagnosis (read-only, NO mutations).**
  Live pull (`leads.py`, `campaign_status.py`, `yesterday_review.py`). Account healthy & delivering;
  6 campaigns enabled at **$100/day** total (BMX $45, TTL $20, Lower Value-New $15, TTL broad $10,
  Higher Value-New $5, Blottman New pM $5). **stenth $500 firing consistently — 7× in last 7d.**
  **Jun-20 = 16 leads** on 18,494 impr / 198 clk / $117.91 (spend ran hot vs $100 target; PMAX can do ~2×/day).
  **IMPRESSION SPIKE EXPLAINED:** the 18.5k (vs ~800 on Jun 17) is **98% PMAX** — BMX 12,663 impr ($0.56 CPC)
  + Blottman New pM 5,507 impr (**$0.16 CPC**); Search campaigns tiny/clean. Those CPCs = cheap
  Display/Discover/YT inventory, NOT search demand (PMAX has no network controls; FUE already OFF).
  **Device split is the smoking gun:** Mobile 13,553 impr / 13 conv (the real engine, healthy);
  **Desktop 1,041 impr / 1 clk / 0 conv** (pure junk Display reach); **Tablet 3,895 impr / $15 / 2 conv**
  (the old tablet waste creeping back); CTV 5 impr (PMAX starting to push video). Mobile carries all the
  real conversions, so the headline number is mostly harmless cheap reach — BUT the underlying risk is
  PMAX optimizing toward **Contact Us form-fills** (untrusted WEBPAGE_CODELESS signal) → cheap Display
  placements breed low-quality/bot form-fills, matching Leslie's "I only get 5–10/week" complaint.
  Recommended cleanest cut = pause **Blottman New pM** (worst junk-reach/$: 5.5k cheap impr, 1 conv,
  near-dup of BMX; siblings #2/#3 already paused Jun-14 for the same reason). **DECISION: user said KEEP
  Blottman New pM enabled — no change made.** Real long-term lever stays the same: point PMAX at the
  verified call signal (stenth) instead of Contact Us = needs the form tag / site access (still blocked).
  Watch item: lead *quality* of PMAX Contact Us form-fills.
