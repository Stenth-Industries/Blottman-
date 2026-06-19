"use client";

import Image from "next/image";
import { motion, useReducedMotion, type Variants } from "motion/react";
import CtaButton from "./CtaButton";
import { BENEFITS, PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";

// Staggered entrance: each child rises + fades in sequence.
const container: Variants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.12, delayChildren: 0.08 } },
};
const item: Variants = {
  hidden: { opacity: 0, y: 18 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] } },
};

// Dark, bold hero. No site header/nav — this is a focused conversion page.
export default function Hero() {
  const reduce = useReducedMotion();

  return (
    <section className="relative overflow-hidden bg-ink text-white">
      {/* Ontario courthouse atmosphere — slightly blurred so it reads as background, not focus */}
      <Image
        src="/courthouse-bg.png"
        alt=""
        aria-hidden="true"
        fill
        priority
        sizes="100vw"
        className="pointer-events-none object-cover object-center blur-[1px]"
      />
      {/* left-to-right darkening: left very dark for the headline, right darkened ~30% behind Leslie */}
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-r from-ink/90 via-ink/72 to-ink/65" />
      {/* soft black halo behind Leslie's portrait so it blends into the hero */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_78%_55%,rgba(12,12,12,0.65),transparent_55%)]" />
      {/* warm gold light — reduced so it doesn't overpower */}
      <div className="pointer-events-none absolute -right-40 -top-40 h-[28rem] w-[28rem] rounded-full bg-gold/8 blur-[130px]" />
      <div className="section relative z-10 grid items-center gap-12 py-16 sm:py-24 lg:grid-cols-[1.15fr_0.85fr]">
        <motion.div
          className="lg:-ml-16 xl:-ml-28"
          variants={container}
          initial={reduce ? false : "hidden"}
          animate="show"
        >
          <motion.div variants={item}>
            <Image
              src="/logo.png"
              alt="Blottman Legal Services"
              width={1957}
              height={1800}
              priority
              className="mb-6 h-auto w-[120px] sm:w-[120px]"
            />
          </motion.div>
          <motion.p variants={item} className="text-lg font-semibold uppercase tracking-[0.18em] text-gold">
            Ontario Traffic-Ticket Defence
          </motion.p>
          <motion.h1 variants={item} className="display mt-5 text-5xl sm:text-7xl">
            Fight your ticket.
            <br />
            Protect your <span className="text-gold-sheen">record.</span>
          </motion.h1>

          <motion.ul variants={item} className="mt-8 grid gap-3 sm:grid-cols-2">
            {BENEFITS.map((b) => (
              <li key={b} className="flex items-start gap-2.5 text-[15px] text-white/85">
                <Check />
                <span>{b}</span>
              </li>
            ))}
          </motion.ul>

          <motion.div variants={item} className="mt-9 flex flex-col items-start gap-4 sm:flex-row sm:items-center">
            <CtaButton href="#quote">Get a Free Case Review</CtaButton>
            <a
              href={`tel:${PHONE_TEL}`}
              className="inline-flex items-center gap-2.5 text-sm font-semibold text-white hover:text-gold"
            >
              <span className="grid h-10 w-10 place-items-center rounded-full border border-gold/40 text-gold">
                <Phone />
              </span>
              <span className="leading-tight">
                <span className="block text-[11px] uppercase tracking-[0.18em] text-gold/80">Call for a free review</span>
                {PHONE_DISPLAY}
              </span>
            </a>
          </motion.div>
        </motion.div>

        {/* Leslie — real, unedited photo blended into the hero with CSS only */}
        <motion.div
          className="relative ml-auto hidden w-full max-w-[330px] lg:block"
          initial={reduce ? false : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
        >
          {/* Portrait card + name badge — own positioning context so the badge anchors to the card, not the whole column */}
          <div className="relative">
            {/* warm gold glow + soft shadow around the card so it sits in the black-and-gold hero */}
            <div className="absolute -inset-4 rounded-[2.25rem] bg-gold/15 blur-3xl" />
            <div className="relative aspect-[4/5] overflow-hidden rounded-[2rem] border border-[rgba(232,176,65,0.22)] bg-ink-soft shadow-[0_35px_90px_-30px_rgba(0,0,0,0.85)] ring-1 ring-inset ring-white/[0.07]">
              <Image
                src="/leslie-office.png"
                alt="Leslie Rivas — licensed Ontario paralegal, Blottman Law"
                fill
                priority
                sizes="(max-width: 1024px) 100vw, 40vw"
                className="object-cover object-top brightness-95"
              />
              {/* soft black gradient — softer at the bottom so it isn't too heavy, easing to clear over her face */}
              <div className="pointer-events-none absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-ink/65 via-ink/20 to-transparent" />
              {/* gentle top fade */}
              <div className="pointer-events-none absolute inset-x-0 top-0 h-1/5 bg-gradient-to-b from-ink/40 to-transparent" />
              {/* edge vignette — darkens the corners/edges, keeps the centre (face) clear */}
              <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_50%_38%,transparent_46%,rgba(12,12,12,0.62))]" />
            </div>
            <div className="absolute -bottom-5 -left-5 rounded-2xl border border-gold/20 bg-ink/90 px-5 py-3.5 shadow-[0_18px_44px_-14px_rgba(0,0,0,0.9)] ring-1 ring-inset ring-white/[0.08] backdrop-blur-sm">
              <p className="font-display text-xl uppercase tracking-tight text-gold">Leslie Rivas</p>
              <p className="mt-0.5 text-[11px] uppercase tracking-[0.18em] text-white/60">Licensed Ontario Paralegal</p>
            </div>
          </div>

          {/* Personal quote from Leslie, beneath her portrait (clears the overhanging name badge) */}
          <figure className="mt-10 border-l-2 border-gold/50 pl-5">
            <blockquote className="text-[13.5px] italic leading-relaxed text-white/75">
              &ldquo;Many drivers underestimate the long-term consequences of a traffic ticket.
              It can affect your insurance, your driving record, and your future. Before you pay
              a ticket or let a deadline pass, take the time to understand your rights and the
              options available to you.&rdquo;
            </blockquote>
            <figcaption className="mt-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-gold">
              &mdash; Leslie Rivas
            </figcaption>
          </figure>
        </motion.div>
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
