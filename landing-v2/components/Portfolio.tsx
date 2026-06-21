import Image from "next/image";
import SectionCta from "./SectionCta";
import { PORTFOLIO } from "@/lib/content";

// "Portfolio" of recent results — outcomes we've secured for clients.
export default function Portfolio() {
  return (
    <section className="bg-ink py-16 sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">Recent Results</p>
          <h2 className="h-section mt-4 text-white">
            A snapshot of <span className="text-gold-sheen">outcomes.</span>
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {PORTFOLIO.map((p) => (
            <div key={p.title} className="card group overflow-hidden">
              <div className="relative aspect-[16/10] bg-ink-soft">
                <Image
                  src={p.image}
                  alt={p.title}
                  fill
                  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                  className="object-cover transition-transform duration-500 group-hover:scale-105"
                />
                <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink/70 to-transparent" />
                <span className="absolute left-4 top-4 rounded-full bg-gold-sheen px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-ink">
                  {p.result}
                </span>
              </div>
              <div className="p-5">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-gold">{p.tag}</p>
                <p className="mt-1.5 font-display text-xl uppercase tracking-tight text-white">{p.title}</p>
              </div>
            </div>
          ))}
        </div>

        <SectionCta />
      </div>
    </section>
  );
}
