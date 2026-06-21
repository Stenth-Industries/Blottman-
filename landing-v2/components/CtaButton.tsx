import Link from "next/link";

type Props = {
  href: string;
  children: React.ReactNode;
  variant?: "primary" | "ghost";
  className?: string;
};

// Single source of truth for CTA styling — an outline pill (per image copy 4.png):
// light text + a thin light border on a TRANSPARENT background, with a diagonal
// arrow. On hover the text + border + arrow turn gold (a deeper, less-bright
// gold than the headline sheen). No background fill in any state.
export default function CtaButton({
  href,
  children,
  className = "",
}: Props) {
  return (
    <Link
      href={href}
      className={`group inline-flex items-center justify-center gap-3 rounded-full border border-white/45 px-8 py-4 text-[13px] font-semibold uppercase tracking-[0.12em] transition-colors duration-200 hover:border-gold focus:outline-none focus:ring-2 focus:ring-gold/50 ${className}`}
    >
      {/* White by default; the rich-gold gradient is revealed on hover via
          background-clip (same technique as .text-gold-sheen). */}
      <span className="bg-gold-sheen-hover bg-clip-text text-white transition-colors duration-200 group-hover:text-transparent">
        {children}
      </span>
      {/* Diagonal arrow matching the reference; turns gold on hover. */}
      <svg
        viewBox="0 0 24 24"
        aria-hidden="true"
        className="h-4 w-4 shrink-0 text-white transition-[color,transform] duration-200 group-hover:text-gold motion-safe:group-hover:translate-x-0.5 motion-safe:group-hover:-translate-y-0.5"
      >
        <path
          d="M7 17L17 7M17 7H8M17 7V16"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </Link>
  );
}
