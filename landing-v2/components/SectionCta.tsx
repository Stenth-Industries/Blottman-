import CtaButton from "./CtaButton";

// Desktop-only CTA at the end of each major section.
// Hidden on mobile, where a single fixed StickyCta is used instead.
export default function SectionCta({
  label = "Get My Free Case Review",
}: {
  label?: string;
}) {
  return (
    <div className="mt-12 hidden justify-center md:flex">
      <CtaButton href="#quote">{label}</CtaButton>
    </div>
  );
}
