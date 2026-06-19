import Link from "next/link";
import { PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";

// Dark "before you pay your ticket" banner — driving-with-no-insurance intent.
// Sits after the Expertise grid. Black + gold theme, mirrors the site's section styling.
export default function NoInsuranceBanner() {
  return (
    <section className="bg-ink py-16 text-white sm:py-20">
      <div className="section max-w-3xl text-center">
        <p className="inline-flex items-center justify-center gap-2.5 text-xs font-semibold uppercase tracking-[0.28em] text-gold">Driving With No Insurance</p>
        <h2 className="h-section mt-4">
          Charged With Driving With No Insurance in{" "}
          <span className="text-gold-sheen">Ontario?</span>
        </h2>
        <p className="mx-auto mt-5 max-w-2xl text-[15px] leading-relaxed text-white/70">
          The decisions you make now could affect your driving record, insurance premiums,
          and future options. Before paying your ticket, speak with Blottman Legal Services
          to understand your rights and the options available to you.
        </p>

        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Link
            href="#quote"
            className="inline-flex items-center justify-center rounded-full bg-gold-sheen px-8 py-4 text-[13px] font-semibold uppercase tracking-[0.12em] text-ink shadow-[0_8px_24px_rgba(231,172,64,0.35)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_12px_32px_rgba(231,172,64,0.5)] focus:outline-none focus:ring-2 focus:ring-gold/60"
          >
            Speak With Blottman Legal
          </Link>
          <a
            href={`tel:${PHONE_TEL}`}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-gold/50 px-8 py-4 text-[13px] font-semibold uppercase tracking-[0.12em] text-gold transition-all duration-200 hover:-translate-y-0.5 hover:bg-gold/10 focus:outline-none focus:ring-2 focus:ring-gold/60"
          >
            Call {PHONE_DISPLAY}
          </a>
        </div>
      </div>
    </section>
  );
}
