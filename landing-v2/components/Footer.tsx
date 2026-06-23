import Link from "next/link";
import { BUSINESS_NAME, PHONE_DISPLAY, PHONE_TEL, CONTACT_EMAIL } from "@/lib/content";

// Minimal black/gold footer. Carries the business name + a Privacy Policy link,
// which Google's destination policies expect on a page that collects personal
// data (the quote form). Kept light so it doesn't compete with the CTA above it.
export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="border-t border-white/10 bg-ink py-10 text-white/60">
      <div className="section flex flex-col items-center gap-5 text-center sm:flex-row sm:justify-between sm:text-left">
        <div>
          <p className="font-display text-lg uppercase tracking-wide text-white">{BUSINESS_NAME}</p>
          <p className="mt-1 text-[13px]">Ontario traffic-ticket defence · Licensed paralegal</p>
        </div>

        <div className="flex flex-col items-center gap-2 text-[13px] sm:items-end">
          <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-1">
            <a href={`tel:${PHONE_TEL}`} className="transition-colors hover:text-gold">{PHONE_DISPLAY}</a>
            <a href={`mailto:${CONTACT_EMAIL}`} className="transition-colors hover:text-gold">{CONTACT_EMAIL}</a>
            <Link href="/privacy" className="transition-colors hover:text-gold">Privacy Policy</Link>
          </div>
          <p className="text-white/40">© {year} {BUSINESS_NAME}. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
