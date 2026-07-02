"use client";

import { useState } from "react";
import { CHARGE_OPTIONS, PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";
import { submitLead } from "@/lib/lead-client";

type Status = "idle" | "submitting" | "error";

// Compact 2-step lead form directly under the hero, so a paid-click visitor can
// convert without scrolling the whole page. Step 1 asks only what Leslie needs
// to call back (charge + phone); step 2 adds the name (+ optional email).
// Posts to the same /api/lead as the bottom QuoteForm and fires the same
// Google Ads conversion. The SKAG pages pass `defaultCharge` so the dropdown
// arrives pre-selected with the offence the visitor searched for.
export default function QuickForm({ defaultCharge = "" }: { defaultCharge?: string }) {
  const [step, setStep] = useState<1 | 2>(1);
  const [done, setDone] = useState(false);
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");
  const [charge, setCharge] = useState(defaultCharge);
  const [phone, setPhone] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const input =
    "w-full rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3.5 text-[15px] text-white placeholder-white/40 outline-none transition focus:border-gold/50 focus:bg-white/[0.06]";
  const button =
    "btn-sheen inline-flex items-center justify-center whitespace-nowrap rounded-xl bg-gold-sheen px-6 py-3.5 text-[13px] font-bold uppercase tracking-[0.12em] text-ink shadow-[0_8px_24px_rgba(231,172,64,0.2)] transition hover:-translate-y-0.5 disabled:opacity-60";

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("submitting");
    setError("");

    const fd = new FormData(e.currentTarget);
    fd.set("charge", charge);
    fd.set("phone", phone);

    try {
      await submitLead(fd);
      setDone(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please call us.");
      setStatus("error");
    }
  }

  const chargeLabel = CHARGE_OPTIONS.find((o) => o.value === charge)?.label || charge;

  return (
    <section id="free-review" className="scroll-mt-6 border-y border-gold/20 bg-ink-soft/60">
      <div className="section grid items-center gap-7 py-10 sm:py-12 lg:grid-cols-[0.85fr_1.15fr] lg:gap-14">
        {/* Left — the promise */}
        <div>
          <p className="eyebrow">Free Case Review</p>
          <h2 className="mt-3 font-display text-3xl uppercase leading-none tracking-tight text-white sm:text-4xl">
            Check your ticket <span className="text-gold-sheen">in 30 seconds.</span>
          </h2>
          <p className="mt-3 max-w-md text-sm leading-relaxed text-white/60">
            Tell us the charge and your number — we&apos;ll review your options and call you back.
            Free, confidential, no obligation.
          </p>
        </div>

        {/* Right — the 2-step form */}
        {done ? (
          <div className="flex items-center gap-4 rounded-2xl border border-gold/30 bg-ink/60 p-6">
            <span className="grid h-12 w-12 shrink-0 place-items-center rounded-full bg-gold/10 text-gold">
              <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </span>
            <div>
              <p className="font-display text-xl uppercase tracking-tight text-gold-sheen">Thank you.</p>
              <p className="mt-1 text-[13.5px] leading-relaxed text-white/70">
                We&apos;ll call you shortly at {phone}. Want to talk now?{" "}
                <a href={`tel:${PHONE_TEL}`} className="font-semibold text-gold hover:text-gold-sheen">
                  Call {PHONE_DISPLAY}
                </a>
              </p>
            </div>
          </div>
        ) : step === 1 ? (
          /* key forces a remount when the step flips — without it React reuses
             the step-1 phone <input> DOM node for step-2's email field (same
             position + type), leaking the typed phone number into it. */
          <form
            key="quick-step-1"
            onSubmit={(e) => {
              e.preventDefault();
              setStep(2);
            }}
            className="grid gap-3 sm:grid-cols-[1.15fr_1fr_auto]"
          >
            <div className="relative">
              <select
                required
                value={charge}
                onChange={(e) => setCharge(e.target.value)}
                aria-label="What were you charged with?"
                className={`${input} appearance-none pr-10`}
              >
                <option value="" disabled className="text-black">
                  What were you charged with?
                </option>
                {CHARGE_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value} className="text-black">
                    {o.label}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-4 flex items-center text-white/40">
                <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                </svg>
              </div>
            </div>
            <input
              type="tel"
              required
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="Phone number"
              aria-label="Phone number"
              autoComplete="tel"
              inputMode="tel"
              pattern="[0-9()+\-.\s]{7,}"
              title="Please enter a valid phone number"
              className={input}
            />
            <button type="submit" className={button}>
              Continue
            </button>
            <p className="text-[11px] leading-relaxed text-white/40 sm:col-span-3">
              Step 1 of 2 — free &amp; confidential. Prefer to talk?{" "}
              <a href={`tel:${PHONE_TEL}`} className="font-semibold text-gold/80 hover:text-gold">
                Call {PHONE_DISPLAY}
              </a>
            </p>
          </form>
        ) : (
          <form key="quick-step-2" onSubmit={handleSubmit} className="grid gap-3 sm:grid-cols-[1fr_1fr_auto]">
            <input
              name="name"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Full name"
              aria-label="Full name"
              autoComplete="name"
              className={input}
            />
            <input
              name="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email (optional)"
              aria-label="Email (optional)"
              autoComplete="email"
              className={input}
            />
            {/* Honeypot: real users never fill "company". */}
            <input type="text" name="company" tabIndex={-1} autoComplete="off" aria-hidden="true" className="hidden" />
            <button type="submit" disabled={status === "submitting"} className={button}>
              {status === "submitting" ? "Sending…" : "Get My Review"}
            </button>
            {status === "error" && (
              <p className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-[13px] text-red-200 sm:col-span-3">
                {error}
              </p>
            )}
            <p className="text-[11px] leading-relaxed text-white/40 sm:col-span-3">
              Almost done — {chargeLabel} · {phone}{" "}
              <button
                type="button"
                onClick={() => setStep(1)}
                className="font-semibold text-gold/80 underline underline-offset-2 hover:text-gold"
              >
                Edit
              </button>
            </p>
          </form>
        )}
      </div>
    </section>
  );
}
