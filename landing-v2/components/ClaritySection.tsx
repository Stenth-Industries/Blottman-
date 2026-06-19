"use client";

import { motion, useReducedMotion } from "motion/react";
import CtaButton from "./CtaButton";
import { PHONE_TEL } from "@/lib/content";

export default function ClaritySection() {
  const reduce = useReducedMotion();

  return (
    <section className="bg-ink py-16 sm:py-24 text-white relative overflow-hidden" id="clarity">
      {/* Background glow or texture */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(231,172,64,0.15),transparent_70%)]" />
      
      <div className="section relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          
          {/* Left Column: The Message */}
          <motion.div
            initial={reduce ? false : { opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
          >
            <p className="text-sm font-semibold uppercase tracking-widest text-gold mb-4">
              Licensed Ontario Paralegal
            </p>
            <h2 className="font-display text-4xl sm:text-5xl lg:text-[4rem] leading-[1.05] uppercase tracking-tight text-white">
              Not sure what to do next?
              <br />
              <span className="text-gold-sheen">Send it to Leslie.</span>
            </h2>
            
            <p className="mt-6 text-[15px] sm:text-lg text-white/80 leading-relaxed max-w-lg">
              You do not need to figure this out alone. Whether it's an HTA matter or a serious offence, send what you received. Leslie reviews your charge and explains your options before you decide.
            </p>

            <div className="mt-8 flex flex-col sm:flex-row gap-4">
              <CtaButton href="#quote" className="w-full sm:w-auto text-center justify-center">
                Send My Ticket for Review
              </CtaButton>
              <CtaButton href={`tel:${PHONE_TEL}`} variant="ghost" className="w-full sm:w-auto text-center justify-center">
                <Phone />
                Call Leslie Now
              </CtaButton>
            </div>
          </motion.div>

          {/* Right Column: The "What did you receive?" Checkpoint */}
          <motion.div
            initial={reduce ? false : { opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1], delay: 0.1 }}
            className="relative lg:mt-0 mt-4"
          >
            {/* Soft gold glow behind the card */}
            <div className="absolute -inset-4 rounded-3xl bg-gold/10 blur-2xl" />
            
            <div className="relative rounded-3xl border border-white/10 bg-white/5 backdrop-blur-sm p-6 sm:p-8 shadow-[0_30px_70px_-30px_rgba(12,12,12,0.8)] ring-1 ring-inset ring-white/10">
              <p className="font-display text-xl uppercase tracking-tight text-white mb-6">
                What did you receive?
              </p>
              
              <div className="space-y-3">
                {[
                  {
                    title: "Ticket",
                    desc: "Traffic tickets for speeding, careless driving, cell phone, etc.",
                  },
                  {
                    title: "Summons",
                    desc: "A required court appearance for a serious offence category.",
                  },
                  {
                    title: "Provincial Offence Notice",
                    desc: "Official notice of a charge requiring a deadline response.",
                  }
                ].map((item, idx) => (
                  <button 
                    key={idx} 
                    onClick={() => {
                      const el = document.getElementById('quote');
                      if (el) el.scrollIntoView({ behavior: 'smooth' });
                    }}
                    className="w-full text-left group flex items-start gap-4 rounded-xl border border-white/10 bg-black/20 p-4 transition duration-300 hover:bg-white/10 hover:border-gold/30 cursor-pointer focus:outline-none focus:ring-1 focus:ring-gold/50"
                  >
                    <div className="mt-1 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-white/30 group-hover:border-gold transition-colors">
                      <div className="h-2 w-2 rounded-full bg-gold opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                    <div>
                      <p className="font-display text-lg text-white group-hover:text-gold transition-colors tracking-wide">{item.title}</p>
                      <p className="mt-1 text-sm text-white/60 leading-relaxed">{item.desc}</p>
                    </div>
                  </button>
                ))}
              </div>

              <div className="mt-6 pt-6 border-t border-white/10">
                <p className="text-sm text-white/70 flex items-start gap-3">
                  <ShieldCheck />
                  <span className="leading-relaxed">HTA and provincial offence matters reviewed. Record, licence, and insurance consequences explained.</span>
                </p>
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}

function Phone() {
  return (
    <svg viewBox="0 0 24 24" className="h-4 w-4 mr-2 inline-block" aria-hidden="true">
      <path
        fill="currentColor"
        d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z"
      />
    </svg>
  );
}

function ShieldCheck() {
  return (
    <svg className="h-5 w-5 text-gold shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
    </svg>
  );
}
