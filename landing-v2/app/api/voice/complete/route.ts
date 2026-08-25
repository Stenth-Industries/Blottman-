import { NextRequest } from "next/server";
import { formParams, logCallEvent, publicUrl, twiml, verifyTwilio, xml } from "@/lib/twilio";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const VOICE = "Polly.Joanna";

const NO_ANSWER =
  "Sorry, we could not reach the office. Please try again shortly, or request a " +
  "free case review at blottman dot C A.";

// Runs when the <Dial> ends, for any reason. Two jobs.
//
// 1. Say something useful when her line did not pick up. TwiML placed after a
//    <Dial> that has an action URL is never executed, so this is the only place
//    the no-answer message can live.
//
// 2. Record the numbers that make call measurement possible. DialCallDuration
//    is the real conversation length, separate from the total call, which
//    includes the greeting and the ringing. Google only ever sees the total,
//    which is why the 45-second conversion threshold has to be re-derived from
//    these logs rather than guessed at. `From` plus the call start time is also
//    exactly the key that call-based offline conversion import needs, and it is
//    the half `call_view` cannot give us.
export async function POST(req: NextRequest) {
  const params = await formParams(req);
  if (!verifyTwilio(req, publicUrl(req, "/api/voice/complete"), params)) {
    return new Response("invalid signature", { status: 403 });
  }

  const status = params.DialCallStatus || "";
  const talk = Number(params.DialCallDuration || "0");

  await logCallEvent({
    at: new Date().toISOString(),
    stage: "completed",
    dialStatus: status,
    talkSeconds: talk,
    callSid: params.CallSid || "",
    from: params.From || "",
    to: params.To || "",
  });

  if (status === "completed") {
    return twiml("<Hangup/>");
  }
  // no-answer, busy, failed, canceled
  return twiml(`<Say voice="${VOICE}">${xml(NO_ANSWER)}</Say><Hangup/>`);
}
