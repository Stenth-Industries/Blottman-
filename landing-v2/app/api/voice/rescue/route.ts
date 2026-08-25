import { NextRequest } from "next/server";
import { dialOffice, formParams, logCallEvent, publicUrl, twiml, verifyTwilio, xml } from "@/lib/twilio";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const VOICE = "Polly.Joanna";
const GOODBYE = "Goodbye.";

// Last chance for a caller who pressed 2 by mistake. A 1 here bridges exactly
// as a 1 at the first prompt would have; anything else, including silence,
// ends the call. Someone who genuinely wanted the courthouse already has their
// answer and rings off during the offer.
//
// `rescued` in the log separates these from first-prompt accepts, so a rising
// count here would mean the greeting is being misheard rather than that the
// gate is working.
export async function POST(req: NextRequest) {
  const params = await formParams(req);
  if (!verifyTwilio(req, publicUrl(req, "/api/voice/rescue"), params)) {
    return new Response("invalid signature", { status: 403 });
  }

  const rescued = (params.Digits || "").trim() === "1";

  await logCallEvent({
    at: new Date().toISOString(),
    stage: "rescue",
    outcome: rescued ? "rescued" : "declined_final",
    callSid: params.CallSid || "",
    from: params.From || "",
  });

  if (rescued) return twiml(dialOffice());
  return twiml(`<Say voice="${VOICE}">${xml(GOODBYE)}</Say><Hangup/>`);
}
