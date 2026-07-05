import { NextRequest, NextResponse } from "next/server";

// Lead intake for the QuoteForm. Forwards the submission to a single Google
// Apps Script web app (LEAD_WEBHOOK_URL) that BOTH logs the lead to a Sheet and
// emails it via the Google account — no third-party email provider, no API keys.
//
// NOTE: ticket-photo upload was removed (Law Society of Ontario rules — we can't
// review a ticket without a conflict check + signed retainer). Leads are plain
// contact submissions now.
//
// Env (see LEAD_FORM_SETUP.md):
//   LEAD_WEBHOOK_URL       — the Apps Script web-app /exec URL (primary: email + auto-reply + Sheet)
//   N8N_LEAD_WEBHOOK_URL   — optional n8n fan-out (instant alert + Lead Tracker row); best-effort,
//                            a failure here never blocks or fails the lead
// If unset, the lead is logged to the server console (dev) and still returns ok.

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  let form: FormData;
  try {
    form = await req.formData();
  } catch {
    return bad("Invalid submission.");
  }

  // Honeypot: real users never fill "company". Bots do → accept & drop.
  if (str(form.get("company"))) {
    return NextResponse.json({ ok: true });
  }

  const lead = {
    name: str(form.get("name")),
    phone: str(form.get("phone")),
    email: str(form.get("email")),
    charge: str(form.get("charge")),
    message: str(form.get("message")),
    gclid: str(form.get("gclid")),
    page: str(form.get("page")),
    ts: new Date().toISOString(),
  };

  // Only name + phone are required — Leslie calls leads back, so email and a
  // written message are optional (fewer required fields = fewer abandons).
  if (!lead.name || !lead.phone) {
    return bad("Please fill in your name and phone number.");
  }

  const url = process.env.LEAD_WEBHOOK_URL;
  if (!url) {
    console.warn("[lead] LEAD_WEBHOOK_URL not set — lead not delivered:", lead);
    return NextResponse.json({ ok: true });
  }

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lead),
      // Apps Script answers from script.googleusercontent.com — allow the redirect.
      redirect: "follow",
    });
    if (!res.ok) throw new Error(`webhook ${res.status}: ${await res.text()}`);
  } catch (err) {
    console.error("[lead] webhook failed", err);
    return NextResponse.json(
      { ok: false, error: "Something went wrong on our end. Please call us so we don't miss you." },
      { status: 502 }
    );
  }

  // Best-effort fan-out to n8n (instant alert + Lead Tracker). Must never
  // affect the response — the lead is already safely delivered above.
  const n8nUrl = process.env.N8N_LEAD_WEBHOOK_URL;
  if (n8nUrl) {
    try {
      await fetch(n8nUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(lead),
      });
    } catch (err) {
      console.error("[lead] n8n fan-out failed (non-fatal)", err);
    }
  }

  return NextResponse.json({ ok: true });
}

function str(v: FormDataEntryValue | null): string {
  return typeof v === "string" ? v.trim() : "";
}

function bad(error: string) {
  return NextResponse.json({ ok: false, error }, { status: 400 });
}
