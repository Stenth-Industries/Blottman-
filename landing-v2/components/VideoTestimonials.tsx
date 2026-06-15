import SectionCta from "./SectionCta";
import { VIDEO_TESTIMONIALS } from "@/lib/content";

// 3x3 grid of video testimonials. Each tile is a placeholder until real
// footage is added — swap the inner div for a <video> or embed.
export default function VideoTestimonials() {
  return (
    <section className="bg-ink py-16 text-white sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">In Their Words</p>
          <h2 className="h-section mt-4 text-white">
            Hear it from <span className="text-gold-sheen">drivers we&apos;ve helped.</span>
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-5 sm:grid-cols-2 md:grid-cols-3">
          {VIDEO_TESTIMONIALS.map((v) => (
            <div
              key={v.id}
              className="group relative flex aspect-video items-center justify-center overflow-hidden rounded-2xl border border-ink-line bg-ink-soft"
            >
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(231,172,64,0.12),transparent_65%)]" />
              <div className="flex flex-col items-center gap-3 text-center">
                <span className="flex h-14 w-14 items-center justify-center rounded-full bg-white/5 ring-1 ring-gold/30 transition group-hover:bg-gold group-hover:ring-gold">
                  <svg viewBox="0 0 24 24" className="h-6 w-6 text-gold transition group-hover:text-ink" aria-hidden="true">
                    <path fill="currentColor" d="M8 5v14l11-7z" />
                  </svg>
                </span>
                <span className="text-xs font-medium uppercase tracking-[0.15em] text-white/50">
                  {v.caption}
                </span>
              </div>
            </div>
          ))}
        </div>

        <SectionCta />
      </div>
    </section>
  );
}
