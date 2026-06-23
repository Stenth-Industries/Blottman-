"use client";

import { useEffect, useRef } from "react";
import Stars from "./Stars";
import GoogleG from "./GoogleG";
import SectionCta from "./SectionCta";
import {
  TRUSTINDEX_WIDGET_ID,
  GOOGLE_RATING,
  GOOGLE_SAMPLE_REVIEWS,
} from "@/lib/content";

// Google reviews section. Two modes:
//   • TRUSTINDEX_WIDGET_ID set  -> embed the live Trustindex widget (real,
//     auto-updating Google reviews; free, no Google Cloud billing).
//   • not set (default)         -> render styled sample cards so the page is
//     always complete during development / before the widget is connected.
// The section heading/framing is the site's own, so the widget sits inside the
// same black-and-gold layout as the rest of the page.
export default function GoogleReviews() {
  return (
    <section className="bg-ink border-t border-ink-line py-16 sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">Google Reviews</p>
          <h2 className="h-section mt-4 text-white">
            What our <span className="text-gold-sheen">clients say.</span>
          </h2>
          {/* Mobile swipe hint */}
          <div className="mt-6 flex items-center gap-2 text-gold/60 sm:hidden">
            <svg className="h-5 w-5 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
            <span className="font-sans text-xs uppercase tracking-widest">Swipe to explore</span>
          </div>
        </div>

        {TRUSTINDEX_WIDGET_ID ? (
          <TrustindexWidget id={TRUSTINDEX_WIDGET_ID} />
        ) : (
          <SampleReviews />
        )}

        <SectionCta />
      </div>
    </section>
  );
}

// Trustindex renders its widget at the position of its loader <script>. React
// won't execute a script written directly into JSX, so we append it into this
// container in an effect — the widget then mounts inside our section. The widget
// is already themed (dark cards, gold) in the Trustindex dashboard, so we add no
// styling of our own here.
function TrustindexWidget({ id }: { id: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || el.querySelector("script")) return;
    const s = document.createElement("script");
    s.src = `https://cdn.trustindex.io/loader.js?${id}`;
    s.defer = true;
    s.async = true;
    el.appendChild(s);
  }, [id]);

  return <div ref={ref} className="mt-10" />;
}

// Aggregate trust badge + written review cards in the site's dark tokens.
function SampleReviews() {
  const reviewUrl =
    "https://www.google.com/maps/search/?api=1&query=Blottman+Legal+Services+Cookstown";
  return (
    <>
      <div className="mt-10 flex flex-col items-center gap-6 rounded-2xl border border-gold/40 bg-ink-soft px-7 py-7 text-center shadow-[0_0_30px_-12px_rgba(231,172,64,0.4)] sm:flex-row sm:justify-between sm:gap-6 sm:text-left">
        {/* Left — aggregate rating */}
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:gap-5">
          <GoogleG className="h-10 w-10 shrink-0" />
          <div className="flex flex-col items-center sm:items-start">
            <div className="flex items-baseline gap-2">
              <span className="font-display text-4xl leading-none text-white">
                {GOOGLE_RATING.rating.toFixed(1)}
              </span>
              <span className="text-sm text-white/60">out of 5</span>
            </div>
            <Stars rating={GOOGLE_RATING.rating} color="#e7ac40" className="mt-2" />
            <p className="mt-2 text-sm font-semibold text-gold">
              Excellent · {GOOGLE_RATING.reviews}+ Google reviews
            </p>
          </div>
        </div>

        {/* Right — actions */}
        <div className="flex flex-col items-center gap-3 sm:items-end">
          <a
            href={reviewUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center rounded-full bg-gold-sheen px-6 py-2.5 text-[12px] font-semibold uppercase tracking-[0.12em] text-ink shadow-[0_8px_24px_rgba(231,172,64,0.35)] transition hover:-translate-y-0.5"
          >
            Write a Review
          </a>
          <a
            href={reviewUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-semibold text-gold underline-offset-4 hover:underline"
          >
            Read all reviews &rarr;
          </a>
        </div>
      </div>

      <div className="mt-8 grid auto-cols-[85%] grid-flow-col snap-x snap-mandatory overflow-x-auto pb-8 sm:auto-cols-auto sm:grid-flow-row sm:grid-cols-2 sm:overflow-visible sm:pb-0 md:grid-cols-3 gap-5">
        {GOOGLE_SAMPLE_REVIEWS.slice(0, 6).map((r, i) => (
          <figure key={`${r.author}-${i}`} className="card flex snap-center flex-col gap-4 p-6">
            <div className="flex items-center justify-between">
              <Stars rating={r.rating} color="#e7ac40" />
              <GoogleG className="h-4 w-4" />
            </div>
            <blockquote className="text-base leading-relaxed text-white/85">
              &ldquo;{r.text}&rdquo;
            </blockquote>
            <figcaption className="mt-auto flex items-center gap-3 border-t border-white/10 pt-4">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gold-sheen font-display text-sm text-ink">
                {r.author.charAt(0).toUpperCase()}
              </span>
              <div>
                <p className="text-sm font-semibold text-white">{r.author}</p>
                <p className="text-xs text-white/55">
                  {r.relativeTime} · Posted on Google
                </p>
              </div>
            </figcaption>
          </figure>
        ))}
      </div>
    </>
  );
}
