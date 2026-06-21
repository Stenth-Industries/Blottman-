import Link from "next/link";
import { PHONE_TEL } from "@/lib/content";

// Persistent call-to-action, visible on every screen.
// • Desktop / tablet (md+): floating stacked pills bottom-right.
// • Mobile (<md): a full-width sticky bottom bar (Call | Contact) — the standard
//   high-converting mobile pattern, and it can't overlap page content the way the
//   floating pills did. globals.css reserves bottom padding so nothing hides behind it.
export default function FloatingActions() {
  const pill =
    "group inline-flex items-center gap-2 rounded-full px-5 py-3.5 text-[13px] font-semibold uppercase tracking-[0.12em] shadow-lg transition-all duration-200 hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-gold/60";

  return (
    <>
      {/* Desktop / tablet — floating stacked pills bottom-right */}
      <div className="fixed bottom-6 right-4 z-[60] hidden flex-col items-end gap-3 md:flex md:right-6">
        <a
          href={`tel:${PHONE_TEL}`}
          aria-label="Call Blottman Legal now"
          className={`${pill} btn-sheen bg-gold-sheen text-ink shadow-[0_8px_24px_rgba(231,172,64,0.35)] hover:shadow-[0_12px_32px_rgba(231,172,64,0.5)]`}
        >
          <PhoneIcon className="transition-transform duration-200 group-hover:rotate-12" />
          <span>Call Us</span>
        </a>
        <Link
          href="#quote"
          aria-label="Contact us for a free case review"
          className={`${pill} border border-gold/50 bg-ink/95 text-gold backdrop-blur hover:bg-gold/10`}
        >
          <ChatIcon className="transition-transform duration-200 group-hover:-translate-y-0.5" />
          <span>Contact Us</span>
        </Link>
      </div>

      {/* Mobile — full-width sticky bottom bar, Call | Contact side by side */}
      <div className="fixed inset-x-0 bottom-0 z-[60] flex border-t border-gold/20 bg-ink/95 backdrop-blur md:hidden [padding-bottom:env(safe-area-inset-bottom)]">
        <a
          href={`tel:${PHONE_TEL}`}
          aria-label="Call Blottman Legal now"
          className="btn-sheen flex flex-1 items-center justify-center gap-2 bg-gold-sheen px-4 py-4 text-[13px] font-semibold uppercase tracking-[0.12em] text-ink"
        >
          <PhoneIcon />
          <span>Call Us</span>
        </a>
        <Link
          href="#quote"
          aria-label="Contact us for a free case review"
          className="flex flex-1 items-center justify-center gap-2 border-l border-gold/20 px-4 py-4 text-[13px] font-semibold uppercase tracking-[0.12em] text-gold"
        >
          <ChatIcon />
          <span>Contact Us</span>
        </Link>
      </div>
    </>
  );
}

function PhoneIcon({ className }: { className?: string }) {
  return (
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
      className={className}
    >
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z" />
    </svg>
  );
}

function ChatIcon({ className }: { className?: string }) {
  return (
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
      className={className}
    >
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  );
}
