"use client";

import { useState } from "react";
import SectionCta from "./SectionCta";
import { FAQS } from "@/lib/content";

// FAQ accordion answering the biggest objections to fighting a ticket.
export default function Faq() {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <section className="bg-paper py-16 sm:py-24">
      <div className="section max-w-3xl">
        <div className="text-center">
          <p className="eyebrow justify-center">Questions</p>
          <h2 className="h-section mt-4">
            Before you just <span className="text-gold-sheen">pay it.</span>
          </h2>
        </div>

        <div className="mt-12 divide-y divide-ink/10 overflow-hidden rounded-2xl border border-ink/10 bg-white">
          {FAQS.map((item, i) => {
            const isOpen = open === i;
            return (
              <div key={item.q}>
                <button
                  onClick={() => setOpen(isOpen ? null : i)}
                  className="flex w-full items-center justify-between gap-4 px-5 py-5 text-left"
                  aria-expanded={isOpen}
                >
                  <span className="text-base font-semibold text-ink">{item.q}</span>
                  <span
                    className={`grid h-7 w-7 shrink-0 place-items-center rounded-full border border-gold/40 text-gold transition-transform ${
                      isOpen ? "rotate-45 bg-gold-sheen text-ink" : ""
                    }`}
                    aria-hidden="true"
                  >
                    <svg viewBox="0 0 24 24" className="h-4 w-4">
                      <path fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" d="M12 5v14M5 12h14" />
                    </svg>
                  </span>
                </button>
                <div
                  className={`grid overflow-hidden px-5 transition-all duration-300 ${
                    isOpen ? "grid-rows-[1fr] pb-5 opacity-100" : "grid-rows-[0fr] opacity-0"
                  }`}
                >
                  <p className="min-h-0 text-[15px] leading-relaxed text-ink-muted">{item.a}</p>
                </div>
              </div>
            );
          })}
        </div>

        <SectionCta label="Talk to a Paralegal — Free" />
      </div>
    </section>
  );
}
