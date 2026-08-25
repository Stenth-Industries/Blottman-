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

// A submission arrives in one of three shapes:
//   complete — the whole form was filled in. The normal case.
//   partial  — the visitor gave their charge and phone in QuickForm step 1 and
//              then left. Sent by sendBeacon during page unload. A phone number
//              and a named charge is a callable lead, so we deliver it rather
//              than throwing it away, which is what used to happen.
//   update   — the same visitor came back and finished after we already
//              delivered their partial. Matched by leadId, and labelled so it
//              reads as more detail on an existing lead, not a second person.
type Stage = "complete" | "partial" | "update";

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

  const stage = stageOf(form.get("stage"));
  const lead = {
    name: str(form.get("name")),
    phone: str(form.get("phone")),
    email: str(form.get("email")),
    charge: str(form.get("charge")),
    message: str(form.get("message")),
    gclid: str(form.get("gclid")),
    page: str(form.get("page")),
    leadId: str(form.get("leadId")),
    stage,
    ts: new Date().toISOString(),
  };

  // Phone plus a charge is the floor: it is everything Leslie needs to call
  // back and decide whether the case is hers. Name is required as soon as the
  // visitor is actually filling the form in; it is waived only for a partial,
  // where by definition they left before reaching that field.
  //
  // Email and the ticket description are optional on purpose. They were made
  // required on Aug 1 and Aug 12 and the Search conversion rate fell from
  // 4.96% to 0.43% over the same window — four required fields including a
  // free-text box, on traffic that is ~95% mobile. The charge dropdown does
  // the pre-screening the description was added for: it is a closed list of
  // the nine offences Leslie takes, so a parking-fine or payment enquiry
  // cannot pick one.
  if (!lead.phone || !lead.charge) {
    return bad("Please give us a phone number and the charge you're facing.");
  }
  if (stage !== "partial" && !lead.name) {
    return bad("Please fill in your name and phone number.");
  }

  // Keep the downstream payload shape identical to what the Apps Script and the
  // n8n workflows already read (name / message are rendered straight into the
  // alert email), so a partial or an update explains itself in Leslie's inbox
  // without either of those needing a change.
  if (stage === "partial") {
    lead.name = lead.name || "No name given";
    lead.message =
      "PARTIAL FORM. This visitor selected their charge and gave a phone number, " +
      "then left the page before finishing. The number and the charge are what they typed. " +
      "Worth a callback.";
  } else if (stage === "update") {
    lead.message =
      "MORE DETAIL ON THE LEAD ALREADY SENT FOR " + lead.phone + ". " +
      (lead.message || "No description given.");
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

function stageOf(v: FormDataEntryValue | null): Stage {
  const s = str(v);
  return s === "partial" || s === "update" ? s : "complete";
}

function str(v: FormDataEntryValue | null): string {
  return typeof v === "string" ? v.trim() : "";
}

function bad(error: string) {
  return NextResponse.json({ ok: false, error }, { status: 400 });
}
