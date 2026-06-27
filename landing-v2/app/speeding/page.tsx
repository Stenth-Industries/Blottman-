import type { Metadata } from "next";
import TicketLanding from "@/components/TicketLanding";
import { TICKET_PAGES } from "@/lib/content";

// /speeding — keyword-matched SKAG landing page (template for the other ticket
// types). Point the "speeding ticket" SKAG's final URL here.
const page = TICKET_PAGES.speeding;

export const metadata: Metadata = {
  title: page.metaTitle,
  description: page.metaDescription,
  alternates: { canonical: `/${page.slug}` },
  openGraph: {
    type: "website",
    url: `/${page.slug}`,
    siteName: "Blottman Legal Services",
    title: page.metaTitle,
    description: page.metaDescription,
    locale: "en_CA",
    images: [{ url: "/logo.png", alt: "Blottman Legal Services" }],
  },
};

export default function SpeedingPage() {
  return <TicketLanding page={page} />;
}
