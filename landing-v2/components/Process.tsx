import Image from "next/image";
import SectionCta from "./SectionCta";
import { PROCESS } from "@/lib/content";

// Numbered step-by-step — Garde Wilson "What happens when I'm charged?" pattern.
export default function Process() {
  return (
    <section className="relative overflow-hidden bg-ink py-16 sm:py-24">
      {/* Heavy vignette: pure black creeping in from the edges to tightly frame the content */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_30%,#000_100%)] opacity-90" />
      
      <div className="section relative">
        <div className="max-w-2xl">
          <p className="eyebrow">How It Works</p>
          <h2 className="h-section mt-4 text-white">
            How we <span className="text-gold-sheen">fight for you.</span>
          </h2>
          {/* Mobile swipe hint */}
          <div className="mt-6 flex items-center gap-2 text-gold/60 sm:hidden">
            <svg className="h-5 w-5 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
            <span className="font-sans text-xs uppercase tracking-widest">Swipe to explore</span>
          </div>
        </div>

        <div className="mt-16 grid auto-cols-[85%] grid-flow-col snap-x snap-mandatory overflow-x-auto pb-8 sm:auto-cols-auto sm:grid-flow-row sm:grid-cols-2 sm:overflow-visible sm:pb-0 lg:grid-cols-4 gap-4 sm:gap-8">
          {PROCESS.map((p, index) => (
            <div key={p.step} className="group relative flex snap-center flex-col">
              <div className="card relative flex-1 border-white/5 bg-ink-soft/40 transition-all duration-500 hover:-translate-y-2 hover:border-gold/30 hover:bg-ink-soft hover:shadow-[0_20px_40px_-15px_rgba(231,172,64,0.15)]">
                {/* Image Container — clipping only the top corners so the badge below can overflow safely if needed */}
                <div className="relative aspect-[4/3] overflow-hidden rounded-t-2xl bg-ink">
                  <Image
                    src={p.image}
                    alt={p.title}
                    fill
                    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
                    className={`object-cover transition-transform duration-700 group-hover:scale-105 grayscale contrast-125 opacity-80 mix-blend-luminosity ${p.step === "03" ? "brightness-150" : ""}`}
                  />
                  <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink via-ink/20 to-transparent opacity-90 mix-blend-overlay" />
                  
                  {/* Massive Step Number inside the image */}
                  <span className="absolute bottom-6 left-6 font-display text-[3.5rem] leading-none text-gold drop-shadow-[0_4px_24px_rgba(0,0,0,1)]">
                    {p.step}
                  </span>
                </div>

                <div className="px-6 pb-8 pt-8">
                  <h3 className="font-display text-xl uppercase tracking-tight text-white">
                    {p.title}
                  </h3>
                  <p className="mt-3 text-[14.5px] leading-relaxed text-white/65">
                    {p.step === "01" ? (
                      <>
                        Tell us what happened and send us a quick message. <strong className="font-semibold text-white">It takes two minutes and costs nothing.</strong>
                      </>
                    ) : (
                      p.body
                    )}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16">
          <SectionCta label="Send Us a Message" />
        </div>
      </div>
    </section>
  );
}
