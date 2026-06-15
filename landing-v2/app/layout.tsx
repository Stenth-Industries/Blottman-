import type { Metadata } from "next";
import { Anton, Poppins } from "next/font/google";
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

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${anton.variable} ${poppins.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
