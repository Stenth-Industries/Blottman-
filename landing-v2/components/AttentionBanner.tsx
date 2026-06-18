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
            Help protect your record — and your insurance rates. Free case review.
          </p>
        </div>
        <Link
          href="#quote"
          className="shrink-0 rounded-full border border-ink/60 px-7 py-3 text-[13px] font-semibold uppercase tracking-[0.12em] text-ink transition hover:bg-ink hover:text-gold"
        >
          Get My Free Review
        </Link>
      </div>
    </section>
  );
}
