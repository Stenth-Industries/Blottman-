// ── Blottman Legal Services — lead webhook (Google Apps Script) ──────────────────────────
// Paste this into the Sheet's Apps Script editor (Extensions → Apps Script),
// Save, then Deploy → New deployment → Web app (Execute as: Me, Access: Anyone).
// It logs each lead to the Sheet AND emails it from your Google account.
//
// Sheet header row (row 1): ts | name | phone | email | charge | message | gclid | page | ticket

// Where leads are emailed. Comma-separate for several; cc optional.
const TO_EMAIL = "info@stenth.com";
const CC_EMAIL = ""; // e.g. "leslie@example.com" when you add her

// Auto-reply sent to the person who filled out the form.
const REPLY_FROM_NAME = "Blottman Legal Services";
const REPLY_SUBJECT = "We've got your case — Blottman Legal Services";
const PHONE_DISPLAY = "(647) 794-7750";
const PHONE_TEL = "+16477947750";
const SITE_URL = "https://blottman.ca";

// Brand palette (gardewilson-style black & gold)
const C = {
  ink: "#0e0e0f",       // near-black background
  panel: "#161617",     // card background
  line: "#2a2a2c",      // hairline borders
  gold: "#e7ac40",      // primary brand gold
  goldBright: "#f5c03d",// highlight gold
  text: "#e8e6e1",      // light body text
  muted: "#9b988f",     // secondary text
};

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    const sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    sh.appendRow([d.ts, d.name, d.phone, d.email, d.charge || "", d.message, d.gclid, d.page, d.ticket_name || ""]);

    const body =
      "New traffic-ticket lead\n\n" +
      "Name:    " + d.name + "\n" +
      "Phone:   " + d.phone + "\n" +
      "Email:   " + d.email + "\n" +
      "Charge:  " + (d.charge || "—") + "\n" +
      "Message: " + (d.message || "—") + "\n" +
      "gclid:   " + (d.gclid || "—") + "\n" +
      "Page:    " + (d.page || "—") + "\n";

    const msg = {
      to: TO_EMAIL,
      subject: "New case review request — " + d.name,
      body: body,
      name: "Blottman Legal Services Leads",
      replyTo: d.email || TO_EMAIL,
    };
    if (CC_EMAIL) msg.cc = CC_EMAIL;
    if (d.ticket_b64) {
      msg.attachments = [
        Utilities.newBlob(Utilities.base64Decode(d.ticket_b64), d.ticket_mime, d.ticket_name),
      ];
    }
    MailApp.sendEmail(msg);

    // Auto-reply to the lead (only if they gave a valid-looking email).
    if (d.email && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) {
      const firstName = (d.name || "").trim().split(/\s+/)[0] || "there";
      MailApp.sendEmail({
        to: d.email,
        subject: REPLY_SUBJECT,
        body: autoReplyText(firstName),       // plain-text fallback
        htmlBody: autoReplyHtml(firstName),   // the pretty version
        name: REPLY_FROM_NAME,
        replyTo: TO_EMAIL,
      });
    }

    return ok({ ok: true });
  } catch (err) {
    return ok({ ok: false, error: String(err) });
  }
}

