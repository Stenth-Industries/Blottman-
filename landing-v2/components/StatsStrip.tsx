"use client";

import { useEffect, useRef, useState } from "react";
import { m, useInView, useReducedMotion, type Variants } from "motion/react";

// Premium trust strip below the hero. Dark, minimal, gold used lightly.
// Claims are legally safe — no win-rate or outcome guarantees.
const STATS: { count?: number; suffix?: string; value?: string; label: string }[] = [
  { count: 500, suffix: "+", label: "Tickets Handled" },
  { value: "Fixed Fees", label: "No Surprises" },
  { value: "Licensed", label: "Ontario Paralegal" },
  { value: "24/7", label: "Free Case Review" },
];

const container: Variants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
};
const item: Variants = {
  hidden: { opacity: 0, y: 18 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] } },
};

export default function StatsStrip() {
  const reduce = useReducedMotion();

  return (
    <section className="border-y border-ink-line bg-ink">
      <div className="section">
        <m.div
          className="grid grid-cols-2 lg:grid-cols-4"
          variants={container}
          initial={reduce ? false : "hidden"}
          whileInView="show"
          viewport={{ once: true, margin: "-80px" }}
        >
          {STATS.map((s) => (
            <m.div
              key={s.label}
              variants={item}
              className="px-6 py-9 text-center border-ink-line [&:nth-child(even)]:border-l [&:nth-child(n+3)]:border-t lg:[&:nth-child(n+2)]:border-l lg:[&:nth-child(n+3)]:border-t-0"
            >
              <p className="font-display text-3xl uppercase tracking-tight text-white sm:text-4xl">
                {s.count != null ? <CountUp to={s.count} suffix={s.suffix} /> : s.value}
              </p>
              <span className="mx-auto mt-3 block h-px w-7 bg-gold/50" />
              <p className="mt-3 text-xs uppercase tracking-[0.18em] text-white/55">{s.label}</p>
            </m.div>
          ))}
        </m.div>
      </div>
    </section>
  );
}

// Counts up to `to` once the element scrolls into view.
function CountUp({ to, suffix = "", duration = 1.4 }: { to: number; suffix?: string; duration?: number }) {
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });
  const reduce = useReducedMotion();
  const [n, setN] = useState(0);

  useEffect(() => {
    if (!inView) return;
    if (reduce) {
      setN(to);
      return;
    }
    let raf = 0;
    const start = performance.now();
    const tick = (t: number) => {
      const p = Math.min(1, (t - start) / (duration * 1000));
      setN(Math.round((1 - Math.pow(1 - p, 3)) * to));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [inView, to, duration, reduce]);

  return (
    <span ref={ref}>
      {n}
      {suffix}
    </span>
  );
}
