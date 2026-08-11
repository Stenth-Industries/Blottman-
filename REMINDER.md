# ⏰ Reminders — Blottman Law Ads

## 🔴 ~Aug 14-15, 2026 — Repoint PMAX (BMX) final URL blottman.com → blottman.ca (FOR AKASH + KUSHAGRA)
**Same decision gate as the Jul 5 entry below — still not done as of Aug 11.** BMX's asset group final
URL is still `https://blottman.com/`. On Aug 11 we made two changes to BMX already (budget $65→$50/day,
removed the PMAX call-asset to push impulse-call traffic toward a form instead) and deliberately did NOT
stack a third significant change (this URL migration) on the same campaign within the same 72h window —
this account has a documented history (the June delivery-collapse incident) of stacked changes causing
real damage. **Wait ~3-4 days from Aug 11, let the budget cut + call-asset removal show clean data, then
do the migration as its own isolated step:**
1. Repoint BMX asset group final URL `blottman.com/` → `blottman.ca/`
2. Repoint or drop the 2 campaign-level sitelinks on BMX (one points to `/contact-us/`, which doesn't
   exist on blottman.ca — needs to go to the homepage instead, where the QuickForm lives)
3. Check the 8 account-level sitelinks that also touch blottman.com and could still serve on BMX
FUE is already off on BMX, so no risk of Google auto-expanding into other blottman.com pages mid-move.

**Also open from Aug 11, not yet investigated:** blottman.com does have a lead form after all — it's a
**LeadConnector/GoHighLevel iframe embed** (`api.leadconnectorhq.com/widget/form/...`, form named
"Blottman"), invisible to a plain HTML/curl check since it's a client-side iframe (a first pass missed
it). It's a separate system from blottman.ca's QuoteForm/QuickForm and is NOT wired to the
`Submit Lead Form` Ads conversion action, so submissions through it are probably going untracked.
There's also a **CallRail** dynamic-number-insertion script on the page (swaps the displayed phone
number per traffic source) — not previously documented anywhere in this account's notes. Both need a
real look: who owns/monitors the LeadConnector form, does Leslie see those submissions, and does
CallRail's number swap explain anything about the call-quality pattern.

To act: open Claude Code in this folder and say *"check on the BMX final URL migration + the
LeadConnector/CallRail stuff we found Aug 11."*

---

## 🔴 ~July 5, 2026 — Check .ca form signal → then repoint PMAX to blottman.ca
**Decision gate for repointing PMAX (BMX + Blottman New pM) from blottman.com → blottman.ca.**
Today (Jun 28) PMAX asset groups all land on **`https://blottman.com/`** (old site, FUE OFF), so PMAX
only feeds the untrusted "Contact Us" codeless signal — its sole trusted signal is calls (stenth). The
new **Search – Ontario Traffic Tickets (Consolidated)** (`23971101309`, live Jun 27) lands on
**blottman.ca**, where the form fires a real Google Ads conversion.

**VERIFIED Jun 28 (Anshul):** the .ca form→conversion path is fully wired in production —
blottman.ca returns 200, loads gtag `AW-11165656868`, and the form-conversion send_to
`AW-11165656868/RcgyCPuevdwaEKTOmcwp` is baked into the live JS bundle. `QuoteForm.tsx` fires
`gtag('event','conversion', {send_to})` on successful submit. Env vars confirmed set in Vercel prod
(gtag loading live = `NEXT_PUBLIC_GADS_ID` + `NEXT_PUBLIC_GADS_CONVERSION` present). Code is good —
the only open question is whether real submissions register as the **`Submit Lead Form`** action
(`7173263227`) in Google Ads.

**On ~Jul 5, run:** `python code/leads.py` and `python code/yesterday_review.py` — look for
**`Submit Lead Form` conversions** appearing from the consolidated Search campaign (Search should have
exited LEARNING by ~Jul 4–5).
- **If ≥ ~5 Submit Lead Form conversions have logged** (proves .ca tracking works end-to-end) AND BMX
  is stable → **repoint PMAX asset groups to `https://blottman.ca/`** (one move, on a quiet day, NO
  budget/bid changes — it resets PMAX learning). This lets PMAX optimize toward real form leads, not
  just the codeless Contact Us.
- **If 0 form conversions** → do NOT repoint PMAX; debug why the .ca form action isn't registering
  (submit a live test lead on blottman.ca, watch the action in Google Ads) before moving PMAX.

To act: open Claude Code in `E:\Blottman-law` and say *"check the .ca form signal."*

---

## 🔴 June 24, 2026 — Check blottman.ca migration test (broad campaign)
On Jun 23 the 2 enabled RSAs in **Traffic ticket lawyer broad** (`23039650759`) were
repointed from blottman.com → **blottman.ca** (staged test before migrating all campaigns).
**Run:** `python code/check_broad_tomorrow.py` — confirm both ads are **APPROVED**, serving,
clicks land on blottman.ca, and a conversion shows. Sitelinks left on blottman.com (mismatch
accepted for the test). **If approved + clean → migrate the rest** (other Search campaigns + PMAX).
**If disapproved → read the policy reason** before rolling out further.

> **Jun 23 update (Anshul):** hit a *"One website per ad group / This ad can't run"* disapproval —
> the 2 PAUSED ads in the ad group were still on blottman.com, and Google's "one website per ad group"
> rule counts paused ads too, so the .ca/.com mix flagged the whole group. **Fixed** by repointing the
> 2 paused ads to blottman.ca (`code/fix_paused_ad_domains.py`). ⚠️ **When migrating the rest, sweep
> PAUSED ads too** in every campaign or you'll re-trigger this. Sitelinks still on .com — migrate those too.

To act: open Claude Code in `E:\Blottman-law` and say *"check the blottman.ca migration."*

---

## 🔵 ~June 15, 2026 — Reassess PMAX taper (Step 3)
After raising **PMAX - Blottman Max** to $50/day on Jun 10, check whether it held ~$50 CPA at the new budget.

**If CPA held ($50–60) and it's spending the budget:**
- Begin **Step 3 taper**: gradually shift `Blottman New pM #2` ($35.61/day) and `#3` ($35.61/day) budgets into Max, then pause #2/#3 once Max absorbs the volume.
- Run **Step 4 geo trim**: drop Vaughan, Markham, London, Cambridge, Orillia (0 conversions).

**Also check:** did the STENTH $500 call conversion start firing? → run `python stenth_watch.py`

To act: open Claude Code in `E:\Blottman-law` and say *"reassess the PMAX taper."*

---

## 🟢 Ongoing — daily
- `python stenth_watch.py` each morning — confirm the $500 stenth call signal starts flowing (was switched Jun 9, expected to lag a few days).

## 🟡 When ready
- Flip **Final URL Expansion OFF** on PMAX - Blottman Max (UI: Campaign settings → Final URL expansion).
- Provide brand creative for PMAX: 4+ landscape + 4+ square + 2 portrait images, 1 short video.
- Decide audience signal source (remarketing list vs custom segment).
