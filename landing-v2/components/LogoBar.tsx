import { BRAND_LOGOS } from "@/lib/content";

// "Featured on" scrolling logo strip — Garde Wilson uses a marquee here.
// 9 placeholder logos; swap each text chip for a real <img> logo later.
export default function LogoBar() {
  const loop = [...BRAND_LOGOS, ...BRAND_LOGOS];
  return (
    <section className="border-b border-ink/10 bg-white py-10">
      <div className="section">
        <p className="text-center text-xs font-semibold uppercase tracking-[0.28em] text-ink-muted">
          As featured in
        </p>
      </div>
      <div className="relative mt-6 overflow-hidden [mask-image:linear-gradient(to_right,transparent,black_12%,black_88%,transparent)]">
        <div className="flex w-max animate-marquee items-center gap-10 px-5">
          {loop.map((name, i) => (
            <span
              key={`${name}-${i}`}
              className="whitespace-nowrap text-lg font-semibold text-ink-muted/70 grayscale transition hover:text-ink hover:grayscale-0"
              title="Placeholder logo"
            >
              {name}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
