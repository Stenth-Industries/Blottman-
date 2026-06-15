import Link from "next/link";

type Props = {
  href: string;
  children: React.ReactNode;
  variant?: "primary" | "ghost";
  className?: string;
};

// Single source of truth for CTA styling — gold, bold, uppercase (Garde Wilson style).
export default function CtaButton({
  href,
  children,
  variant = "primary",
  className = "",
}: Props) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-full px-8 py-4 text-[13px] font-semibold uppercase tracking-[0.12em] transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gold/60";
  const styles =
    variant === "primary"
      ? "bg-gold-sheen text-ink shadow-[0_8px_24px_rgba(231,172,64,0.35)] hover:-translate-y-0.5 hover:shadow-[0_12px_32px_rgba(231,172,64,0.5)]"
      : "border border-gold/50 text-gold hover:bg-gold/10";

  return (
    <Link href={href} className={`${base} ${styles} ${className}`}>
      {children}
    </Link>
  );
}
