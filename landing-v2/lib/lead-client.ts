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

// Posts the lead and fires the Ads conversion. Throws with a user-facing
// message on failure so callers can render it directly.
export async function submitLead(fd: FormData): Promise<void> {
  fd.set("gclid", getGclid());
  fd.set("page", window.location.pathname);

  const res = await fetch("/api/lead", { method: "POST", body: fd });
  const json = (await res.json().catch(() => ({}))) as { ok?: boolean; error?: string };
  if (!res.ok || !json.ok) {
    throw new Error(json.error || "Something went wrong. Please try again or call us.");
  }

  // Tell Google Ads a lead converted (no-op if the tag isn't configured).
  const sendTo = process.env.NEXT_PUBLIC_GADS_CONVERSION;
  if (sendTo && typeof window.gtag === "function") {
    window.gtag("event", "conversion", { send_to: sendTo });
  }
}
