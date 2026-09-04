import { NextRequest } from "next/server";
import { formParams, logCallEvent, publicUrl, verifyTwilio } from "@/lib/twilio";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Twilio calls this once the bridged recording has finished processing, when
// TWILIO_RECORD is on. It is a separate route rather than a query string on an
// existing one because Twilio signs the full URL including the query, and
// publicUrl() rebuilds it without one, so every callback would 403.
//
// RecordingDuration is the cleanest talk time we can get: it starts when she
// answers, so unlike the duration Google counts it excludes the greeting and
// the ringing. That is the number the 45-second stenth conversion threshold
// has to be re-derived from.
//
// The URL is logged, not the audio. Twilio holds the media; nothing is copied
// into this deployment.
export async function POST(req: NextRequest) {
  const params = await formParams(req);
  if (!verifyTwilio(req, publicUrl(req, "/api/voice/recording"), params)) {
    return new Response("invalid signature", { status: 403 });
  }

  await logCallEvent({
    at: new Date().toISOString(),
    stage: "recording",
    recordingSid: params.RecordingSid || "",
    recordingUrl: params.RecordingUrl || "",
    recordingSeconds: Number(params.RecordingDuration || "0"),
    recordingChannels: params.RecordingChannels || "",
    recordingStatus: params.RecordingStatus || "",
    callSid: params.CallSid || "",
  });

  // A 204 must be constructed with a null body; an empty string still counts
  // as a body and throws, which turns the whole callback into a 500.
  return new Response(null, { status: 204 });
}
