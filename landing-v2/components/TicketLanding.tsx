import Hero from "@/components/Hero";
import Reveal from "@/components/Reveal";
import StatsStrip from "@/components/StatsStrip";
import Expertise from "@/components/Expertise";
import Process from "@/components/Process";
import GoogleReviews from "@/components/GoogleReviews";
import Faq from "@/components/Faq";
import QuoteForm from "@/components/QuoteForm";
import FloatingActions from "@/components/FloatingActions";
import NoInsuranceBanner from "@/components/NoInsuranceBanner";
import Footer from "@/components/Footer";
import { FAQS, type TicketPage } from "@/lib/content";

// FAQPage JSON-LD (same FAQs as the homepage) so each ticket page is eligible
// for rich results too.
const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: FAQS.map(({ q, a }) => ({
    "@type": "Question",
    name: q,
    acceptedAnswer: { "@type": "Answer", text: a },
  })),
};

// Reusable SKAG landing template. Renders the shared trust sections with a hero
// + intro matched to one ticket type (TicketPage). Each per-ticket route
// (app/<slug>/page.tsx) just hands its TICKET_PAGES entry to this. Keeps every
// ticket page on-brand and fully tracked (same QuoteForm → /api/lead).
export default function TicketLanding({ page }: { page: TicketPage }) {
  return (
    <main>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }} />
      <Hero
        eyebrow={page.eyebrow}
        titleLine1={page.titleLine1}
        titleLine2={page.titleLine2}
        titleHighlight={page.titleHighlight}
        benefits={page.benefits}
      />
      <StatsStrip />
      <Reveal><TicketIntro page={page} /></Reveal>
      <Reveal><Expertise /></Reveal>
      <Reveal><NoInsuranceBanner /></Reveal>
      <Reveal><Process /></Reveal>
      <Reveal><GoogleReviews /></Reveal>
      <Reveal><Faq /></Reveal>
      <Reveal><QuoteForm /></Reveal>
      <Footer />
      <FloatingActions />
    </main>
  );
}

// Charge-specific intro block — the message-match copy that mirrors the search
// term and gives the page unique, indexable content.
function TicketIntro({ page }: { page: TicketPage }) {
  return (
    <section className="bg-ink py-16 text-white sm:py-24">
      <div className="section max-w-3xl">
        <p className="eyebrow">{page.introEyebrow}</p>
        <h2 className="h-section mt-4 text-white">{page.introHeading}</h2>
        <p className="mt-6 text-[15px] leading-relaxed text-white/70">{page.introBody}</p>
      </div>
    </section>
  );
}
