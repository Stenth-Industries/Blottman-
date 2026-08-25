import { NextRequest } from "next/server";
import { formParams, logCallEvent, publicUrl, twiml, verifyTwilio, xml } from "@/lib/twilio";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Entry point for every Google Ads call. Twilio answers immediately and reads
// the screening prompt; the caller can press a key at any point during it, so a
// real client is through in a few seconds while a payment or courthouse caller
// presses 2 and never reaches her phone.
//
// Wording is Leslie's own, from WhatsApp on Aug 20. Left verbatim: it is her
// firm answering her phone, and it is good copy anyway. Both options are
// framed symmetrically, which is what makes a wrong-number caller self-select
// instead of pressing 1 to reach a human.
const GREETING =
  "Thanks for calling Blottman Legal Services. If you have received a traffic " +
  "ticket or summons to court, press 1. To pay a fine or reach a courthouse, press 2.";

// Played instead of the greeting outside business hours, when configured. See
// AFTER_HOURS below: the default is to ring her anyway.
const AFTER_HOURS =
  "Thanks for calling Blottman Legal Services. Our office is closed right now. " +
  "Please leave us your details for a free case review at blottman dot C A, " +
  "or call back during business hours and we will be glad to help.";

const VOICE = "Polly.Joanna";

// "ring" (default) puts after-hours callers through exactly like any other
// call. "message" plays AFTER_HOURS and hangs up. Open question with Leslie as
// of Aug 20, so the default is the one that cannot lose her a client.
const AFTER_HOURS_MODE = process.env.TWILIO_AFTER_HOURS === "message" ? "message" : "ring";
const OPEN_HOUR = Number(process.env.TWILIO_OPEN_HOUR || "9");
const CLOSE_HOUR = Number(process.env.TWILIO_CLOSE_HOUR || "19");

// Her hours are Toronto time and the server is not, so read the hour in her
// timezone rather than the machine's.
function torontoHour(): number {
  const s = new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Toronto",
    hour: "numeric",
    hour12: false,
  }).format(new Date());
  return Number(s);
}

export async function POST(req: NextRequest) {
  const params = await formParams(req);
  if (!verifyTwilio(req, publicUrl(req, "/api/voice"), params)) {
    return new Response("invalid signature", { status: 403 });
  }

  const hour = torontoHour();
  const closed = hour < OPEN_HOUR || hour >= CLOSE_HOUR;

  await logCallEvent({
    at: new Date().toISOString(),
    stage: "greeting",
    torontoHour: hour,
    closed,
    callSid: params.CallSid || "",
    from: params.From || "",
    to: params.To || "",
    fromCity: params.FromCity || "",
    fromState: params.FromState || "",
  });

  if (closed && AFTER_HOURS_MODE === "message") {
    return twiml(`<Say voice="${VOICE}">${xml(AFTER_HOURS)}</Say><Hangup/>`);
  }

  // actionOnEmptyResult sends us the timeout case too, where we connect the
  // call anyway. Failing open matters: a caller who is confused, on a rotary
  // phone, or simply slow is far more expensive to drop than a junk call is to
  // let through.
  return twiml(
    `<Gather numDigits="1" timeout="7" actionOnEmptyResult="true" ` +
      `action="/api/voice/screen" method="POST">` +
      `<Say voice="${VOICE}">${xml(GREETING)}</Say>` +
      `</Gather>`
  );
}
