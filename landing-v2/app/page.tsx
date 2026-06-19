import Hero from "@/components/Hero";
import Reveal from "@/components/Reveal";
import StatsStrip from "@/components/StatsStrip";
import AttentionBanner from "@/components/AttentionBanner";
import Expertise from "@/components/Expertise";
import Process from "@/components/Process";
import Portfolio from "@/components/Portfolio";
import WrittenTestimonials from "@/components/WrittenTestimonials";
import Faq from "@/components/Faq";
import QuoteForm from "@/components/QuoteForm";
import FloatingActions from "@/components/FloatingActions";
import NoInsuranceBanner from "@/components/NoInsuranceBanner";

// Single conversion-focused landing page — no site header or footer.
// Styled after gardewilson.com.au: black + gold, heavy condensed headlines.
// Desktop: each major section ends with its own CTA.
// All screens: a floating bottom-right widget (Call Us / Contact Us) stays visible.
//
// NOTE: LogoBar ("as featured in"), VideoTestimonials, CaseStudies and Trustpilot were removed
// pending REAL content (their files remain in /components for later). Portfolio + WrittenTestimonials
// are rendered again at the client's request — ⚠️ their data in lib/content.ts is still placeholder
// and must be swapped for genuine, accurate results/reviews before this page goes live.
export default function Home() {
  return (
    <main>
      <Hero />
      <StatsStrip />
      <Reveal><AttentionBanner /></Reveal>
      <Expertise />
      <Reveal><NoInsuranceBanner /></Reveal>
      <Reveal><Process /></Reveal>
      <Reveal><Portfolio /></Reveal>
      <Reveal><WrittenTestimonials /></Reveal>
      <Reveal><Faq /></Reveal>
      <Reveal><QuoteForm /></Reveal>
      <FloatingActions />
    </main>
  );
}
