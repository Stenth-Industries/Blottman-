# ⏰ Reminders — Blottman Law Ads

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
