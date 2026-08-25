// Client-side lead submission shared by QuoteForm (bottom of page) and
// QuickForm (under the hero). Attaches the Google click id + page, posts to
// /api/lead, and fires the Google Ads conversion on success.

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
  }
}

// Google click id from the landing URL so the lead can be tied back to the ad
// later (offline conversion import for booked consults). Read at submit time —
// these pages never client-navigate, so the search params don't change.
export function getGclid(): string {
  const p = new URLSearchParams(window.location.search);
  return p.get("gclid") || p.get("gbraid") || p.get("wbraid") || "";
}

// Groups the two posts a single QuickForm visitor can make (the abandonment
// beacon and the finished submit) so the server can label the second one as an
// update instead of letting Leslie think it is a second person.
export function newLeadId(): string {
  const c = globalThis.crypto;
  if (c && typeof c.randomUUID === "function") return c.randomUUID();
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

function withContext(fd: FormData): FormData {
  fd.set("gclid", getGclid());
  fd.set("page", window.location.pathname);
  return fd;
}

// Posts the lead and fires the Ads conversion. Throws with a user-facing
// message on failure so callers can render it directly.
export async function submitLead(fd: FormData): Promise<void> {
  withContext(fd);

  const res = await fetch("/api/lead", { method: "POST", body: fd });
  const json = (await res.json().catch(() => ({}))) as { ok?: boolean; error?: string };
  if (!res.ok || !json.ok) {
    throw new Error(json.error || "Something went wrong. Please try again or call us.");
  }

  fireConversion();
}

// Delivers a partial lead (charge + phone, no name) while the page is being
// torn down. A visitor who gives us a number and then leaves is still a lead
// Leslie can call — before this, that visitor was simply lost.
//
// sendBeacon is the only send that survives unload; it takes FormData, which
// the route already parses. Returns whether the browser accepted it.
export function beaconPartialLead(fd: FormData): boolean {
  try {
    withContext(fd);
    if (typeof navigator.sendBeacon === "function") {
      return navigator.sendBeacon("/api/lead", fd);
    }
    // Very old browsers: keepalive fetch is the next best thing.
    void fetch("/api/lead", { method: "POST", body: fd, keepalive: true });
    return true;
  } catch {
    return false;
  }
}

// Tell Google Ads a lead converted (no-op if the tag isn't configured).
export function fireConversion(): void {
  const sendTo = process.env.NEXT_PUBLIC_GADS_CONVERSION;
  if (sendTo && typeof window.gtag === "function") {
    window.gtag("event", "conversion", { send_to: sendTo });
  }
}
