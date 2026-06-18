"use client";

import { useState } from "react";
import { PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";

type Status = "idle" | "submitting" | "done";

// Bottom-of-page quote form: first name, last name, email, phone.
// Submits to a placeholder handler — wire to Netlify Forms / an API route later.
export default function QuoteForm() {
  const [status, setStatus] = useState<Status>("idle");

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    console.log("[QuoteForm] submit start");
    setStatus("submitting");
    const data = Object.fromEntries(new FormData(e.currentTarget).entries());
    // Placeholder: replace with a real POST (Netlify Forms / API route).
    console.log("[QuoteForm] captured lead", data);
    setTimeout(() => {
      setStatus("done");
      console.log("[QuoteForm] submit done");
    }, 600);
  }

  return (
    <section id="quote" className="relative scroll-mt-6 overflow-hidden bg-ink py-16 text-white sm:py-24">
      <div className="pointer-events-none absolute -left-40 bottom-0 h-[28rem] w-[28rem] rounded-full bg-gold/10 blur-[120px]" />
      <div className="section relative max-w-2xl">
        <div className="text-center">
          <p className="eyebrow justify-center">Free Case Review</p>
          <h2 className="display mt-4 text-4xl text-white sm:text-5xl">
            Get your <span className="text-gold-sheen">free quote.</span>
          </h2>
          <p className="mt-4 text-sm text-white/70">
            Tell us where to reach you and we&apos;ll review your ticket with no obligation.
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
          <form onSubmit={handleSubmit} className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field name="firstName" label="First name" autoComplete="given-name" />
            <Field name="lastName" label="Last name" autoComplete="family-name" />
            <Field name="email" label="Email" type="email" autoComplete="email" className="sm:col-span-2" />
            <Field name="phone" label="Phone" type="tel" autoComplete="tel" className="sm:col-span-2" />

            <button
              type="submit"
              disabled={status === "submitting"}
              className="mt-2 inline-flex items-center justify-center gap-3 rounded-none bg-gold-sheen px-10 py-[18px] text-[12px] font-semibold uppercase tracking-[0.22em] text-ink transition hover:brightness-[1.04] disabled:opacity-60 sm:col-span-2"
            >
              {status === "submitting" ? "Sending…" : "Get My Free Quote"}
            </button>

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
