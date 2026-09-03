# Reminders — Blottman Law

> Follow-ups that need a human to act or a date to arrive.
> Deep context lives in `CLAUDE.md`; this file is only "what to do next, and when".
> **Rewritten 2026-09-03** — every prior item was from June and long since done or
> superseded (blottman.ca migration check, PMAX taper, FUE flip, daily `stenth_watch`).
> Git history has the old version if anyone needs it.

---

## 🔴 Friday 2026-09-04 — BMX Target CPA verdict

On **Sep 2** the $95 Target CPA was removed from **PMAX - Blottman Max** (`22979153470`),
leaving plain Maximize Conversions. Day one looked strong, but one day proves nothing in
this account.

**Run:** `python code/leads.py` and `python code/campaign_status.py`

**The question:** has BMX held its volume, or was Sep 2 an outlier?

| Read | Verdict |
|---|---|
| BMX holding **~15-20 clicks/day** and converting most days | Working. Leave it alone. |
| BMX back to **~5 clicks/day and zeros** | Sep 2 was noise. Next lever is the **conversion-goal mix**, not bidding. |

**Baselines to compare against:**
- BMX Aug 18-31: **$705.21 / 4 conv = $176.30 CPA**, including 6 consecutive zero days.
- BMX Sep 2: **276 impr / 20 clicks / $47.47 / 3 conv = $15.82 CPA**.
- Account Sep 2: 828 impr / 53 clicks / $108.46 / **4 conv @ $27.12** — best day in 30
  days on both count and cost, and phantom-free (`all_conversions == conversions`).

⚠️ **Friday is only 2 days post-change.** It can catch a collapse but cannot confirm a fix.
**The real checkpoint is Sun 2026-09-06 / Mon 2026-09-07**: if BMX has logged **5+ conversions
since the change at a CPA under ~$100**, call it fixed. Precedent for caution: Aug 10 also did
3 conversions and was followed by zeros on Aug 11, 13, 15 and 16.

To act: open Claude Code in `E:\Blottman-law` and say *"check BMX."*

---

## 🟡 Needs Leslie — not blocked on us

- **Brand creative for PMAX.** Still the biggest unfilled gap vs competitors: 4+ landscape,
  4+ square, 2+ portrait images, 1 short video. Open since June.
- **The old 647 number is still published** on **Google Business Profile** and **blottman.com**.
  Ad calls and blottman.ca taps now route through the Twilio press-1 screening
  (+1 289 401 5322), but anyone who finds her via GBP or the old site still reaches her cell
  unscreened. This is the remaining hole in call screening.
- **Retention capture (`Retained?` column).** Parked since Jul 17 by decision, not by a
  blocker. Still the prerequisite for Offline Conversion Import, and still the number that
  decides whether ~$128/lead is good or ruinous.

---

## 🟢 Watch — no action yet

- **Keypress data from Twilio screening.** Press-1 vs press-2 counts in the
  `/api/voice/complete` logs are the first direct measurement of the junk-call rate this
  account has ever had. Pending real call volume.
- **Call-duration thresholds.** Google times calls from when *Twilio* answers, so the
  greeting plus ringing inflates every counted duration. `stenth` (45s) and
  `Calls From Website` (60s) should both be re-cut from a week of real `DialCallDuration`
  data — not by arithmetic.

---

## ⛔ Do not do these

- **Do not re-add an audience signal to asset group `6607110351`.** That is what triggered
  the `COMMISSION_OF_A_CRIME_IN_PERSONALIZED_ADS` throttle and the June delivery collapse.
- **Do not cut Search Consolidated to $30.** That Aug 29 recommendation is stale — Search is
  currently the cheaper lead source (~$100/lead vs BMX's $176 over the same 14 days).
- **Do not chase BMX's `HAS_ASSET_GROUPS_LIMITED_BY_POLICY` flag.** Verified Sep 2: every
  enabled asset is APPROVED with zero policy topic entries. It is a harmless residual.
- **Do not publish the paused PMAX draft** (Maximize Conversion Value, tROAS 2.27, created
  Aug 11). There is no revenue data in the account to support value bidding.
