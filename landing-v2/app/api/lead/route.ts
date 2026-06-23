import { NextRequest, NextResponse } from "next/server";

// Lead intake for the QuoteForm. Forwards the submission to a single Google
// Apps Script web app (LEAD_WEBHOOK_URL) that BOTH logs the lead to a Sheet and
// emails it via the Google account — no third-party email provider, no API keys.
// The optional ticket photo is passed through as base64 for the script to attach.
//
// Env (see LEAD_FORM_SETUP.md):
//   LEAD_WEBHOOK_URL   — the Apps Script web-app /exec URL
// If unset, the lead is logged to the server console (dev) and still returns ok.

export const runtime = "nodejs";

// 4 MB cap — Vercel rejects request bodies over ~4.5 MB before this route runs,
// so keep the ticket photo (plus form fields) safely under that platform limit.
const MAX_FILE_BYTES = 4 * 1024 * 1024;

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
    ticket_name: "",
    ticket_mime: "",
    ticket_b64: "",
  };

  if (!lead.name || !lead.phone || !lead.email || !lead.message) {
    return bad("Please fill in your name, phone, email and a brief message.");
  }

  // Optional ticket photo → base64 so the script can attach it to the email.
  const file = form.get("ticket");
  if (file instanceof File && file.size > 0) {
    if (file.size > MAX_FILE_BYTES) {
      return bad("Ticket image is too large (max 4 MB).");
    }
    const buf = Buffer.from(await file.arrayBuffer());
    lead.ticket_name = file.name || "ticket";
    lead.ticket_mime = file.type || "application/octet-stream";
    lead.ticket_b64 = buf.toString("base64");
  }

  const url = process.env.LEAD_WEBHOOK_URL;
  if (!url) {
    const { ticket_b64, ...safe } = lead; // don't dump the base64 blob
    console.warn("[lead] LEAD_WEBHOOK_URL not set — lead not delivered:", safe);
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

  return NextResponse.json({ ok: true });
}

function str(v: FormDataEntryValue | null): string {
  return typeof v === "string" ? v.trim() : "";
}

function bad(error: string) {
  return NextResponse.json({ ok: false, error }, { status: 400 });
}
