# Quote-form lead capture — setup

The form (`components/QuoteForm.tsx`) posts to `app/api/lead/route.ts`, which:

1. **Emails the lead** to Leslie (+ optional cc) — via Resend.
2. **Logs it to a Google Sheet** — the zero-cost "mini-CRM" (optional).
3. **Fires the Google Ads conversion** on success (optional).
4. **Captures the `gclid`** so leads can be tied to the ad later (offline conversion import for booked consults).

Spam is handled by a honeypot field. The optional ticket photo is attached to the email (max 6 MB).

> Until the env vars are set the form still works — leads just get written to the server console instead of delivered. Set the vars in `.env.local` (local) and in your host's env settings (e.g. Vercel → Project → Settings → Environment Variables). Copy `.env.local.example` to start.

---

## 1. Email (Resend) — required for leads to actually arrive

1. Create a free account at a.
2. **Add & verify a domain** (`blottman.com`) under Domains, or skip for testing and send from `onboarding@resend.dev`.
3. Create an API key → set `RESEND_API_KEY`.
4. Set `LEAD_TO_EMAIL` to Leslie's email (comma-separate for several). Optional `LEAD_CC_EMAIL=info@stenth.com`.
5. Set `LEAD_FROM_EMAIL` to a verified-domain address (e.g. `Blottman Leads <leads@blottman.com>`); omit while testing to use `onboarding@resend.dev`.

## 2. Google Sheet log (optional but recommended)

1. New Google Sheet. Header row: `ts | name | phone | email | message | gclid | page | ticket`.
2. Extensions → **Apps Script**, paste:

   ```js
   function doPost(e) {
     const d = JSON.parse(e.postData.contents);
     const sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
     sh.appendRow([d.ts, d.name, d.phone, d.email, d.message, d.gclid, d.page, d.ticket]);
     return ContentService.createTextOutput(JSON.stringify({ ok: true }))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```

3. Deploy → **New deployment** → type **Web app** → Execute as *me*, Who has access *Anyone* → copy the URL.
4. Set `GOOGLE_SHEET_WEBHOOK_URL` to that URL.

This sheet is your running lead log — add a "Booked?" column to mark consults (feeds the $500 OCI later).

## 3. Google Ads conversion (optional)

In Google Ads, open the existing **`Submit Lead Form`** conversion action (id `7173263227`). Use its tag snippet to read:

- `NEXT_PUBLIC_GADS_ID` = the `AW-XXXXXXXXXX` tag id.
- `NEXT_PUBLIC_GADS_CONVERSION` = the `send_to` value `AW-XXXXXXXXXX/yyyyyyyyyyyyy` (id **and** label).

Once set, a successful submit fires `gtag('event','conversion', {send_to: …})` and the action finally counts (it's been firing 0 because its tag was never installed). This gives PMAX/Search a *real* lead signal instead of the codeless "Contact Us".

## Test

- `npm run dev`, submit the form. With no env set, check the terminal for `[lead] … email skipped` + the payload.
- With Resend set, the email should arrive; check Resend's dashboard logs if not.