function ok(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// ── Preview helper ───────────────────────────────────────────────────────────
// Run this from the editor (select testAutoReply → Run) to email a preview of
// the auto-reply, so you can see exactly what a lead receives. No real lead
// involved — it always sends to the test address below.
const TEST_EMAIL = "brothersify10@gmail.com";
function testAutoReply() {
  MailApp.sendEmail({
    to: TEST_EMAIL,
    subject: "[TEST] " + REPLY_SUBJECT,
    body: autoReplyText("Alex"),
    htmlBody: autoReplyHtml("Alex"),
    name: REPLY_FROM_NAME,
    replyTo: TO_EMAIL,
  });
  Logger.log("Test auto-reply sent to " + TEST_EMAIL);
}

// ── Auto-reply (plain text fallback) ─────────────────────────────────────────
function autoReplyText(firstName) {
  return (
    "Hi " + firstName + ",\n\n" +
    "Thank you for contacting Blottman Legal Services. We've received your request for a " +
    "free case review, and a member of our team will get back to you, usually " +
    "within one business day.\n\n" +
    "In the meantime, we recommend not paying the fine or pleading guilty until " +
    "we've had a chance to review your ticket, as that can affect your demerit " +
    "points and insurance.\n\n" +
    "If you'd like to speak with us sooner, call " + PHONE_DISPLAY + " or simply " +
    "reply to this email.\n\n" +
    "Warm regards,\n" +
    "Leslie Rivas\n" +
    "Blottman Legal Services\n" +
    SITE_URL + "\n"
  );
}

// ── Auto-reply (HTML — clean, simple, professional; inline styles) ───────────
function autoReplyHtml(firstName) {
  return (
'<!doctype html><html><body style="margin:0;padding:0;background:#f4f4f5;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;">' +
  '<tr><td align="center" style="padding:32px 16px;">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:540px;background:#ffffff;border:1px solid #e5e5e7;border-radius:8px;">' +

      // ── Header ──
      '<tr><td style="padding:28px 36px;border-bottom:3px solid #e7ac40;">' +
        '<div style="font:700 18px/1.2 Georgia,\'Times New Roman\',serif;color:#1a1a1a;">Blottman Legal Services</div>' +
        '<div style="font:400 13px/1.2 Arial,Helvetica,sans-serif;color:#777;margin-top:4px;">Ontario Traffic-Ticket Defence</div>' +
      '</td></tr>' +

      // ── Body ──
      '<tr><td style="padding:32px 36px 8px 36px;">' +
        '<p style="font:400 16px/1.6 Arial,Helvetica,sans-serif;color:#1a1a1a;margin:0 0 16px 0;">Hi ' + firstName + ',</p>' +
        '<p style="font:400 15px/1.65 Arial,Helvetica,sans-serif;color:#3a3a3a;margin:0 0 16px 0;">' +
          'Thank you for contacting Blottman Legal Services. We\'ve received your request for a free case review, ' +
          'and a member of our team will get back to you, usually within one business day.</p>' +
        '<p style="font:400 15px/1.65 Arial,Helvetica,sans-serif;color:#3a3a3a;margin:0 0 16px 0;">' +
          'In the meantime, we recommend not paying the fine or pleading guilty until we\'ve had a chance ' +
          'to review your ticket, as that can affect your demerit points and insurance.</p>' +
        '<p style="font:400 15px/1.65 Arial,Helvetica,sans-serif;color:#3a3a3a;margin:0 0 8px 0;">' +
          'If you\'d like to speak with us sooner, you can reach us at ' +
          '<a href="tel:' + PHONE_TEL + '" style="color:#b8860b;text-decoration:none;font-weight:bold;">' + PHONE_DISPLAY + '</a> ' +
          'or simply reply to this email.</p>' +
      '</td></tr>' +

      // ── Sign-off ──
      '<tr><td style="padding:16px 36px 32px 36px;">' +
        '<p style="font:400 15px/1.6 Arial,Helvetica,sans-serif;color:#1a1a1a;margin:0;">Warm regards,<br>' +
          '<strong>Leslie Rivas</strong><br>' +
          '<span style="color:#777;">Blottman Legal Services</span></p>' +
      '</td></tr>' +

      // ── Footer ──
      '<tr><td style="padding:20px 36px;border-top:1px solid #eeeeee;background:#fafafa;border-radius:0 0 8px 8px;">' +
        '<div style="font:400 12px/1.6 Arial,Helvetica,sans-serif;color:#888;">' +
          'Blottman Legal Services &nbsp;&middot;&nbsp; ' + PHONE_DISPLAY + ' &nbsp;&middot;&nbsp; ' +
          '<a href="' + SITE_URL + '" style="color:#b8860b;text-decoration:none;">blottman.ca</a><br>' +
          '<span style="color:#aaa;">You received this email because you requested a free case review at blottman.ca.</span>' +
        '</div>' +
      '</td></tr>' +

    '</table>' +
  '</td></tr>' +
'</table></body></html>'
  );
}
