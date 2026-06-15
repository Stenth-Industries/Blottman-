import Stars from "./Stars";
import { TRUSTPILOT } from "@/lib/content";

// Placeholder Trustpilot widget — 4.7 stars across 67 reviews.
// Replace with the official Trustpilot embed script when available.
export default function Trustpilot() {
  return (
    <section className="bg-paper py-12">
      <div className="section">
        <div className="mx-auto flex max-w-2xl flex-col items-center gap-3 rounded-2xl border border-ink/10 bg-white px-8 py-8 text-center shadow-[0_1px_3px_rgba(12,12,12,0.06)]">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink">
            <span className="inline-block h-4 w-4 rounded-sm bg-[#00b67a]" aria-hidden="true" />
            Trustpilot
          </div>
          <Stars rating={TRUSTPILOT.rating} className="scale-110" />
          <p className="font-display text-3xl text-ink">{TRUSTPILOT.rating} OUT OF 5</p>
          <p className="text-sm text-ink-muted">Based on {TRUSTPILOT.reviews} verified reviews</p>
          <p className="text-xs text-ink-muted/60">Placeholder widget — connect the live Trustpilot embed when ready.</p>
        </div>
      </div>
    </section>
  );
}
