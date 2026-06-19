import Image from "next/image";
import SectionCta from "./SectionCta";
import { PROCESS } from "@/lib/content";

// Numbered step-by-step — Garde Wilson "What happens when I'm charged?" pattern.
export default function Process() {
  return (
    <section className="bg-ink py-16 sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">How It Works</p>
          <h2 className="h-section mt-4 text-white">
            From ticket to <span className="text-gold-sheen">resolved.</span>
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {PROCESS.map((p) => (
            <div key={p.step} className="card overflow-hidden">
              <div className="relative aspect-[4/3] bg-ink-soft">
                <Image
                  src={p.image}
                  alt={p.title}
                  fill
                  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
                  className="object-cover"
                />
                <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink/85 via-ink/20 to-transparent" />
                <span className="absolute bottom-3 left-4 font-display text-5xl text-gold drop-shadow-[0_2px_8px_rgba(0,0,0,0.6)]">
                  {p.step}
                </span>
              </div>
              <div className="p-6">
                <h3 className="font-display text-lg uppercase tracking-tight text-white">
                  {p.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-white/65">{p.body}</p>
              </div>
            </div>
          ))}
        </div>

        <SectionCta label="Send Us Your Ticket" />
      </div>
    </section>
  );
}
