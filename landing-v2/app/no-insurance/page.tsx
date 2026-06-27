import type { Metadata } from "next";
import TicketLanding from "@/components/TicketLanding";
import { TICKET_PAGES } from "@/lib/content";

// /no-insurance — keyword-matched SKAG landing page. Point the no-insurance
// SKAG's final URL here.
const page = TICKET_PAGES["no-insurance"];

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

export default function NoInsurancePage() {
  return <TicketLanding page={page} />;
}
