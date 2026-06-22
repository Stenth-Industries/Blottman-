"use client";

import { m, useReducedMotion, type HTMLMotionProps } from "motion/react";

type Props = {
  children: React.ReactNode;
  delay?: number;
  className?: string;
} & HTMLMotionProps<"div">;

// Reusable scroll-reveal: section fades + rises once as it enters the viewport.
// Respects prefers-reduced-motion (renders static).
export default function Reveal({ children, delay = 0, className, ...rest }: Props) {
  const reduce = useReducedMotion();

  if (reduce) {
    return <div className={className}>{children}</div>;
  }

  return (
    <m.div
      className={className}
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1], delay }}
      {...rest}
    >
      {children}
    </m.div>
  );
}
