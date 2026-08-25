import crypto from "crypto";
import type { NextRequest } from "next/server";

// Twilio voice webhook helpers.
//
// The call path is:  Google forwarding number -> Twilio number -> this app ->
// Leslie's line. Twilio answers instantly and reads a short screening prompt,
// so a caller who wants to pay a fine or find a courthouse can be turned away
// before her phone ever rings. Three months and six measurement windows show
// the junk rate flat at 42-53% no matter what we do inside Google Ads, because
// PMAX matches semantically and a negative keyword cannot block a category.
//
// Google passes the original caller's number through its forwarding number, so
// `From` here is the real caller. That is the number `call_view` will not give
// us (it exposes caller_area_code only) and the missing half of call-based
// offline conversion import.

export const TWIML_HEADERS = { "Content-Type": "text/xml; charset=utf-8" };

export function twiml(body: string): Response {
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><Response>${body}</Response>`, {
    headers: TWIML_HEADERS,
  });
}

// Escapes text going into <Say>. A caller cannot inject here, but a stray & in
// copy would make the document invalid and drop the call.
export function xml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// Twilio signs every webhook: HMAC-SHA1 over the full URL with the POST params
// appended in sorted order. Verified only when TWILIO_AUTH_TOKEN is set, so the
// endpoints still work while the account is being set up.
export function verifyTwilio(req: NextRequest, url: string, params: Record<string, string>): boolean {
  const token = process.env.TWILIO_AUTH_TOKEN;
  if (!token) return true;

  const sig = req.headers.get("x-twilio-signature");
  if (!sig) return false;

  const data = Object.keys(params)
    .sort()
    .reduce((acc, k) => acc + k + params[k], url);
  const expected = crypto.createHmac("sha1", token).update(Buffer.from(data, "utf-8")).digest("base64");

  const a = Buffer.from(sig);
  const b = Buffer.from(expected);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

// The URL Twilio signed. Behind Vercel's proxy the request URL is the internal
// one, so rebuild it from the forwarded headers, or from an explicit override
// if the deployment sits behind something that rewrites the host.
export function publicUrl(req: NextRequest, path: string): string {
  const base = process.env.TWILIO_PUBLIC_BASE_URL;
  if (base) return base.replace(/\/$/, "") + path;
  const proto = req.headers.get("x-forwarded-proto") || "https";
  const host = req.headers.get("x-forwarded-host") || req.headers.get("host") || "";
  return `${proto}://${host}${path}`;
}

export async function formParams(req: NextRequest): Promise<Record<string, string>> {
  const fd = await req.formData();
  const out: Record<string, string> = {};
  fd.forEach((v, k) => {
    if (typeof v === "string") out[k] = v;
  });
  return out;
}

// Every screening decision is logged in one shape so the keypress can be
// counted. This is the first direct measurement of the junk rate we have ever
// had: today it is inferred from call duration and area code.
export async function logCallEvent(event: Record<string, unknown>): Promise<void> {
  console.log("[voice]", JSON.stringify(event));
  const url = process.env.CALL_LOG_WEBHOOK_URL;
  if (!url) return;
  try {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(event),
    });
  } catch (err) {
    console.error("[voice] call log fan-out failed (non-fatal)", err);
  }
}
