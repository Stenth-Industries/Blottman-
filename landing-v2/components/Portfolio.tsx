import Image from "next/image";
import SectionCta from "./SectionCta";
import { PORTFOLIO } from "@/lib/content";

// "Portfolio" of recent results — real outcomes clients described in their own
// verified Google reviews (see PORTFOLIO in lib/content.ts for the source quotes).
export default function Portfolio() {
  return (
    <section className="bg-ink py-16 sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">Recent Results</p>
          <h2 className="h-section mt-4 text-white">
            A snapshot of <span className="text-gold-sheen">outcomes.</span>
          </h2>
          <p className="mt-4 text-[14.5px] leading-relaxed text-white/60">
            Real results clients shared in their verified Google reviews. Every case is different —
            past outcomes don&apos;t guarantee future ones.
          </p>
        </div>

        <div className="mt-14 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 lg:gap-8">
          {PORTFOLIO.map((p) => (
            <div key={p.title} className="group relative flex flex-col overflow-hidden rounded-2xl border border-white/5 border-t-gold/40 bg-ink-soft/30 shadow-lg transition-all duration-500 hover:-translate-y-1 hover:border-gold/40 hover:bg-ink-soft/60 hover:shadow-[0_15px_30px_-10px_rgba(231,172,64,0.15)]">
              {/* Image Container — Graded to match luxury aesthetic */}
              <div className="relative aspect-[16/10] overflow-hidden bg-ink">
                <Image
                  src={p.image}
                  alt={p.title}
                  fill
                  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                  className="object-cover transition-transform duration-700 group-hover:scale-105 grayscale contrast-125 opacity-75 mix-blend-luminosity"
                />
                <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink via-ink/40 to-transparent opacity-90 mix-blend-overlay" />
                
                {/* Charge Label overlaying the image like a case file tab */}
                <div className="absolute left-0 top-6 rounded-r-lg border border-l-0 border-white/10 border-r-gold/30 bg-ink/90 py-2 pl-6 pr-5 shadow-lg backdrop-blur-md">
                  <span className="text-[10px] font-bold uppercase tracking-[0.25em] text-white/60">
                    Charge // <span className="text-white">{p.title}</span>
                  </span>
                </div>
              </div>

              {/* Outcome Content (Flipped Hierarchy to sell the result) */}
              <div className="flex flex-1 flex-col justify-center p-6 pt-7">
                <h3 className="font-display text-[1.65rem] leading-[1.1] uppercase tracking-tight text-gold-sheen">
                  {p.result}
                </h3>
                <div className="mt-4 flex items-center gap-3">
                  <p className="text-[12.5px] font-semibold tracking-wide text-white/70">
                    {p.tag}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16">
          <SectionCta />
        </div>
      </div>
    </section>
  );
}
