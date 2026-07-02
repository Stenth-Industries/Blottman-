import Link from "next/link";
import { BUSINESS_NAME, PHONE_DISPLAY, PHONE_TEL, CONTACT_EMAIL, TICKET_PAGES } from "@/lib/content";

// Minimal black/gold footer. Carries the business name + a Privacy Policy link,
// which Google's destination policies expect on a page that collects personal
// data (the quote form). Kept light so it doesn't compete with the CTA above it.
// Also links every per-offence landing page (derived from TICKET_PAGES, so a new
// page shows up here automatically) — internal links for visitors and SEO.
export default function Footer() {
  const year = new Date().getFullYear();
  const ticketLinks = Object.values(TICKET_PAGES).map((p) => ({
    label: p.introEyebrow,
    href: `/${p.slug}`,
  }));

  return (
    <footer className="border-t border-white/10 bg-ink py-10 text-white/60">
      <div className="section">
        <nav aria-label="Ticket defence pages" className="mb-8 border-b border-white/10 pb-8">
          <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-white/40">
            What we fight
          </p>
          <ul className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-[13px]">
            {ticketLinks.map((l) => (
              <li key={l.href}>
                <Link href={l.href} className="transition-colors hover:text-gold">
                  {l.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="flex flex-col items-center gap-5 text-center sm:flex-row sm:justify-between sm:text-left">
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
      </div>
    </footer>
  );
}
