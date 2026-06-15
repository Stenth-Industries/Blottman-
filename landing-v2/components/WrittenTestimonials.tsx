import SectionCta from "./SectionCta";
import Stars from "./Stars";
import { WRITTEN_TESTIMONIALS } from "@/lib/content";

// 3x3 grid of written testimonials — review-card style with gold stars.
export default function WrittenTestimonials() {
  return (
    <section className="bg-white py-16 sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">Reviews</p>
          <h2 className="h-section mt-4">
            What our <span className="text-gold-sheen">clients say.</span>
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-5 sm:grid-cols-2 md:grid-cols-3">
          {WRITTEN_TESTIMONIALS.map((t) => (
            <figure key={t.name} className="card flex flex-col gap-4 p-6">
              <Stars rating={5} color="#e7ac40" />
              <blockquote className="text-[15px] leading-relaxed text-ink/90">
                &ldquo;{t.quote}&rdquo;
              </blockquote>
              <figcaption className="mt-auto border-t border-ink/10 pt-4">
                <p className="text-sm font-semibold text-ink">{t.name}</p>
                <p className="text-xs text-ink-muted">
                  {t.location} · {t.date}
                </p>
              </figcaption>
            </figure>
          ))}
        </div>

        <SectionCta />
      </div>
    </section>
  );
}
