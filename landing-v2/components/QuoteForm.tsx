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
    <section id="quote" className="relative scroll-mt-6 overflow-hidden bg-ink py-16 text-white sm:py-32">
      {/* Background glow */}
      <div className="pointer-events-none absolute -left-40 bottom-0 h-[28rem] w-[28rem] rounded-full bg-gold/10 blur-[120px]" />
      
      <div className="section relative">
        <div className="grid grid-cols-1 items-start gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:gap-24">
          
          {/* Left Column: Context & Contact */}
          <div className="lg:sticky lg:top-32">
            <p className="eyebrow">Free Case Review</p>
            <h2 className="h-section mt-4 text-white">
              Get your <span className="text-gold-sheen">free quote.</span>
            </h2>
            <p className="mt-5 text-[15px] leading-relaxed text-white/60 sm:max-w-md">
              Tell us what happened and upload your ticket. We'll review the charges and let you know exactly what your options are. No cost, no obligation.
            </p>
            
            <div className="mt-10 border-t border-white/10 pt-8 hidden lg:block">
              <p className="font-display text-lg uppercase tracking-wide text-white">Prefer to talk directly?</p>
              <a href={`tel:${PHONE_TEL}`} className="mt-3 inline-flex items-center gap-3 text-lg font-semibold text-gold transition-colors hover:text-gold-sheen">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-gold/10">
                  <svg viewBox="0 0 24 24" className="h-5 w-5" aria-hidden="true">
                    <path fill="currentColor" d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z" />
                  </svg>
                </span>
                {PHONE_DISPLAY}
              </a>
            </div>
          </div>

          {/* Right Column: The Form */}
          <div className="rounded-[2rem] border border-white/5 bg-ink-soft/40 p-6 sm:p-10 shadow-2xl backdrop-blur-sm">
            {status === "done" ? (
              <div className="flex h-full flex-col items-center justify-center text-center py-12">
                <div className="grid h-20 w-20 place-items-center rounded-full bg-gold/10 text-gold mb-6">
                  <svg viewBox="0 0 24 24" className="h-10 w-10" fill="none" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <p className="font-display text-4xl text-gold-sheen uppercase tracking-tight">Thank you.</p>
                <p className="mt-4 text-[15px] leading-relaxed text-white/70">
                  We've received your ticket details and will be in touch shortly to discuss your options.
                </p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} encType="multipart/form-data" className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <Field name="name" label="Full name" autoComplete="name" className="sm:col-span-2" />
                <Field name="phone" label="Phone" type="tel" autoComplete="tel" />
                <Field name="email" label="Email" type="email" autoComplete="email" />

                {/* Dropdown for Charge Type */}
                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="text-[11px] font-semibold uppercase tracking-widest text-white/50">Charge Type</span>
                  <div className="relative">
                    <select
                      name="charge"
                      required
                      className="w-full appearance-none rounded-xl border border-white/10 bg-white/[0.03] px-5 py-4 text-[15px] text-white outline-none transition focus:border-gold/50 focus:bg-white/[0.06]"
                      defaultValue=""
                    >
                      <option value="" disabled className="text-black">Select what you were charged with...</option>
                      <option value="Speeding" className="text-black">Speeding</option>
                      <option value="Stunt Driving" className="text-black">Stunt Driving</option>
                      <option value="Careless Driving" className="text-black">Careless Driving</option>
                      <option value="Distracted Driving" className="text-black">Distracted / Cell Phone</option>
                      <option value="Suspended Licence" className="text-black">Suspended Licence</option>
                      <option value="Fail to Remain" className="text-black">Fail to Remain / Stop</option>
                      <option value="Other" className="text-black">Other</option>
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-5 flex items-center text-white/40">
                      <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </div>
                </label>

                {/* Honeypot */}
                <input type="text" name="company" tabIndex={-1} autoComplete="off" aria-hidden="true" className="hidden" />

                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="flex items-baseline justify-between text-[11px] font-semibold uppercase tracking-widest text-white/50">
                    Upload your ticket <span className="text-white/30 normal-case tracking-normal font-normal">(optional)</span>
                  </span>
                  <input
                    name="ticket"
                    type="file"
                    accept="image/*,.pdf"
                    className="w-full rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3 text-sm text-white/80 outline-none transition file:mr-5 file:rounded-full file:border-0 file:bg-white/10 file:px-5 file:py-2.5 file:text-[11px] file:font-semibold file:uppercase file:tracking-wide file:text-white hover:file:bg-white/20 focus:border-gold/50 focus:bg-white/[0.06]"
                  />
                </label>

                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="flex items-baseline justify-between text-[11px] font-semibold uppercase tracking-widest text-white/50">
                    Brief message
                  </span>
                  <textarea
                    name="message"
                    rows={4}
                    required
                    placeholder="Tell us briefly what happened…"
                    className="resize-y w-full rounded-xl border border-white/10 bg-white/[0.03] px-5 py-4 text-[15px] text-white placeholder-white/30 outline-none transition focus:border-gold/50 focus:bg-white/[0.06]"
                  />
                </label>

                {status === "error" && (
                  <p className="rounded-xl border border-red-500/30 bg-red-500/10 px-5 py-4 text-[13px] text-red-200 sm:col-span-2">
                    {error}
                  </p>
                )}

                <div className="mt-4 flex flex-col gap-4 sm:col-span-2">
                  <button
                    type="submit"
                    disabled={status === "submitting"}
                    className="btn-sheen w-full inline-flex items-center justify-center rounded-xl bg-gold-sheen px-8 py-4 text-[14px] font-bold uppercase tracking-[0.15em] text-ink shadow-[0_8px_24px_rgba(231,172,64,0.25)] transition hover:-translate-y-0.5 disabled:opacity-60"
                  >
                    {status === "submitting" ? "Sending…" : "Get My Free Quote"}
                  </button>
                  <p className="text-center text-[11px] leading-relaxed text-white/40">
                    By submitting, you agree to be contacted about your case. All information is confidential.
                  </p>
                </div>
              </form>
            )}
          </div>
          
          {/* Mobile phone block (bottom) */}
          <div className="mt-4 border-t border-white/10 pt-8 lg:hidden text-center">
            <p className="text-xs uppercase tracking-widest text-white/50">Prefer to talk directly?</p>
            <a href={`tel:${PHONE_TEL}`} className="mt-2 inline-flex items-center gap-2 text-lg font-semibold text-gold">
              <svg viewBox="0 0 24 24" className="h-4 w-4" fill="currentColor">
                <path d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z" />
              </svg>
              {PHONE_DISPLAY}
            </a>
          </div>

        </div>
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
    <label className={`flex flex-col gap-2 ${className}`}>
      <span className="text-[11px] font-semibold uppercase tracking-widest text-white/50">{label}</span>
      <input
        name={name}
        type={type}
        required
        autoComplete={autoComplete}
        className="w-full rounded-xl border border-white/10 bg-white/[0.03] px-5 py-4 text-[15px] text-white placeholder-white/30 outline-none transition focus:border-gold/50 focus:bg-white/[0.06]"
      />
    </label>
  );
}
