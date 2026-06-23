import type { Metadata, Viewport } from "next";
import { Anton, Poppins } from "next/font/google";
import Script from "next/script";
import MotionProvider from "@/components/MotionProvider";
import { PHONE_TEL, PHONE_DISPLAY, GOOGLE_RATING } from "@/lib/content";
import "./globals.css";

const SITE_URL = "https://blottman.ca";
const SITE_TITLE = "Fight Your Traffic Ticket | Blottman Law — Ontario";
const SITE_DESCRIPTION =
  "Licensed Ontario paralegal. We fight speeding, careless, stunt-driving and other traffic tickets to protect your record and insurance. Free case review.";

// LegalService structured data — local-SEO signal (name, phone, area served,
// service type) rendered on every page so Google can identify the business.
const businessJsonLd = {
  "@context": "https://schema.org",
  "@type": "LegalService",
  name: "Blottman Law",
  description: SITE_DESCRIPTION,
  url: SITE_URL,
  telephone: PHONE_TEL,
  priceRange: "$$",
  areaServed: { "@type": "AdministrativeArea", name: "Ontario, Canada" },
  address: { "@type": "PostalAddress", addressRegion: "ON", addressCountry: "CA" },
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: GOOGLE_RATING.rating,
    reviewCount: GOOGLE_RATING.reviews,
  },
};

// Anton ≈ the heavy condensed "Thunder" display face used on gardewilson.com.au
const anton = Anton({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-anton",
  display: "swap",
});

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-poppins",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: SITE_TITLE,
  description: SITE_DESCRIPTION,
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url: SITE_URL,
    siteName: "Blottman Law",
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    locale: "en_CA",
    images: [{ url: "/logo.png", alt: "Blottman Law" }],
  },
  twitter: {
    card: "summary_large_image",
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    images: ["/logo.png"],
  },
};

// Match the mobile browser chrome to the black theme (no white flash on load).
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#0c0c0c",
};

// Google tag (gtag.js) — loads only when NEXT_PUBLIC_GADS_ID is set, so dev/
// preview stay clean. Needed for the QuoteForm's Google Ads conversion to fire.
const GADS_ID = process.env.NEXT_PUBLIC_GADS_ID;
// "Calls From Website" number-swap label (AW-…/label). When set, gtag replaces
// the displayed PHONE_DISPLAY with a Google forwarding number for ad visitors so
// website calls ≥60s are tracked as conversions. Office line still rings normally.
const GADS_CALL_CONVERSION = process.env.NEXT_PUBLIC_GADS_CALL_CONVERSION;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${anton.variable} ${poppins.variable}`}>
      <body className="font-sans">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(businessJsonLd) }}
        />
        <MotionProvider>{children}</MotionProvider>
        {GADS_ID && (
          <>
            <Script src={`https://www.googletagmanager.com/gtag/js?id=${GADS_ID}`} strategy="afterInteractive" />
            <Script id="gtag-init" strategy="afterInteractive">
              {`window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', '${GADS_ID}');${
                GADS_CALL_CONVERSION
                  ? `\ngtag('config', '${GADS_CALL_CONVERSION}', { 'phone_conversion_number': '${PHONE_DISPLAY}' });`
                  : ""
              }`}
            </Script>
          </>
        )}
      </body>
    </html>
  );
}
