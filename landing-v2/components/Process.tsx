import SectionCta from "./SectionCta";
import { PROCESS } from "@/lib/content";

// Numbered step-by-step — Garde Wilson "What happens when I'm charged?" pattern.
export default function Process() {
  return (
    <section className="bg-paper py-16 sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">How It Works</p>
          <h2 className="h-section mt-4">
            From ticket to <span className="text-gold-sheen">resolved.</span>
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {PROCESS.map((p) => (
            <div key={p.step} className="card overflow-hidden">
              <div className="relative flex aspect-[4/3] items-center justify-center bg-ink">
                <span className="font-display text-6xl text-gold/25">{p.step}</span>
                <span className="absolute bottom-3 right-3 text-[10px] uppercase tracking-[0.2em] text-white/30">
                  Image
                </span>
              </div>
              <div className="p-6">
                <h3 className="font-display text-lg uppercase tracking-tight text-ink">
                  {p.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-muted">{p.body}</p>
              </div>
            </div>
          ))}
        </div>

        <SectionCta label="Send Us Your Ticket" />
      </div>
    </section>
  );
}
