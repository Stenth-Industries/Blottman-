"use client";

import type { CSSProperties } from "react";
import Image from "next/image";
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
      <Image
        src="/what-we-fight-bg-3.webp"
        alt=""
        aria-hidden="true"
        fill
        sizes="100vw"
        className="pointer-events-none object-cover opacity-[0.67]"
      />
      {/* horizontal overlay: near-black through the centre behind the grid, lighter at the edges so the road shows only there */}
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-r from-ink/35 via-ink to-ink/35" />
      {/* stronger centre darkening behind the offence grid so the cards sit on clean near-black */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_72%_92%_at_center,rgba(12,12,12,0.82),transparent_72%)]" />
      {/* warm gold glow on the far left and far right edges (slightly reduced) */}
      <div className="pointer-events-none absolute -left-44 top-1/2 h-[30rem] w-[30rem] -translate-y-1/2 rounded-full bg-gold/8 blur-[140px]" />
      <div className="pointer-events-none absolute -right-44 top-1/2 h-[30rem] w-[30rem] -translate-y-1/2 rounded-full bg-gold/8 blur-[140px]" />
      <div className="section relative z-10 max-w-[1180px]">
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
        </m.div>

        <m.div
          className="mt-12 grid grid-cols-1 gap-px overflow-hidden rounded-2xl border border-ink-line bg-ink-line sm:grid-cols-2 lg:grid-cols-3"
          variants={container}
          initial={reduce ? false : "hidden"}
          whileInView="show"
          viewport={{ once: true, margin: "-80px" }}
        >
          {EXPERTISE.map((card, i) => (
            <m.div
              key={card.title}
              variants={item}
              className="group relative overflow-hidden bg-ink p-5"
              style={
                card.image
                  ? ({
                      "--img-o": card.imageOpacity ?? 0.18,
                      "--img-oh": (card.imageOpacity ?? 0.18) + 0.1,
                    } as CSSProperties)
                  : undefined
              }
            >
              {card.image && (
                <>
                  {/* subtle right-side background texture (already a dark photo) */}
                  <div className="pointer-events-none absolute inset-y-0 right-0 w-2/3">
                    <Image
                      src={card.image}
                      alt=""
                      aria-hidden="true"
                      fill
                      sizes="(max-width: 1024px) 60vw, 25vw"
                      className="object-cover object-center opacity-[var(--img-o)]"
                    />
                  </div>
                  {/* strong dark gradient on the left so the text area stays clean; image stays visible on the right */}
                  <div className="pointer-events-none absolute inset-0 bg-gradient-to-r from-ink from-[38%] via-ink/65 to-ink/5" />
                </>
              )}
              <div className={`relative z-10 ${card.image ? "sm:max-w-[58%]" : ""}`}>
                <m.span
                  variants={numberItem}
                  className="inline-block origin-left font-display text-2xl text-gold/60 transition-all duration-300 group-hover:scale-110 group-hover:text-gold"
                >
                  {String(i + 1).padStart(2, "0")}
                </m.span>
                <h3 className="mt-4 font-display text-xl uppercase tracking-tight text-white [text-shadow:0_1px_10px_rgba(12,12,12,0.6)]">
                  {card.title}
                </h3>
                <p className="mt-2 text-base leading-relaxed text-white/70 [text-shadow:0_1px_8px_rgba(12,12,12,0.6)]">{card.blurb}</p>
              </div>
            </m.div>
          ))}
        </m.div>

        <SectionCta />
      </div>
    </section>
  );
}
