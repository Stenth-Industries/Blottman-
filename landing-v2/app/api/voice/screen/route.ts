import { NextRequest } from "next/server";
import { formParams, logCallEvent, publicUrl, twiml, verifyTwilio, xml } from "@/lib/twilio";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const VOICE = "Polly.Joanna";

// Leslie's real line. Everything that reaches here is a call she would have
// received anyway; the only question is whether it is worth her time.
//
// Normalised rather than trusted. A ten-digit North American number set without
// its country code gets a "+" from Twilio and is then read as an international
// dial: 7057901965 became +7 057901965, country code 7, and failed instantly
// with the caller hearing our no-answer message a second later. That is a
// silent, total outage of the call path, caused by a typo in an env var.
function normalizePhone(raw: string): string {
  const trimmed = raw.trim();
  if (trimmed.startsWith("+")) return trimmed;
  const digits = trimmed.replace(/\D/g, "");
  if (digits.length === 10) return "+1" + digits;
  if (digits.length === 11 && digits.startsWith("1")) return "+" + digits;
  return "+" + digits;
}

const OFFICE_LINE = normalizePhone(process.env.TWILIO_FORWARD_TO || "+16477947750");

// Leslie's wording, from WhatsApp on Aug 20, with a goodbye added so the line
// does not simply go dead.
const WRONG_NUMBER =
  "Please contact the courthouse that issued your ticket for assistance in " +
  "payment or inquiries. Goodbye.";

export async function POST(req: NextRequest) {
  const params = await formParams(req);
  if (!verifyTwilio(req, publicUrl(req, "/api/voice/screen"), params)) {
    return new Response("invalid signature", { status: 403 });
  }

  const digits = (params.Digits || "").trim();
  // Only an explicit 2 is turned away. No input, a mis-key, or anything else
  // connects — see the fail-open note in the greeting route.
  const outcome = digits === "2" ? "declined" : digits === "1" ? "accepted" : "no_input";

  await logCallEvent({
    at: new Date().toISOString(),
    stage: "screened",
    outcome,
    digits,
    dialing: outcome === "declined" ? "" : OFFICE_LINE,
    callSid: params.CallSid || "",
    from: params.From || "",
  });

  if (outcome === "declined") {
    return twiml(`<Say voice="${VOICE}">${xml(WRONG_NUMBER)}</Say><Hangup/>`);
  }

  // answerOnBridge keeps real ringback in the caller's ear instead of silence
  // while her phone rings, and stops Twilio billing the leg as answered until
  // she actually picks up. The caller's own number is passed through as the
  // caller id, so her handset shows who is calling exactly as it does today.
  return twiml(
    `<Dial timeout="25" answerOnBridge="true" action="/api/voice/complete" method="POST">` +
      `<Number>${xml(OFFICE_LINE)}</Number>` +
      `</Dial>`
  );
}
