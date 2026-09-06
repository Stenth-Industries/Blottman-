# Reminders — Blottman Law

> Follow-ups that need a human to act or a date to arrive.
> Deep context lives in `CLAUDE.md`; this file is only "what to do next, and when".
> **Rewritten 2026-09-03** — every prior item was from June and long since done or
> superseded (blottman.ca migration check, PMAX taper, FUE flip, daily `stenth_watch`).
> Git history has the old version if anyone needs it.

---

## ✅ CLOSED 2026-09-06 — BMX Target CPA verdict: WORKING

Removing the $95 Target CPA from **PMAX - Blottman Max** (`22979153470`) on Sep 2 cleared the
bar this file set: **5 conversions, $218.57, $43.71 CPA (Sep 2-6)**, against **2 conversions,
$414.87, $207 CPA** over the nine days before. Clicks went 7.7/day to 14.8/day.

Leave it alone. Stop checking daily. Full numbers and caveats in `CLAUDE.md`.

**The one thing that would reopen this:** BMX running **4+ consecutive zero-conversion days**.
Sep 5 was already a zero, and n is only 5 days. If it happens, the next lever is the
**conversion-goal mix, NOT a new Target CPA** — the signal $95 was calibrated against
(stenth calls) is no longer where BMX converts.

---

## 🔴 Someone has to read this value — `TWILIO_RECORD`

A `TWILIO_RECORD` variable now exists in **Vercel Production** on landing-v2, created ~Sep 4.
**Its value cannot be read from Claude Code** (`vercel env pull` returns `[SENSITIVE]`).

Recording is off unless the value is exactly `1`. If it *is* `1`, these three gates from the
Sep-5 build were supposed to come first, and none of them are technical:

1. **Leslie's agreement in writing.** These are prospective-client calls to a licensed
   paralegal. The confidentiality duty is hers; the audio sits in Stenth's Twilio account.
2. **HTTP basic auth on Twilio media URLs**, set *before* the first recorded call. Twilio
   recording URLs are unauthenticated by default — anyone with the link can play the audio.
3. **A retention decision.** Nothing in this repo deletes recordings.

**To check:** open the value in the Vercel dashboard, or look for recordings in the Twilio
console. If it is on and the gates were not cleared, set it to `0` and redeploy.

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
- **Do not move budget between BMX and Search on a weekly CPA read.** Which one looks cheaper
  has now flipped twice in eight days (Aug 29: BMX $176 vs Search $100; Sep 6: BMX $44 vs
  Search $103). At 7-8 conversions per campaign that ranking is noise. Both stay at $50/day.
- **Do not chase BMX's `HAS_ASSET_GROUPS_LIMITED_BY_POLICY` flag.** Verified Sep 2: every
  enabled asset is APPROVED with zero policy topic entries. It is a harmless residual.
- **Do not publish the paused PMAX draft** (Maximize Conversion Value, tROAS 2.27, created
  Aug 11). There is no revenue data in the account to support value bidding.
