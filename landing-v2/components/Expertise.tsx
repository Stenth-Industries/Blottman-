"use client";

import Image from "next/image";
import Link from "next/link";
import { m, useReducedMotion, type Variants } from "motion/react";
import SectionCta from "./SectionCta";
import { EXPERTISE } from "@/lib/content";

const container: Variants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08, delayChildren: 0.05 } },
};
const item: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] } },
};
// Numbers pop in (scale + fade) within each card's reveal.
const numberItem: Variants = {
  hidden: { opacity: 0, scale: 0.5 },
  show: { opacity: 1, scale: 1, transition: { duration: 0.45, ease: [0.22, 1, 0.36, 1] } },
};

// Numbered practice-area grid — Garde Wilson "Expertise" pattern, on black.
export default function Expertise() {
  const reduce = useReducedMotion();

  return (
    <section className="relative overflow-hidden bg-ink py-16 text-white sm:py-24">
      {/* full-section background — kept very faint behind everything (not inside the cards) */}
      {/* Faint (0.67 opacity), below-fold decorative backdrop — low quality is
          invisible here but saves ~50 KiB off the 84 KiB default. */}
      <Image
        src="/what-we-fight-bg-3.webp"
        alt=""
        aria-hidden="true"
        fill
        sizes="100vw"
        quality={45}
        className="pointer-events-none object-cover opacity-[0.67]"
      />
      {/* horizontal overlay: near-black through the centre behind the grid, lighter at the edges so the road shows only there */}
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-r from-ink/35 via-ink to-ink/35" />
      {/* stronger centre darkening behind the offence grid so the cards sit on clean near-black */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_72%_92%_at_center,rgba(12,12,12,0.82),transparent_72%)]" />
      {/* warm gold glow on the far left and far right edges (slightly reduced) */}
      <div className="pointer-events-none absolute -left-44 top-1/2 h-[30rem] w-[30rem] -translate-y-1/2 rounded-full bg-gold/8 blur-[140px]" />
      <div className="pointer-events-none absolute -right-44 top-1/2 h-[30rem] w-[30rem] -translate-y-1/2 rounded-full bg-gold/8 blur-[140px]" />
      <div className="section relative z-10">
        <m.div
          className="max-w-2xl"
          initial={reduce ? false : { opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
          <p className="eyebrow">What We Fight</p>
          <h2 className="h-section mt-4 text-white">
            Every ticket has a <span className="text-gold-sheen">defence.</span>
          </h2>
          {/* Mobile swipe hint */}
          <div className="mt-6 flex items-center gap-2 text-gold/60 sm:hidden">
            <svg className="h-5 w-5 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
            <span className="font-sans text-xs uppercase tracking-widest">Swipe to explore</span>
          </div>
        </m.div>

        {/* Full-width image tiles — uses the snapshot photos and spreads the 9
            charges horizontally (3 across) instead of one tall text column. */}
        <m.div
          className="mt-12 grid auto-cols-[85%] grid-flow-col snap-x snap-mandatory overflow-x-auto pb-8 sm:auto-cols-auto sm:grid-flow-row sm:grid-cols-2 sm:overflow-visible sm:pb-0 lg:grid-cols-3 gap-4"
          variants={container}
          initial={reduce ? false : "hidden"}
          whileInView="show"
          viewport={{ once: true, margin: "-80px" }}
        >
          {EXPERTISE.map((card, i) => (
            <m.div
              key={card.title}
              variants={item}
              className="group relative flex snap-center min-h-[280px] flex-col justify-end overflow-hidden rounded-2xl border border-white/10 bg-ink shadow-lg transition-all duration-500 hover:-translate-y-2 hover:border-gold/30 hover:shadow-[0_20px_40px_-15px_rgba(231,172,64,0.15)] sm:min-h-[300px]"
            >
              {/* Charge photo */}
              <Image
                src={card.image}
                alt={card.title}
                fill
                sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                className="object-cover grayscale contrast-110 brightness-90 transition-all duration-700 group-hover:scale-105 group-hover:grayscale-0 group-hover:contrast-100 group-hover:brightness-100"
              />
              {/* Legibility gradient + gold hover wash */}
              <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink via-ink/85 to-ink/10" />
              <div className="pointer-events-none absolute inset-0 bg-white/0 transition-colors duration-500 group-hover:bg-white/[0.03]" />

              {/* Index number */}
              <m.span
                variants={numberItem}
                className="absolute right-5 top-4 font-display text-[2.5rem] leading-none text-gold drop-shadow-[0_4px_12px_rgba(0,0,0,1)]"
              >
                {String(i + 1).padStart(2, "0")}
              </m.span>

              {/* Title + blurb */}
              <div className="relative z-10 p-6">
                <h3 className="font-display text-xl uppercase tracking-tight text-white [text-shadow:0_2px_12px_rgba(0,0,0,0.85)]">
                  {card.title}
                </h3>
                <p className="mt-2 text-[13.5px] leading-relaxed text-white/75 [text-shadow:0_1px_10px_rgba(0,0,0,0.9)]">
                  {card.blurb}
                </p>
                <p className="mt-3 inline-flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-[0.15em] text-gold [text-shadow:0_1px_10px_rgba(0,0,0,0.9)] transition-transform duration-300 group-hover:translate-x-0.5">
                  {card.href ? "Learn more" : "Free case review"}
                  <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12l-7.5 7.5M21 12H3" />
                  </svg>
                </p>
              </div>

              {/* Whole card is clickable — its landing page when one exists,
                  otherwise straight to the hero QuickForm. */}
              <Link
                href={card.href ?? "#free-review"}
                aria-label={`${card.title} — ${card.href ? "learn more" : "get a free case review"}`}
                className="absolute inset-0 z-20 rounded-2xl focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gold/60"
              />
            </m.div>
          ))}
        </m.div>

        <SectionCta />
      </div>
    </section>
  );
}
