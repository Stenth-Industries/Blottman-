import CtaButton from "./CtaButton";

// Mobile-only: ONE call-to-action fixed to the bottom of the screen,
// staying visible as the user scrolls. Hidden on desktop (md and up).
export default function StickyCta() {
  return (
    <div className="fixed inset-x-0 bottom-0 z-50 border-t border-gold/20 bg-ink/95 px-4 py-3 backdrop-blur md:hidden">
      <CtaButton href="#quote" className="w-full">
        Get My Free Case Review
      </CtaButton>
    </div>
  );
}
