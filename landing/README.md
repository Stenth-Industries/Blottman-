# Blottman Law — Landing Page

A self-hosted, single-page landing page for the Google Ads traffic-ticket campaigns. Built because
**we have no access to blottman.com** — this page is a destination *we* fully control, so we can
finally (a) track form conversions, (b) capture the `gclid` for the future $500 offline-conversion
import, and (c) email leads straight to the client.

## Files
- `index.html` — the landing page (hero + free-case-review form + practice areas + call CTAs).
- `thank-you.html` — shown after a successful submit; **fires the Google Ads conversion**.

## What's already wired in
| Thing | Value | Where |
|---|---|---|
| GA4 / Google tag | `G-GJSGF3MX1J` | `<head>` of both pages |
| Google Ads conversion (`Submit Lead Form`, id `7173263227`) | `send_to: AW-11165656868/RcgyCPuevdwaEKTOmcwp` | `thank-you.html` |
| Call number | (647) 794-7750 → `tel:+16477947750` | both pages |
| gclid capture | hidden form field + `localStorage` | `index.html` |
| Lead delivery + storage | Netlify Forms (`name="case-review"`) | the `<form>` |

## Deploy (Netlify — free, ~10 min)
1. Create a free account at [netlify.com].
2. **Add new site → Deploy manually** and drag this `landing/` folder in (or connect this Git repo
   and set the publish directory to `landing`).
3. Netlify auto-detects the form (the `data-netlify="true"` attribute). Go to
   **Site → Forms → Form notifications → Add notification → Email** and enter the **client's email**
   so every lead is forwarded the moment it's submitted. (Submissions are also stored in the Netlify
   dashboard as a backup — this is the answer to "does she actually receive the leads?")
4. **Custom domain:** since we chose a fresh standalone domain, register one (e.g. a `.ca`), then in
   **Netlify → Domain settings** add it and follow the DNS steps. Netlify issues HTTPS automatically.

## Point the ads at it
Once the domain is live, set it as the **Final URL** on the live campaigns (currently all → homepage):
- `Traffic ticket lawyer broad` RSAs `812451424746`, `812455198290`
- The 3 PMAX asset groups (UI)
Use a clean URL like `https://YOURDOMAIN.ca/?utm_source=google&utm_medium=cpc`. Auto-tagging appends
`gclid`, which the page captures.

## Test before spending on it
1. Open `https://YOURDOMAIN.ca/?gclid=test123`.
2. Submit the form with **TEST** in the name.
3. Confirm: (a) you land on the thank-you page, (b) the lead email arrives, (c) the Netlify dashboard
   shows the entry **with `gclid=test123`**, (d) in Google Ads **Goals → Submit Lead Form** flips to
   "Recording conversions" within a few hours.

## Copy / compliance notes (verify with client before launch)
- Page says **"licensed Ontario paralegal"** and **"LSO-licensed"** (accurate per our notes — she IS
  LSO-verified) rather than "lawyer." Keeps it policy-clean for legal-services ads.
- **"500+ cases handled"** — confirmed true in our notes; keep or adjust the number with the client.
- **"We attend court for you / most clients never appear"** — confirm this phrasing is OK with her.
- Explicit **"we do not handle parking tickets"** on the form — matches the campaign negatives and
  the lead-form copy; keeps off-target parking leads out.
