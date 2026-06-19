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
                <p className="mt-0.5 flex items-center gap-1.5 text-xs text-ink-muted">
                  <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" aria-hidden="true">
                    <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5a5.6 5.6 0 0 1-2.4 3.7v3h3.9c2.3-2.1 3.5-5.2 3.5-8.9z" />
                    <path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-2.9l-3.9-3c-1.1.7-2.5 1.2-4.1 1.2-3.1 0-5.8-2.1-6.7-5H1.3v3.1A12 12 0 0 0 12 24z" />
                    <path fill="#FBBC05" d="M5.3 14.3a7.2 7.2 0 0 1 0-4.6V6.6H1.3a12 12 0 0 0 0 10.8z" />
                    <path fill="#EA4335" d="M12 4.8c1.8 0 3.3.6 4.5 1.8l3.4-3.4A12 12 0 0 0 12 0 12 12 0 0 0 1.3 6.6l4 3.1C6.2 6.9 8.9 4.8 12 4.8z" />
                  </svg>
                  Verified Google review
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
