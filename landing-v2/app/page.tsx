import dynamic from "next/dynamic";
import Hero from "@/components/Hero";
import Reveal from "@/components/Reveal";
import StatsStrip from "@/components/StatsStrip";
import AttentionBanner from "@/components/AttentionBanner";

// Below-fold: code-split so their JS doesn't block the hero paint.
const Expertise = dynamic(() => import("@/components/Expertise"));
const Process = dynamic(() => import("@/components/Process"));
const Portfolio = dynamic(() => import("@/components/Portfolio"));
const GoogleReviews = dynamic(() => import("@/components/GoogleReviews"));
const Faq = dynamic(() => import("@/components/Faq"));
const QuoteForm = dynamic(() => import("@/components/QuoteForm"));
const FloatingActions = dynamic(() => import("@/components/FloatingActions"));
const NoInsuranceBanner = dynamic(() => import("@/components/NoInsuranceBanner"));

// Single conversion-focused landing page — no site header or footer.
// Styled after gardewilson.com.au: black + gold, heavy condensed headlines.
// Desktop: each major section ends with its own CTA.
// All screens: a floating bottom-right widget (Call Us / Contact Us) stays visible.
//
// NOTE: LogoBar ("as featured in"), VideoTestimonials, CaseStudies and Trustpilot were removed
// pending REAL content (their files remain in /components for later). Reviews use Kushagra's
// GoogleReviews component (live Trustindex Google-reviews widget). ⚠️ Portfolio data in
// lib/content.ts is still placeholder and must be swapped for genuine outcomes before go-live.
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
      <Reveal><GoogleReviews /></Reveal>
      <Reveal><Faq /></Reveal>
      <Reveal><QuoteForm /></Reveal>
      <FloatingActions />
    </main>
  );
}
