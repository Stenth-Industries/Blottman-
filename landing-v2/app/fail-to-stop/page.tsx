import type { Metadata } from "next";
import TicketLanding from "@/components/TicketLanding";
import { TICKET_PAGES } from "@/lib/content";

// /fail-to-stop — keyword-matched SKAG landing page. Point the fail-to-stop
// SKAG's final URL here.
const page = TICKET_PAGES["fail-to-stop"];

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

export default function FailToStopPage() {
  return <TicketLanding page={page} />;
}
