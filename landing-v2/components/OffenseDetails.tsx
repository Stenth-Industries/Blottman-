"use client";

import Image from "next/image";
import Link from "next/link";
import { m, useReducedMotion } from "motion/react";
import { type TicketPage, PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";

export default function OffenseDetails({ page }: { page: TicketPage }) {
  const reduce = useReducedMotion();

  // If we don't have a background image, fallback to the abstract siren one
  const bgImage = page.bgImage || "/abstract_siren_bg.png";

  return (
    <section className="relative overflow-hidden bg-ink py-16 text-white sm:py-24">
      {/* Background Image with seamless top/bottom fades and vignette */}
      <div className="pointer-events-none absolute inset-0">
        <img
          src={bgImage}
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

      {/* Large vertical typography (Luxury fashion style) */}
      <div
        className="pointer-events-none absolute -left-48 top-1/2 flex -translate-y-1/2 -rotate-90 select-none items-center whitespace-nowrap opacity-[0.02]"
        aria-hidden="true"
      >
        <span className="display text-[clamp(6rem,18vw,14rem)] text-white">
          {page.introEyebrow} Defence
        </span>
      </div>

      <div className="section relative z-10 max-w-5xl text-center">
        <p className="eyebrow justify-center">{page.introEyebrow}</p>
        <h2 className="h-section mt-4">
          {page.introHeading.split(' Ontario?')[0]}
          {page.introHeading.includes(' Ontario?') && (
            <>
              {" "}
              <span className="text-gold-sheen">Ontario?</span>
            </>
          )}
        </h2>
        <p className="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-white/70">
          {page.introBody}
        </p>

        {/* Static Glassmorphism Penalty Grid (Large Uppercase Gold Titles) */}
        {page.consequences && page.consequences.length > 0 && (
          <div className={`mt-16 grid grid-cols-1 gap-6 text-left sm:grid-cols-${Math.min(page.consequences.length, 3)}`}>
            {page.consequences.map((c, i) => (
              <m.div
                key={i}
                initial={reduce ? false : { opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.5, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] }}
              >
                <div className="group relative flex h-full flex-col items-start overflow-hidden rounded-2xl bg-ink/40 p-8 ring-1 ring-inset ring-white/5 backdrop-blur-xl transition-all duration-500 hover:-translate-y-1.5 hover:shadow-[0_12px_32px_rgba(255,255,255,0.04)]">
                  {/* Very subtle glossy top highlight for that glass edge feel */}
                  <div className="absolute inset-x-0 top-0 h-px w-full bg-gradient-to-r from-transparent via-white/10 to-transparent opacity-30" />
                  
                  {/* Muted Icon in a dark circle - ONLY thing that highlights on hover */}
                  <span className="grid h-12 w-12 place-items-center rounded-full bg-white/5 text-white/40 transition-colors duration-500 group-hover:bg-white/15 group-hover:text-white">
                    {c.icon ? <CardIcon name={c.icon} /> : `0${i + 1}`}
                  </span>
                  
                  {/* Massive Uppercase Gold Value & White Label (Matching No Insurance Banner) */}
                  <div className="mt-8 flex flex-col gap-1">
                    <span className="font-display text-[2rem] uppercase leading-none tracking-tight text-gold-sheen sm:text-[2.5rem]">
                      {c.titleValue}
                    </span>
                    <span className="font-sans text-[13px] font-semibold uppercase tracking-[0.15em] text-white">
                      {c.titleLabel}
                    </span>
                  </div>
                  
                  <p className="mt-4 text-[13.5px] leading-relaxed text-white/70">
                    {c.description}
                  </p>
                </div>
              </m.div>
            ))}
          </div>
        )}

        <p className="mx-auto mt-10 max-w-2xl text-base leading-relaxed text-white/70">
          Blottman Legal Services works to reduce the charge, lower the fine, and protect your
          record. Speak with us before paying — once you pay, you&apos;ve pleaded guilty.
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
            Get a Free Case Review
          </Link>
        </div>
      </div>
    </section>
  );
}

// Crisp, pure SVG icons (Lucide/feather style) — completely non-AI.
function CardIcon({ name }: { name: string }) {
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
  if (name === "suspend" || name === "record") {
    // Lucide "id-card" / "file-text"
    return (
      <svg {...common}>
        <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
        <line x1="10" y1="9" x2="8" y2="9" />
      </svg>
    );
  }
  if (name === "impound") {
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
  if (name === "points" || name === "alert") {
    // Lucide "alert-triangle"
    return (
      <svg {...common}>
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
        <line x1="12" y1="9" x2="12" y2="13" />
        <line x1="12" y1="17" x2="12.01" y2="17" />
      </svg>
    );
  }
  if (name === "insurance") {
    // Lucide "trending-up"
    return (
      <svg {...common}>
        <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
        <polyline points="16 7 22 7 22 13" />
      </svg>
    );
  }
  if (name === "jail") {
    // Lucide "lock"
    return (
      <svg {...common}>
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      </svg>
    );
  }

  // Fallback star icon
  return (
    <svg {...common}>
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  );
}
