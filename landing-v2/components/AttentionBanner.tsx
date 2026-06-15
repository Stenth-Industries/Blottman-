import Link from "next/link";

// Gold attention banner — modelled on Garde Wilson's "first time offender?" strip.
export default function AttentionBanner() {
  return (
    <section className="bg-gold-sheen">
      <div className="section flex flex-col items-center justify-between gap-4 py-7 text-center sm:flex-row sm:text-left">
        <div>
          <p className="font-display text-2xl uppercase leading-none text-ink sm:text-3xl">
            First ticket?
          </p>
          <p className="mt-1 text-sm font-medium text-ink/80">
            Ask how we keep your record — and your insurance — clean.
          </p>
        </div>
        <Link
          href="#quote"
          className="shrink-0 rounded-full border border-ink/30 px-7 py-3 text-[13px] font-semibold uppercase tracking-[0.12em] text-ink transition hover:bg-ink hover:text-gold"
        >
          Find Out More
        </Link>
      </div>
    </section>
  );
}
