"use client";

import { useState } from "react";
import { CHARGE_OPTIONS, PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";
import { submitLead } from "@/lib/lead-client";

type Status = "idle" | "submitting" | "done" | "error";

// Bottom-of-page quote form. Posts to /api/lead, which emails Leslie + logs the
// lead to the Google Sheet. Captures the gclid (for later offline-conversion
// import) and uses a honeypot field for spam.
export default function QuoteForm() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("submitting");
    setError("");

    try {
      await submitLead(new FormData(e.currentTarget));
      setStatus("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please call us.");
      setStatus("error");
    }
  }

  return (
    <section id="quote" className="relative scroll-mt-6 overflow-hidden bg-ink border-t border-ink-line py-16 text-white sm:py-32">
      {/* Background glow — smooth, even radial gradient */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_30%_80%,rgba(231,172,64,0.06)_0%,transparent_60%)]" />
      
      <div className="section relative">
        <div className="grid grid-cols-1 items-start gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:gap-24">
          
          {/* Left Column: Context & Contact */}
          <div className="lg:sticky lg:top-32">
            <p className="eyebrow">Free Case Review</p>
            <h2 className="h-section mt-4 text-white">
              Get your <span className="text-gold-sheen">free quote.</span>
            </h2>
            <p className="mt-5 text-[15px] leading-relaxed text-white/60 sm:max-w-md">
              Tell us what happened and we'll review your charge and let you know exactly what your options are. No cost, no obligation.
            </p>
            
            <div className="mt-10 border-t border-white/10 pt-8 hidden lg:block">
              <p className="font-display text-lg uppercase tracking-wide text-white">Prefer to talk directly?</p>
              <a href={`tel:${PHONE_TEL}`} className="mt-3 inline-flex items-center gap-3 text-lg font-semibold text-gold transition-colors hover:text-gold-sheen">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full border border-gold/40 text-gold transition-colors hover:bg-gold/10">
                  <svg viewBox="0 0 24 24" className="h-4 w-4" fill="currentColor">
                    <path d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z" />
                  </svg>
                </span>
                {PHONE_DISPLAY}
              </a>
              
              {/* Trust Indicators to fill empty space strategically */}
              <div className="mt-8 space-y-4 border-t border-white/5 pt-8">
                <div className="flex items-start gap-3 text-[13px] text-white/70">
                  <svg viewBox="0 0 24 24" className="mt-px h-4 w-4 shrink-0 text-gold/80" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
                  Average response time under 2 hours
                </div>
                <div className="flex items-start gap-3 text-[13px] text-white/70">
                  <svg viewBox="0 0 24 24" className="mt-px h-4 w-4 shrink-0 text-gold/80" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
                  </svg>
                  Reviewed by a licensed Ontario paralegal
                </div>
                <div className="flex items-start gap-3 text-[13px] text-white/70">
                  <svg viewBox="0 0 24 24" className="mt-px h-4 w-4 shrink-0 text-gold/80" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                  </svg>
                  Your information is completely confidential
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: The Form */}
          <div className="rounded-[2rem] border border-white/5 bg-white/[0.02] p-6 sm:p-10 shadow-2xl backdrop-blur-sm">
            {status === "done" ? (
              <div className="flex h-full flex-col items-center justify-center text-center py-12 text-white">
                <div className="grid h-20 w-20 place-items-center rounded-full bg-gold/10 text-gold mb-6">
                  <svg viewBox="0 0 24 24" className="h-10 w-10" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <p className="font-display text-4xl text-gold-sheen uppercase tracking-tight">Thank you.</p>
                <p className="mt-4 text-[15px] leading-relaxed text-white/70">
                  We've received your message and will be in touch shortly to discuss your options.
                </p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} encType="multipart/form-data" className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <Field name="name" label="Full name" autoComplete="name" className="sm:col-span-2" />
                <Field name="phone" label="Phone" type="tel" autoComplete="tel" />
                <Field name="email" label="Email (optional)" type="email" autoComplete="email" required={false} />

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
                      {CHARGE_OPTIONS.map((o) => (
                        <option key={o.value} value={o.value} className="text-black">{o.label}</option>
                      ))}
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-5 flex items-center text-white/40">
                      <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                      </svg>
                    </div>
                  </div>
                </label>

                {/* Honeypot */}
                <input type="text" name="company" tabIndex={-1} autoComplete="off" aria-hidden="true" className="hidden" />

                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="text-[11px] font-semibold uppercase tracking-widest text-white/50">
                    What happened? (optional)
                  </span>
                  <textarea
                    name="message"
                    rows={4}
                    placeholder="e.g., I was pulled over on the 401. The officer said I was doing 130km/h. This is my first ticket."
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
              <span className="grid h-8 w-8 place-items-center rounded-full border border-gold/40 text-gold">
                <svg viewBox="0 0 24 24" className="h-3 w-3" fill="currentColor">
                  <path d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z" />
                </svg>
              </span>
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
  required = true,
}: {
  name: string;
  label: string;
  type?: string;
  autoComplete?: string;
  className?: string;
  required?: boolean;
}) {
  return (
    <label className={`flex flex-col gap-2 ${className}`}>
      <span className="text-[11px] font-semibold uppercase tracking-widest text-white/50">{label}</span>
      <input
        name={name}
        type={type}
        required={required}
        autoComplete={autoComplete}
        className="w-full rounded-xl border border-white/10 bg-white/[0.03] px-5 py-4 text-[15px] text-white placeholder-white/30 outline-none transition focus:border-gold/50 focus:bg-white/[0.06]"
      />
    </label>
  );
}
