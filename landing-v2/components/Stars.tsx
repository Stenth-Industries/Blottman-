// Star rating rendered as SVGs (not emoji). Supports a fractional last star.
// `color` lets review cards use gold while the Trustpilot widget stays green.
export default function Stars({
  rating,
  color = "#00b67a",
  className = "",
}: {
  rating: number;
  color?: string;
  className?: string;
}) {
  return (
    <div className={`flex items-center gap-0.5 ${className}`} aria-label={`${rating} out of 5 stars`}>
      {Array.from({ length: 5 }, (_, i) => {
        const fill = Math.max(0, Math.min(1, rating - i)) * 100;
        const id = `star-${color.replace("#", "")}-${i}`;
        return (
          <svg key={i} viewBox="0 0 20 20" className="h-5 w-5" aria-hidden="true">
            <defs>
              <linearGradient id={id}>
                <stop offset={`${fill}%`} stopColor={color} />
                <stop offset={`${fill}%`} stopColor="#dcdce6" />
              </linearGradient>
            </defs>
            <rect width="20" height="20" rx="3" fill={`url(#${id})`} />
            <path
              d="M10 4.5l1.6 3.3 3.6.5-2.6 2.5.6 3.6L10 13.2 6.8 14.9l.6-3.6L4.8 8.8l3.6-.5z"
              fill="#fff"
            />
          </svg>
        );
      })}
    </div>
  );
}
