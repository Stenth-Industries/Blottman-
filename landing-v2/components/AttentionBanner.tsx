import Link from "next/link";

// Gold attention banner — modelled on Garde Wilson's "first time offender?" strip.
export default function AttentionBanner() {
  return (
    <section className="bg-gold-sheen" aria-labelledby="attention-banner-heading">
      <div className="section flex flex-col items-center justify-between gap-4 py-7 text-center sm:flex-row sm:text-left">
        <div>
          <h2
            id="attention-banner-heading"
            className="font-display text-2xl uppercase leading-none text-ink sm:text-3xl"
          >
            Got a ticket?
          </h2>
          <p className="mt-1 text-sm font-medium text-ink">
            Help protect your record and your insurance rates. Free case review.
          </p>
        </div>
        <Link
          href="#quote"
          className="group inline-flex shrink-0 items-center gap-3 rounded-none border border-ink/60 px-9 py-3.5 text-[12px] font-semibold uppercase tracking-[0.22em] text-ink transition-colors hover:bg-ink hover:text-gold"
        >
          Get My Free Review
          <svg viewBox="0 0 24 24" aria-hidden="true" className="h-3.5 w-3.5 shrink-0 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5">
            <path d="M7 17 17 7M8.5 7H17v8.5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </Link>
      </div>
    </section>
  );
}
