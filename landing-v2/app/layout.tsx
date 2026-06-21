import type { Metadata, Viewport } from "next";
import { Anton, Poppins } from "next/font/google";
import Script from "next/script";
import "./globals.css";

// Anton ≈ the heavy condensed "Thunder" display face used on gardewilson.com.au
const anton = Anton({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-anton",
  display: "swap",
});

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-poppins",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Fight Your Traffic Ticket | Blottman Law — Ontario",
  description:
    "Licensed Ontario paralegal. We fight speeding, careless, stunt-driving and other traffic tickets to protect your record and insurance. Free case review.",
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

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${anton.variable} ${poppins.variable}`}>
      <body className="font-sans">
        {children}
        {GADS_ID && (
          <>
            <Script src={`https://www.googletagmanager.com/gtag/js?id=${GADS_ID}`} strategy="afterInteractive" />
            <Script id="gtag-init" strategy="afterInteractive">
              {`window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', '${GADS_ID}');`}
            </Script>
          </>
        )}
      </body>
    </html>
  );
}
