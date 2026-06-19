import Link from "next/link";
import { PHONE_TEL } from "@/lib/content";

// Floating bottom-right action widget — visible on every screen.
// • Call Now  → dials the office (tel: link)
// • Contact Us → scrolls to the quote/case-review form (#quote)
// Styled to match the site's black + gold theme (mirrors CtaButton).
// Labels ("Call Us" / "Contact Us") stay visible on every screen size.
export default function FloatingActions() {
  const base =
    "group inline-flex items-center gap-2 rounded-full px-5 py-3.5 text-[13px] font-semibold uppercase tracking-[0.12em] shadow-lg transition-all duration-200 hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-gold/60";

  return (
    <div className="fixed bottom-6 right-4 z-[60] flex flex-col items-end gap-3 md:right-6">
      {/* Call — primary gold */}
      <a
        href={`tel:${PHONE_TEL}`}
        aria-label="Call Blottman Legal now"
        className={`${base} bg-gold-sheen text-ink shadow-[0_8px_24px_rgba(231,172,64,0.35)] hover:shadow-[0_12px_32px_rgba(231,172,64,0.5)]`}
      >
        <svg
          width="17"
          height="17"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
          className="transition-transform duration-200 group-hover:rotate-12"
        >
          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z" />
        </svg>
        <span>Call Us</span>
      </a>

      {/* Contact Us — dark/ghost with gold border */}
      <Link
        href="#quote"
        aria-label="Contact us for a free case review"
        className={`${base} border border-gold/50 bg-ink/95 text-gold backdrop-blur hover:bg-gold/10`}
      >
        <svg
          width="17"
          height="17"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
          className="transition-transform duration-200 group-hover:-translate-y-0.5"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
        <span>Contact Us</span>
      </Link>
    </div>
  );
}
