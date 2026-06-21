// ── Blottman Law — lead webhook (Google Apps Script) ──────────────────────────
// Paste this into the Sheet's Apps Script editor (Extensions → Apps Script),
// Save, then Deploy → New deployment → Web app (Execute as: Me, Access: Anyone).
// It logs each lead to the Sheet AND emails it from your Google account.
//
// Sheet header row (row 1): ts | name | phone | email | message | gclid | page | ticket

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
