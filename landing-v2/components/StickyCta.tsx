import CtaButton from "./CtaButton";
import { PHONE_TEL } from "@/lib/content";

// Mobile-only: ONE call-to-action fixed to the bottom of the screen, staying
// visible as the user scrolls. It's a tap-to-call button — the fastest action
// for stressed mobile traffic. Hidden on desktop (md and up).
export default function StickyCta() {
  return (
    <div className="fixed inset-x-0 bottom-0 z-50 border-t border-gold/20 bg-ink/95 px-4 py-3 backdrop-blur md:hidden">
      <CtaButton href={`tel:${PHONE_TEL}`} arrow={false} className="w-full">
        <Phone />
        Call Us Now
      </CtaButton>
    </div>
  );
}

function Phone() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" className="mr-2 inline-block h-4 w-4 align-[-3px]">
      <path
        fill="currentColor"
        d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1z"
      />
    </svg>
  );
}
