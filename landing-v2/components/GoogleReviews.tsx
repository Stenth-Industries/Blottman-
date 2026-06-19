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
    <section className="bg-ink py-16 sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">Google Reviews</p>
          <h2 className="h-section mt-4 text-white">
            What our <span className="text-gold-sheen">clients say.</span>
          </h2>
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
// container in an effect — the widget then mounts inside our section.
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
      <div className="mt-10 flex flex-col items-center gap-4 rounded-2xl border border-white/10 bg-ink-soft px-6 py-7 text-center shadow-[0_1px_3px_rgba(0,0,0,0.4)] sm:flex-row sm:justify-center sm:gap-6 sm:text-left">
        <GoogleG className="h-9 w-9 shrink-0" />
        <div className="flex flex-col items-center sm:items-start">
          <div className="flex items-baseline gap-2">
            <span className="font-display text-4xl leading-none text-white">
              {GOOGLE_RATING.rating.toFixed(1)}
            </span>
            <span className="text-sm text-white/60">out of 5</span>
          </div>
          <Stars rating={GOOGLE_RATING.rating} color="#e7ac40" className="mt-2" />
        </div>
        <div className="hidden h-12 w-px bg-white/10 sm:block" />
        <div className="flex flex-col items-center sm:items-start">
          <p className="text-sm font-semibold text-white">
            Excellent · {GOOGLE_RATING.reviews}+ Google reviews
          </p>
          <div className="mt-2 flex flex-wrap items-center justify-center gap-3 sm:justify-start">
            <a
              href={reviewUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center rounded-full bg-gold-sheen px-5 py-2 text-[12px] font-semibold uppercase tracking-[0.12em] text-ink transition hover:-translate-y-0.5"
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
      </div>

      <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 md:grid-cols-3">
        {GOOGLE_SAMPLE_REVIEWS.map((r, i) => (
          <figure key={`${r.author}-${i}`} className="card flex flex-col gap-4 p-6">
            <div className="flex items-center justify-between">
              <Stars rating={r.rating} color="#e7ac40" />
              <GoogleG className="h-4 w-4" />
            </div>
            <blockquote className="text-[15px] leading-relaxed text-white/85">
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
