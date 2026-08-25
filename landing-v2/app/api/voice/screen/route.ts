import { NextRequest } from "next/server";
import {
  OFFICE_LINE,
  dialOffice,
  formParams,
  logCallEvent,
  publicUrl,
  twiml,
  verifyTwilio,
  xml,
} from "@/lib/twilio";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const VOICE = "Polly.Joanna";

// Leslie's wording, from WhatsApp on Aug 20.
const WRONG_NUMBER =
  "Please contact the courthouse that issued your ticket for assistance in " +
  "payment or inquiries.";

// Pressing 2 was the only irreversible path in the flow; everything else fails
// open. A real client who fat-fingers 2 on a mobile keypad would have been hung
// up on, after we had already paid for the click. So the decline is offered one
// way back, on its own route rather than a query string, because Twilio signs
// the full URL including the query and publicUrl() builds it without one.
const SECOND_CHANCE =
  "If you reached this by mistake and you have a traffic ticket you want to " +
  "fight, press 1 now.";

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
    return twiml(
      `<Say voice="${VOICE}">${xml(WRONG_NUMBER)}</Say>` +
        `<Gather numDigits="1" timeout="5" actionOnEmptyResult="true" ` +
        `action="/api/voice/rescue" method="POST">` +
        `<Say voice="${VOICE}">${xml(SECOND_CHANCE)}</Say>` +
        `</Gather>`
    );
  }

  return twiml(dialOffice());
}
