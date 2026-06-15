import SectionCta from "./SectionCta";
import { CASE_STUDIES } from "@/lib/content";

// 2 before/after case studies.
export default function CaseStudies() {
  return (
    <section className="bg-ink py-16 text-white sm:py-24">
      <div className="section">
        <div className="max-w-2xl">
          <p className="eyebrow">Before &amp; After</p>
          <h2 className="h-section mt-4 text-white">
            Real <span className="text-gold-sheen">transformations.</span>
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-6 lg:grid-cols-2">
          {CASE_STUDIES.map((cs) => (
            <article key={cs.title} className="rounded-2xl border border-ink-line bg-ink-soft p-7">
              <h3 className="font-display text-xl uppercase tracking-tight text-white">{cs.title}</h3>
              <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
                <Column tone="before" label={cs.before.label} points={cs.before.points} />
                <Column tone="after" label={cs.after.label} points={cs.after.points} />
              </div>
            </article>
          ))}
        </div>

        <SectionCta />
      </div>
    </section>
  );
}

function Column({
  tone,
  label,
  points,
}: {
  tone: "before" | "after";
  label: string;
  points: string[];
}) {
  const isAfter = tone === "after";
  return (
    <div
      className={`rounded-xl p-5 ${
        isAfter ? "bg-gold-sheen text-ink" : "bg-ink ring-1 ring-ink-line"
      }`}
    >
      <p
        className={`font-display text-sm uppercase tracking-[0.15em] ${
          isAfter ? "text-ink/70" : "text-gold"
        }`}
      >
        {label}
      </p>
      <ul className="mt-3 space-y-2.5 text-sm">
        {points.map((pt) => (
          <li key={pt} className="flex items-start gap-2">
            <span
              className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${
                isAfter ? "bg-ink/70" : "bg-gold"
              }`}
            />
            <span className={isAfter ? "text-ink/90" : "text-white/80"}>{pt}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
