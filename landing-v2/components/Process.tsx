"use client";

import { motion, useReducedMotion, type Variants } from "motion/react";
import CtaButton from "./CtaButton";
import {
  PROCESS,
  PROCESS_SUBHEADING,
  TICKET_REVIEW,
  PHONE_TEL,
} from "@/lib/content";

const container: Variants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1, delayChildren: 0.05 } },
};
const item: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] } },
};

// "Send your ticket. Know your options." — a conversion bridge, not a generic
// 4-step list. Built mobile-first for stressed Google Ads traffic:
//   • mobile  -> conversion card FIRST, then a compact 3-step timeline.
//   • desktop -> two columns: steps on the left, conversion card on the right.
// Card uses a dark gradient/texture placeholder for now; a generated image
// (phone photographing a ticket) drops into that slot later.
export default function Process() {
  const reduce = useReducedMotion();

  return (
    <section className="bg-paper py-16 sm:py-24">
      <div className="section">
        <motion.div
          className="max-w-2xl"
          initial={reduce ? false : { opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
          <p className="eyebrow">How It Works</p>
          <h2 className="h-section mt-4 text-[1.95rem] leading-[1.02] sm:text-5xl">
            Send your ticket.
            <br />
            <span className="text-gold-sheen">Know your options.</span>
          </h2>
          <p className="mt-4 max-w-md text-[15px] leading-relaxed text-ink-muted sm:max-w-xl sm:text-lg">
            {PROCESS_SUBHEADING}
          </p>
        </motion.div>

        {/* Card is order-1 on mobile (first thing after the heading) and moves
            to the right column on desktop. Steps fill the left column. */}
        <div className="mt-12 grid grid-cols-1 gap-8 lg:grid-cols-2 lg:items-start lg:gap-12">
          {/* --------------------------- 3 STEPS --------------------------- */}
          <motion.ol
            className="relative order-2 lg:order-1 lg:mt-2"
            variants={container}
            initial={reduce ? false : "hidden"}
            whileInView="show"
            viewport={{ once: true, margin: "-80px" }}
          >
            {PROCESS.map((p, i) => {
              const isLast = i === PROCESS.length - 1;
              return (
                <motion.li
                  key={p.step}
                  variants={item}
                  className="relative flex items-start gap-4 pb-6 last:pb-0"
                >
                  {!isLast && (
                    <span
                      aria-hidden="true"
                      className="pointer-events-none absolute left-5 top-10 h-[calc(100%-2.5rem)] w-px bg-gradient-to-b from-gold/35 to-gold/10"
                    />
                  )}
                  <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-gold/40 bg-ink shadow-[0_6px_20px_-8px_rgba(12,12,12,0.5)]">
                    <span className="font-display text-base text-gold">{p.step}</span>
                  </div>
                  <div className="pt-1">
                    <h3 className="font-display text-base uppercase tracking-tight text-ink sm:text-lg">
                      {p.title}
                    </h3>
                    <p className="mt-1 text-sm leading-relaxed text-ink-muted">
                      {p.body}
                    </p>
                  </div>
                </motion.li>
              );
            })}
          </motion.ol>

          {/* ----------------------- CONVERSION CARD ----------------------- */}
          <motion.div
            className="order-1 lg:order-2"
            initial={reduce ? false : { opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          >
            {/* warm gold glow so the dark card sits in the ivory section */}
            <div className="relative">
              <div className="pointer-events-none absolute -inset-2 rounded-[2rem] bg-gold/10 blur-2xl" />
              <div className="relative overflow-hidden rounded-3xl border border-gold/20 bg-ink text-white shadow-[0_30px_70px_-30px_rgba(12,12,12,0.7)] ring-1 ring-inset ring-white/[0.06]">
                {/* IMAGE PLACEHOLDER — desktop only, kept off mobile to stay fast.
                    Replace this block with the generated ticket-photo image. */}
                <div className="relative hidden aspect-[16/7] w-full items-end overflow-hidden bg-ink-soft lg:flex">
                  {/* neutral gradient + faint texture stand-in */}
                  <div className="absolute inset-0 bg-[radial-gradient(ellipse_120%_120%_at_70%_0%,rgba(231,172,64,0.16),transparent_55%)]" />
                  <div className="absolute inset-0 bg-gradient-to-t from-ink via-ink/70 to-transparent" />
                  <div className="absolute inset-0 bg-[linear-gradient(135deg,rgba(255,255,255,0.04)_25%,transparent_25%,transparent_50%,rgba(255,255,255,0.04)_50%,rgba(255,255,255,0.04)_75%,transparent_75%)] bg-[length:14px_14px] opacity-30" />
                  <span className="relative z-10 m-4 text-[10px] uppercase tracking-[0.22em] text-white/30">
                    Image coming soon
                  </span>
                </div>

                <div className="p-5 sm:p-7">
                  <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">
                    {TICKET_REVIEW.title}
                  </p>
                  <p className="mt-2.5 text-[15px] leading-relaxed text-white/80">
                    {TICKET_REVIEW.copy}
                  </p>

                  <ul className="mt-5 space-y-2.5">
                    {TICKET_REVIEW.points.map((pt) => (
                      <li key={pt} className="flex items-start gap-3 text-sm text-white/85">
                        <Check />
                        <span>{pt}</span>
                      </li>
                    ))}
                  </ul>

                  <div className="mt-6 flex flex-col gap-3">
                    <CtaButton href="#quote" className="w-full">
                      {TICKET_REVIEW.primaryCta}
                    </CtaButton>
                    <CtaButton href={`tel:${PHONE_TEL}`} variant="ghost" arrow={false} className="w-full">
                      <Phone />
                      {TICKET_REVIEW.secondaryCta}
                    </CtaButton>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

function Check() {
  return (
    <svg viewBox="0 0 24 24" className="mt-0.5 h-5 w-5 shrink-0 text-gold" aria-hidden="true">
      <path
        fill="none"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M5 13l4 4L19 7"
      />
    </svg>
  );
}

function Phone() {
  return (
    <svg viewBox="0 0 24 24" className="h-4 w-4" aria-hidden="true">
      <path
        fill="currentColor"
        d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z"
      />
    </svg>
  );
}
