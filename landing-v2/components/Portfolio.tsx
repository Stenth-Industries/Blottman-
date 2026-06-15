import SectionCta from "./SectionCta";
import { PORTFOLIO } from "@/lib/content";

// "Portfolio" of recent results — outcomes we've secured for clients.
export default function Portfolio() {
  return (
    <section className="bg-paper py-16 sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">Recent Results</p>
          <h2 className="h-section mt-4">
            A snapshot of <span className="text-gold-sheen">outcomes.</span>
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {PORTFOLIO.map((p) => (
            <div key={p.title} className="card group overflow-hidden">
              <div className="relative flex aspect-[16/10] items-center justify-center bg-ink">
                <span className="text-xs uppercase tracking-[0.2em] text-white/30">Image placeholder</span>
                <span className="absolute left-4 top-4 rounded-full bg-gold-sheen px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-ink">
                  {p.result}
                </span>
              </div>
              <div className="p-5">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-gold-deep">{p.tag}</p>
                <p className="mt-1.5 font-display text-lg uppercase tracking-tight text-ink">{p.title}</p>
              </div>
            </div>
          ))}
        </div>

        <SectionCta />
      </div>
    </section>
  );
}
