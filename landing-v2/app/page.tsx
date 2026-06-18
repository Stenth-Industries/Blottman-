import Hero from "@/components/Hero";
import Reveal from "@/components/Reveal";
import StatsStrip from "@/components/StatsStrip";
import LogoBar from "@/components/LogoBar";
import AttentionBanner from "@/components/AttentionBanner";
import Expertise from "@/components/Expertise";
import ClaritySection from "@/components/ClaritySection";
import Portfolio from "@/components/Portfolio";
import CaseStudies from "@/components/CaseStudies";
import GoogleReviews from "@/components/GoogleReviews";
import Faq from "@/components/Faq";
import QuoteForm from "@/components/QuoteForm";
import StickyCta from "@/components/StickyCta";

// Single conversion-focused landing page — no site header or footer.
// Styled after gardewilson.com.au: black + gold, heavy condensed headlines.
// Desktop: each major section ends with its own CTA.
// Mobile: one fixed CTA pinned to the bottom (StickyCta).
export default function Home() {
  return (
    <main>
      <Hero />
      <StatsStrip />
      <Reveal><LogoBar /></Reveal>
      <Reveal><AttentionBanner /></Reveal>
      <Expertise />
      <Reveal><ClaritySection /></Reveal>
      <Reveal><Portfolio /></Reveal>
      <Reveal><CaseStudies /></Reveal>
      <Reveal><GoogleReviews /></Reveal>
      <Reveal><Faq /></Reveal>
      <Reveal><QuoteForm /></Reveal>
      <StickyCta />
    </main>
  );
}
