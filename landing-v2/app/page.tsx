import Hero from "@/components/Hero";
import Reveal from "@/components/Reveal";
import StatsStrip from "@/components/StatsStrip";
import AttentionBanner from "@/components/AttentionBanner";
import Expertise from "@/components/Expertise";
import Process from "@/components/Process";
import GoogleReviews from "@/components/GoogleReviews";
import Faq from "@/components/Faq";
import QuoteForm from "@/components/QuoteForm";
import FloatingActions from "@/components/FloatingActions";
import NoInsuranceBanner from "@/components/NoInsuranceBanner";
import Footer from "@/components/Footer";
import { FAQS } from "@/lib/content";

// FAQPage structured data — makes the FAQ eligible for Google rich results.
// Generated from the same FAQS array the Faq component renders, so it never drifts.
const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: FAQS.map(({ q, a }) => ({
    "@type": "Question",
    name: q,
    acceptedAnswer: { "@type": "Answer", text: a },
  })),
};

// Single conversion-focused landing page — no site header or footer.
// Styled after gardewilson.com.au: black + gold, heavy condensed headlines.
// Desktop: each major section ends with its own CTA.
// All screens: a floating bottom-right widget (Call Us / Contact Us) stays visible.
//
// NOTE: LogoBar ("as featured in"), VideoTestimonials, CaseStudies and Trustpilot were removed
// pending REAL content (their files remain in /components for later). Reviews use Kushagra's
// GoogleReviews component (live Trustindex Google-reviews widget). The Portfolio "snapshot of
// outcomes" section was removed 2026-06-23 — publicizing client outcomes breaches Law Society
// of Ontario paralegal advertising rules (client request).
export default function Home() {
  return (
    <main>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />
      <Hero />
      <StatsStrip />
      <Reveal><AttentionBanner /></Reveal>
      <Expertise />
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
