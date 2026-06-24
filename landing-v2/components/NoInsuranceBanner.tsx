"use client";

import Link from "next/link";
import { m, useReducedMotion } from "motion/react";
import { PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";

// What's actually at stake on a "drive with no insurance" charge in Ontario.
// Source: Compulsory Automobile Insurance Act, R.S.O. 1990, c. C.25, s. 2 — public
// statute, factual (NOT a results claim), so no LSO marketing-rule concern.
const STAKES: { top: React.ReactNode; bottom: React.ReactNode; body: string; icon: "fine" | "suspend" | "impound" }[] = [
  {
    top: <span className="font-display text-[2.5rem] uppercase leading-none tracking-tight text-gold-sheen">Up to $25,000</span>,
    bottom: <span className="font-sans text-[13px] font-semibold uppercase tracking-[0.15em] text-white">In Fines</span>,
    body: "First offence runs $5,000–$25,000, plus a 25% surcharge. A second conviction can reach $50,000.",
    icon: "fine",
  },
  {
    top: <span className="font-sans text-[13px] font-semibold uppercase tracking-[0.15em] text-white">Licence Suspension</span>,
    bottom: <span className="font-display text-[2.5rem] uppercase leading-none tracking-tight text-gold-sheen">Up to 1 Year</span>,
    body: "Your driver's licence can be suspended on conviction — putting your job and daily life at risk.",
    icon: "suspend",
  },
  {
    top: <span className="font-sans text-[13px] font-semibold uppercase tracking-[0.15em] text-white">Vehicle Impoundment</span>,
    bottom: <span className="font-display text-[2.5rem] uppercase leading-none tracking-tight text-gold-sheen">Plates Seized</span>,
    body: "Your vehicle's licence plates can be impounded, leaving you without a legal way to drive.",
    icon: "impound",
  },
];

// Dark "before you pay your ticket" banner — driving-with-no-insurance intent.
// Sits after the Expertise grid. Black + gold theme, mirrors the site's section styling.
export default function NoInsuranceBanner() {
  const reduce = useReducedMotion();

  return (
    <section className="relative overflow-hidden bg-ink py-16 text-white sm:py-24">
      {/* Background Image with seamless top/bottom fades and vignette */}
      <div className="pointer-events-none absolute inset-0">
        <img
          src="/abstract_siren_bg.png"
          alt=""
          aria-hidden="true"
          className="h-full w-full object-cover object-center opacity-25 brightness-75 mix-blend-lighten"
        />
        {/* Soft edge vignette to focus the center and darken the edges heavily */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_20%,rgba(12,12,12,0.95)_100%)]" />
        {/* Fade into the background color at top and bottom */}
        <div className="absolute inset-x-0 top-0 h-32 bg-gradient-to-b from-ink via-ink/80 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-ink via-ink/90 to-transparent" />
      </div>

      {/* Off-axis background document (ticket) to create massive depth */}
      <div
        className="pointer-events-none absolute right-0 top-1/2 w-[800px] -translate-y-1/2 translate-x-[65%] rotate-12 opacity-5 mix-blend-luminosity"
        aria-hidden="true"
      >
        <img
          src="/process-1-ticket.jpg"
          alt=""
          className="h-auto w-full rounded-3xl"
        />
      </div>

      {/* Large vertical typography (Luxury fashion style) */}
      <div
        className="pointer-events-none absolute -left-48 top-1/2 flex -translate-y-1/2 -rotate-90 select-none items-center whitespace-nowrap opacity-[0.02]"
        aria-hidden="true"
      >
        <span className="display text-[clamp(8rem,20vw,16rem)] text-white">
          Ontario No Insurance Defence
        </span>
      </div>

      <div className="section relative z-10 max-w-5xl text-center">
        <p className="eyebrow justify-center">Driving With No Insurance</p>
        <h2 className="h-section mt-4">
          Charged With Driving With No Insurance in{" "}
          <span className="text-gold-sheen">Ontario?</span>
        </h2>
        <p className="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-white/70">
          Under Ontario&apos;s Compulsory Automobile Insurance Act the penalties are severe — and they
          escalate fast. Before you pay your ticket, understand what&apos;s actually at stake.
        </p>

        {/* What's at stake — factual statutory penalties, mirrors the Expertise card grid */}
        <div className="mt-14 grid grid-cols-1 gap-5 text-left sm:grid-cols-3">
          {STAKES.map((s, i) => (
            <m.div
              key={s.icon}
              initial={reduce ? false : { opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] }}
            >
              <div className="card h-full bg-ink/40 p-8 ring-1 ring-inset ring-white/5 backdrop-blur-xl transition-all duration-300 hover:-translate-y-1.5 hover:bg-ink/60 hover:ring-white/10 hover:shadow-[0_12px_32px_rgba(255,255,255,0.04)]">
                <span className="mb-6 grid h-12 w-12 place-items-center rounded-xl border border-gold/30 bg-ink-soft/50 text-gold shadow-inner">
                  <StakeIcon name={s.icon} />
                </span>
                <div className="flex flex-col gap-1">
                  {s.top}
                  {s.bottom}
                </div>
                <p className="mt-4 text-[13.5px] leading-relaxed text-white/85">{s.body}</p>
              </div>
            </m.div>
          ))}
        </div>

        <p className="mx-auto mt-10 max-w-2xl text-base leading-relaxed text-white/70">
          Blottman Legal Services works to reduce the charge, lower the fine, and protect your
          licence. Speak with us before paying — once you pay, you&apos;ve pleaded guilty.
        </p>

        <div className="mx-auto mt-12 flex w-full max-w-3xl flex-col items-center justify-between gap-6 rounded-2xl bg-ink/40 p-6 shadow-2xl ring-1 ring-inset ring-white/10 backdrop-blur-xl sm:flex-row sm:p-8">
          <a
            href={`tel:${PHONE_TEL}`}
            className="group flex w-full items-center justify-center gap-4 text-left sm:w-auto sm:justify-start"
          >
            <span className="grid h-12 w-12 shrink-0 place-items-center rounded-full border border-white/20 bg-white/5 text-white transition-colors group-hover:border-white/30 group-hover:bg-white/10">
              <svg viewBox="0 0 24 24" className="h-5 w-5" aria-hidden="true">
                <path
                  fill="currentColor"
                  d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z"
                />
              </svg>
            </span>
            <div>
              <span className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-white/50">Call for a free review</span>
              <span className="text-lg font-medium text-white underline decoration-white/30 decoration-2 underline-offset-4 transition-colors group-hover:decoration-white">{PHONE_DISPLAY}</span>
            </div>
          </a>

          <div className="hidden h-12 w-px bg-white/10 sm:block"></div>

          <Link
            href="#quote"
            className="btn-sheen inline-flex w-full items-center justify-center rounded-xl bg-gold-sheen px-8 py-4 text-[13px] font-semibold uppercase tracking-[0.12em] text-ink transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_8px_24px_rgba(231,172,64,0.35)] focus:outline-none focus:ring-2 focus:ring-gold/60 sm:w-auto"
          >
            Speak With Blottman Legal
          </Link>
        </div>
      </div>
    </section>
  );
}

// Icons from Lucide (lucide.dev, ISC license) — inlined as paths so there's no
// runtime dependency or bundle cost.
function StakeIcon({ name }: { name: "fine" | "suspend" | "impound" }) {
  const common = {
    viewBox: "0 0 24 24",
    className: "h-[22px] w-[22px]",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 2,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true as const,
  };
  if (name === "fine") {
    // Lucide "circle-dollar-sign"
    return (
      <svg {...common}>
        <circle cx="12" cy="12" r="10" />
        <path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8" />
        <path d="M12 18V6" />
      </svg>
    );
  }
  if (name === "suspend") {
    // Lucide "id-card" (the driver's licence)
    return (
      <svg {...common}>
        <path d="M16 10h2" />
        <path d="M16 14h2" />
        <path d="M6.17 15a3 3 0 0 1 5.66 0" />
        <circle cx="9" cy="11" r="2" />
        <rect x="2" y="5" width="20" height="14" rx="2" />
      </svg>
    );
  }
  // Lucide "car"
  return (
    <svg {...common}>
      <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2" />
      <circle cx="7" cy="17" r="2" />
      <path d="M9 17h6" />
      <circle cx="17" cy="17" r="2" />
    </svg>
  );
}
