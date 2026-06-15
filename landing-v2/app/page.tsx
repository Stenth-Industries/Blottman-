import Hero from "@/components/Hero";
import Reveal from "@/components/Reveal";
import StatsStrip from "@/components/StatsStrip";
import LogoBar from "@/components/LogoBar";
import AttentionBanner from "@/components/AttentionBanner";
import Expertise from "@/components/Expertise";
import Process from "@/components/Process";
import VideoTestimonials from "@/components/VideoTestimonials";
import Portfolio from "@/components/Portfolio";
import CaseStudies from "@/components/CaseStudies";
import Trustpilot from "@/components/Trustpilot";
import WrittenTestimonials from "@/components/WrittenTestimonials";
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
      <Reveal><Process /></Reveal>
      <Reveal><VideoTestimonials /></Reveal>
      <Reveal><Portfolio /></Reveal>
      <Reveal><CaseStudies /></Reveal>
      <Reveal><Trustpilot /></Reveal>
      <Reveal><WrittenTestimonials /></Reveal>
      <Reveal><Faq /></Reveal>
      <Reveal><QuoteForm /></Reveal>
      <StickyCta />
    </main>
  );
}
