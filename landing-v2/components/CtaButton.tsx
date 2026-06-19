import Link from "next/link";

type Props = {
  href: string;
  children: React.ReactNode;
  variant?: "primary" | "ghost";
  arrow?: boolean;
  className?: string;
};

// Garde Wilson CTA style: wide, squared (border-radius 0), FLAT — no glow, no
// drop shadow — with a small diagonal arrow. Gold is an accent, not a glowing
// blob. Primary = solid flat gold; ghost = thin outline on dark backgrounds.
export default function CtaButton({
  href,
  children,
  variant = "primary",
  arrow = true,
  className = "",
}: Props) {
  const base =
    "group inline-flex items-center justify-center gap-3 rounded-none px-9 py-[18px] text-[12px] font-semibold uppercase tracking-[0.22em] transition-colors duration-300 focus:outline-none focus:ring-1 focus:ring-gold/50";
  const styles =
    variant === "primary"
      ? "bg-gold-sheen text-ink hover:brightness-[1.04]"
      : "border border-white/30 text-white hover:border-gold hover:text-gold";

  return (
    <Link href={href} className={`${base} ${styles} ${className}`}>
      <span>{children}</span>
      {arrow && <Arrow />}
    </Link>
  );
}

// Diagonal up-right arrow — Garde Wilson's signature CTA mark.
function Arrow() {
  return (
    <svg
      viewBox="0 0 24 24"
      aria-hidden="true"
      className="h-3.5 w-3.5 shrink-0 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
    >
      <path
        d="M7 17 17 7M8.5 7H17v8.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
