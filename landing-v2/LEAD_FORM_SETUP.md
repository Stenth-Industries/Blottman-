# Quote-form lead capture — setup (Google Apps Script, no email provider)

The form (`components/QuoteForm.tsx`) posts to `app/api/lead/route.ts`, which forwards
the lead to **one Google Apps Script web app**. That script:

1. **Logs the lead to a Google Sheet** (your running "mini-CRM").
2. **Emails the lead** to you via your Google account (`MailApp`) — no Resend, no API keys.
3. Attaches the optional **ticket photo** (passed through as base64).

The route also captures the **`gclid`** (for later offline-conversion import) and a
honeypot blocks spam. The Google Ads conversion fires on success once configured.

> Until `LEAD_WEBHOOK_URL` is set the form still works — leads are written to the server
> console instead of delivered. Set it in `.env.local` (local) and in Vercel (production).

---

## 1. Create the Sheet

New Google Sheet (signed in as **info@stenth.com**). First row = headers:

```
ts | name | phone | email | message | gclid | page | ticket
```

## 2. Add the Apps Script

In the Sheet: **Extensions → Apps Script**. Delete the stub and paste:

```js
// Where leads are emailed. Comma-separate for several; cc optional.
const TO_EMAIL = "info@stenth.com";
const CC_EMAIL = ""; // e.g. "leslie@example.com" when you add her

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    const sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    sh.appendRow([d.ts, d.name, d.phone, d.email, d.message, d.gclid, d.page, d.ticket_name || ""]);

    const body =
      "New traffic-ticket lead\n\n" +
      "Name:    " + d.name + "\n" +
      "Phone:   " + d.phone + "\n" +
      "Email:   " + d.email + "\n" +
      "Message: " + (d.message || "—") + "\n" +
      "gclid:   " + (d.gclid || "—") + "\n" +
      "Page:    " + (d.page || "—") + "\n";

    const msg = {
      to: TO_EMAIL,
      subject: "New case review request — " + d.name,
      body: body,
      name: "Blottman Law Leads",
      replyTo: d.email || TO_EMAIL,
    };
    if (CC_EMAIL) msg.cc = CC_EMAIL;
    if (d.ticket_b64) {
      msg.attachments = [
        Utilities.newBlob(Utilities.base64Decode(d.ticket_b64), d.ticket_mime, d.ticket_name),
      ];
    }
    MailApp.sendEmail(msg);

    return ok({ ok: true });
  } catch (err) {
    return ok({ ok: false, error: String(err) });
  }
}

function ok(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
```

## 3. Deploy it

- **Deploy → New deployment** → gear icon → **Web app**.
- **Execute as:** Me (info@stenth.com).
- **Who has access:** **Anyone**.
- **Deploy** → approve the permission prompt (it needs Sheets + send-email; click *Advanced → Go to project → Allow*).
- Copy the **Web app URL** (ends in `/exec`).

## 4. Wire it up

- `landing-v2/.env.local` → `LEAD_WEBHOOK_URL=<the /exec URL>`
- Vercel → Project → Settings → Environment Variables → add the same `LEAD_WEBHOOK_URL`
  for **Production** + **Preview**, then **redeploy**.

## 5. Test

```
cd landing-v2 && npm run dev
```
Submit the form → row appears in the Sheet **and** a "Blottman Law Leads" email arrives at
info@stenth.com. (No URL set? The lead prints to the terminal — nothing breaks.)

---

### Notes
- **Quota:** ~100 emails/day on consumer Gmail, 1,500 on Workspace — plenty for leads.
- **Edits to the script:** after changing the code you must **Deploy → Manage deployments →
  edit → Version: New version** for the change to go live (or the `/exec` URL keeps the old code).
- **Adding Leslie later:** just set `CC_EMAIL` (or add to `TO_EMAIL`) in the script and redeploy —
  no app change needed.
- **Booked consults / $500 OCI:** add a "Booked?" column to the Sheet to mark real consults;
  with the captured gclid that feeds offline conversion import later.

## Google Ads conversion (optional, later)

From the existing **`Submit Lead Form`** action (id `7173263227`) in Google Ads, set in Vercel:
`NEXT_PUBLIC_GADS_ID` (`AW-XXXXXXXXXX`) and `NEXT_PUBLIC_GADS_CONVERSION` (`AW-…/label`). On a
successful submit the form fires `gtag('event','conversion', …)` so the action finally counts.
