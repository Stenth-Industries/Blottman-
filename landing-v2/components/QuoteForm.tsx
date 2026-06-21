"use client";

import { useEffect, useRef, useState } from "react";
import { PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";

type Status = "idle" | "submitting" | "done" | "error";

// Fires the Google Ads conversion on a successful lead (no-op until the
// gtag.js tag + NEXT_PUBLIC_GADS_CONVERSION are configured — see layout.tsx).
declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
  }
}

// Bottom-of-page quote form. Posts to /api/lead, which emails Leslie + logs the
// lead to the Google Sheet. Captures the gclid (for later offline-conversion
// import) and uses a honeypot field for spam.
export default function QuoteForm() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");
  const gclid = useRef("");

  // Capture the Google click id from the landing URL so the lead can be tied
  // back to the ad later (offline conversion import for booked consults).
  useEffect(() => {
    const p = new URLSearchParams(window.location.search);
    gclid.current = p.get("gclid") || p.get("gbraid") || p.get("wbraid") || "";
  }, []);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("submitting");
    setError("");

    const fd = new FormData(e.currentTarget);
    fd.set("gclid", gclid.current);
    fd.set("page", typeof window !== "undefined" ? window.location.pathname : "");

    try {
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
      setStatus("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please call us.");
      setStatus("error");
    }
  }

  return (
    <section id="quote" className="relative scroll-mt-6 overflow-hidden bg-ink py-16 text-white sm:py-24">
      <div className="pointer-events-none absolute -left-40 bottom-0 h-[28rem] w-[28rem] rounded-full bg-gold/10 blur-[120px]" />
      <div className="section relative max-w-3xl">
        <div className="text-center">
          <p className="eyebrow justify-center">Free Case Review</p>
          <h2 className="display mt-4 text-4xl text-white sm:text-5xl">
            Get your <span className="text-gold-sheen">free quote.</span>
          </h2>
          <p className="mt-4 text-sm text-white/70">
            Tell us where to reach you and we&apos;ll review your ticket — no obligation.
          </p>
        </div>

        {status === "done" ? (
          <div className="mt-12 rounded-2xl border border-gold/20 bg-white/5 p-8 text-center">
            <p className="font-display text-3xl text-gold-sheen">Thank you.</p>
            <p className="mt-2 text-sm text-white/80">
              We&apos;ve got your details and will call you shortly. Need us now? Call{" "}
              <a href={`tel:${PHONE_TEL}`} className="font-semibold text-gold underline">
                {PHONE_DISPLAY}
              </a>
              .
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} encType="multipart/form-data" className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field name="name" label="Full name" autoComplete="name" className="sm:col-span-2" />
            <Field name="phone" label="Phone" type="tel" autoComplete="tel" />
            <Field name="email" label="Email" type="email" autoComplete="email" />

            {/* Honeypot — hidden from people, catches bots. */}
            <input
              type="text"
              name="company"
              tabIndex={-1}
              autoComplete="off"
              aria-hidden="true"
              className="hidden"
            />

            <label className="flex flex-col gap-1.5 sm:col-span-2">
              <span className="text-xs font-medium uppercase tracking-wide text-white/60">
                Upload your ticket <span className="text-white/35">(optional)</span>
              </span>
              <input
                name="ticket"
                type="file"
                accept="image/*,.pdf"
                className="rounded-xl border border-white/15 bg-white/5 px-4 py-3 text-sm text-white/80 outline-none transition file:mr-4 file:rounded-full file:border-0 file:bg-gold-sheen file:px-4 file:py-1.5 file:text-xs file:font-semibold file:uppercase file:tracking-wide file:text-ink hover:file:brightness-105 focus:border-gold/60 focus:bg-white/10"
              />
              <span className="text-[11px] text-white/40">
                Snap a photo of your ticket — JPG, PNG or PDF (max 6 MB).
              </span>
            </label>

            <label className="flex flex-col gap-1.5 sm:col-span-2">
              <span className="text-xs font-medium uppercase tracking-wide text-white/60">
                Brief message <span className="text-white/35">(optional)</span>
              </span>
              <textarea
                name="message"
                rows={4}
                placeholder="Tell us briefly what happened…"
                className="resize-y rounded-xl border border-white/15 bg-white/5 px-4 py-3 text-sm text-white placeholder-white/30 outline-none transition focus:border-gold/60 focus:bg-white/10"
              />
            </label>

            {status === "error" && (
              <p className="rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200 sm:col-span-2">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={status === "submitting"}
              className="btn-sheen mt-2 inline-flex items-center justify-center rounded-full bg-gold-sheen px-8 py-4 text-[13px] font-semibold uppercase tracking-[0.12em] text-ink shadow-[0_8px_24px_rgba(231,172,64,0.35)] transition hover:-translate-y-0.5 disabled:opacity-60 sm:col-span-2"
            >
              {status === "submitting" ? "Sending…" : "Get My Free Quote"}
            </button>

            <p className="text-center text-[11px] leading-relaxed text-white/40 sm:col-span-2">
              By submitting, you agree to be contacted about your case. We don&apos;t handle parking tickets.
            </p>

            <p className="text-center text-xs text-white/50 sm:col-span-2">
              Prefer to talk?{" "}
              <a href={`tel:${PHONE_TEL}`} className="font-semibold text-gold">
                Call {PHONE_DISPLAY}
              </a>
            </p>
          </form>
        )}
      </div>
    </section>
  );
}

function Field({
  name,
  label,
  type = "text",
  autoComplete,
  className = "",
}: {
  name: string;
  label: string;
  type?: string;
  autoComplete?: string;
  className?: string;
}) {
  return (
    <label className={`flex flex-col gap-1.5 ${className}`}>
      <span className="text-xs font-medium uppercase tracking-wide text-white/60">{label}</span>
      <input
        name={name}
        type={type}
        required
        autoComplete={autoComplete}
        className="rounded-xl border border-white/15 bg-white/5 px-4 py-3 text-sm text-white placeholder-white/30 outline-none transition focus:border-gold/60 focus:bg-white/10"
      />
    </label>
  );
}
