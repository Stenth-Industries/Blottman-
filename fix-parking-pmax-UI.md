# Stop parking + irrelevant calls — PMAX "Final URL Expansion" OFF (UI only)

> Created 2026-06-14 in response to Les's Jun-14 message ("still getting calls for parking
> tickets and irrelevant questions"). The parking/junk calls trace to the **Performance Max**
> campaigns, not the new Search ads. The durable fix is a setting the API can't change
> (`url_expansion_opt_out` was removed from the Campaign resource in google-ads v31 / API v24),
> so it **must** be flipped by hand in the Google Ads UI. Anyone with Standard/Admin can do it.

## Why this is the fix (the data)

Last-14-day check of where parking/irrelevant traffic actually came from:

- **PMAX - Blottman Max** served on insight categories `parking ticket lawyer toronto`
  (45 impr, **5 clicks**), `parking ticket lawyer` (6 impr, 1 click, **1 conversion**),
  `parking tickets` (3 impr). Those clicks → the parking **calls** Les is getting.
- **Blottman New pM #2** served on `immigration lawyers`, `black legal aid clinic`,
  `24 hour free legal advice`, competitor names → the "irrelevant questions."
- The two Search campaigns showed parking **impressions but 0 clicks** → NOT the call source.
  (So do **not** retract the Search ads — they're the clean traffic.)

Keyword negatives can't block PMAX's semantic insight categories / Final-URL-Expansion traffic.
Turning **Final URL Expansion OFF** restricts PMAX to the asset group's own search themes +
the final URLs you specify, which stops the wandering into parking/immigration/legal-aid queries.

(Belt-and-suspenders already done via API on 2026-06-14: added `[BRO] parking` + `[BRO] immigration`
to the shared **Master Negatives** list — helps Search and PMAX search themes, but does NOT touch
the insight-category leak. This UI toggle is the part that does.)

## Steps — do this for ALL 3 PMAX campaigns

Repeat for each: **PMAX - Blottman Max**, **Blottman New pM #2**, **Blottman New pM #3**.

1. Sign in to Google Ads → account **Blottman Law** (customer ID `8586214705`).
2. Left menu → **Campaigns**. Click into the PMAX campaign.
3. Left menu → **Settings** (campaign-level settings).
4. Find **Automatically created assets / Final URL expansion** section
   (sometimes labelled **"Final URL expansion"** or under **"More settings"**).
5. **Uncheck / turn OFF** "Send traffic to the best-performing URLs on your site."
   - Keep the **Final URLs** pointed at the real traffic-ticket pages
     (`blottman.com/traffic-tickets`), NOT the homepage.
6. **Save.**
7. Repeat for the other two PMAX campaigns.

### Optional, same visit (recommended)
- In **PMAX - Blottman Max** → asset group → **Search themes**: confirm there are NO parking
  themes and that the themes are tight (traffic / speeding / careless / stunt / suspended / cell phone).
- **Blottman New pM #2** is the worst junk offender (immigration / legal-aid / competitor reach).
  Consider **pausing #2** or cutting its budget ($22/day) until it's cleaned up — coordinate first.

## After

- Effect isn't instant — PMAX re-learns over **24–48h**. Expect parking/irrelevant calls to taper, not vanish at once.
- **Do not** also re-enable the old "98% Win Rate" / DUI Search ad (ad `774748697421`) — it's a
  policy liability; that's the only "old ad" we deliberately keep paused.
- Re-check after a couple days with the PMAX insight query (per-campaign) — parking categories should drop toward 0 clicks.
- **Log it in CLAUDE.md** (who flipped it + date) so Akash/Kushagra stay in sync — last-save-wins.
