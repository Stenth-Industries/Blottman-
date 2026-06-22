"use client";

import { useState } from "react";
import SectionCta from "./SectionCta";
import { FAQS, PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";

// FAQ accordion answering the biggest objections to fighting a ticket.
export default function Faq() {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <section className="bg-ink border-t border-ink-line py-16 sm:py-32">
      <div className="section">
        <div className="grid grid-cols-1 items-start gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:gap-20">
          
          {/* Left Column: Sticky Header & CTA */}
          <div className="lg:sticky lg:top-32">
            <p className="eyebrow">Questions</p>
            <h2 className="h-section mt-4 text-white">
              Before you just <span className="text-gold-sheen">pay it.</span>
            </h2>
            <p className="mt-5 text-[15px] leading-relaxed text-white/60 sm:max-w-md">
              Paying a ticket is an automatic guilty plea. It immediately goes on your record and can trigger massive insurance hikes. Before you accept the consequences, read the facts.
            </p>
            <div className="mt-10 hidden lg:block">
              <SectionCta label="Talk to a Paralegal — Free" />
              
              <div className="mt-8 border-t border-white/10 pt-6">
                <p className="text-[13px] font-medium tracking-wide text-white/80">
                  Free, no-obligation — average response in under 2 hours.
                </p>
                <div className="mt-3 flex items-center gap-4">
                  <span className="flex items-center gap-2 text-sm font-semibold text-gold">
                    <svg viewBox="0 0 24 24" className="h-4 w-4" aria-hidden="true">
                      <path fill="currentColor" d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z" />
                    </svg>
                    {PHONE_DISPLAY}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Minimalist Accordion */}
          <div className="flex flex-col border-t border-white/10">
            {FAQS.map((item, i) => {
              const isOpen = open === i;
              return (
                <div key={item.q} className="border-b border-white/10">
                  <button
                    onClick={() => setOpen(isOpen ? null : i)}
                    className="group flex w-full items-center justify-between gap-6 py-6 text-left"
                    aria-expanded={isOpen}
                  >
                    <div className="flex items-center gap-5 sm:gap-6">
                      <span className={`font-display text-xl transition-colors duration-300 sm:text-2xl ${isOpen ? "text-gold/80" : "text-white/40 group-hover:text-gold/60"}`}>
                        {(i + 1).toString().padStart(2, '0')}
                      </span>
                      <h3 className={`font-sans text-[1.1rem] leading-snug font-medium transition-colors duration-300 sm:text-xl ${isOpen ? "text-gold" : "text-white/90 group-hover:text-white"}`}>
                        {item.q}
                      </h3>
                    </div>
                    <span
                      className={`grid h-8 w-8 shrink-0 place-items-center rounded-full border transition-all duration-500 ${
                        isOpen ? "rotate-45 border-gold bg-gold text-ink" : "border-white/30 text-white/70 group-hover:border-gold group-hover:text-gold"
                      }`}
                      aria-hidden="true"
                    >
                      <svg viewBox="0 0 24 24" className="h-4 w-4">
                        <path fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" d="M12 5v14M5 12h14" />
                      </svg>
                    </span>
                  </button>
                  <div
                    className={`grid overflow-hidden transition-all duration-500 ease-in-out ${
                      isOpen ? "grid-rows-[1fr] pb-8 opacity-100" : "grid-rows-[0fr] opacity-0"
                    }`}
                  >
                    <p className="min-h-0 text-[15px] leading-relaxed text-white/65 sm:pr-12">{item.a}</p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Mobile CTA (shown at bottom instead of left column) */}
          <div className="mt-4 lg:hidden">
            <SectionCta label="Talk to a Paralegal — Free" />
          </div>

        </div>
      </div>
    </section>
  );
}
