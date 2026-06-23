import type { Metadata } from "next";
import Link from "next/link";
import Footer from "@/components/Footer";
import { BUSINESS_NAME, CONTACT_EMAIL, PHONE_DISPLAY, PHONE_TEL } from "@/lib/content";

export const metadata: Metadata = {
  title: `Privacy Policy | ${BUSINESS_NAME}`,
  description: `How ${BUSINESS_NAME} collects, uses, and protects the information you provide through our website.`,
  robots: { index: true, follow: true },
  alternates: { canonical: "/privacy" },
};

// Last reviewed date shown on the policy. Update when the policy text changes.
const LAST_UPDATED = "June 23, 2026";

// Standalone privacy policy. Required because the landing page collects personal
// data (name/phone/email/ticket photo) and uses Google Ads/Analytics tracking —
// Google's destination policies expect a privacy policy on such a page.
export default function PrivacyPolicy() {
  return (
    <main className="bg-ink text-white">
      <div className="section py-16 sm:py-24">
        <Link href="/" className="eyebrow mb-8 hover:text-gold-sheen">← Back to home</Link>

        <h1 className="h-section text-white">
          Privacy <span className="text-gold-sheen">Policy</span>
        </h1>
        <p className="mt-4 text-[13px] uppercase tracking-widest text-white/40">Last updated {LAST_UPDATED}</p>

        <div className="mt-10 max-w-3xl space-y-8 text-[15px] leading-relaxed text-white/70">
          <p>
            {BUSINESS_NAME} (&quot;we,&quot; &quot;us,&quot; or &quot;our&quot;) provides traffic-ticket defence
            services in Ontario, Canada. This policy explains what information we collect through this website,
            how we use it, and the choices you have. By using this site or submitting our form, you agree to
            this policy.
          </p>

          <Section title="Information we collect">
            <p>When you submit our free case review form, we collect the information you provide, which may include:</p>
            <ul className="mt-3 list-disc space-y-1.5 pl-5">
              <li>Your name, phone number, and email address;</li>
              <li>Details about your charge or ticket, and any message you send us.</li>
            </ul>
            <p className="mt-3">
              We also automatically receive limited technical information through advertising and analytics tools,
              including a Google click identifier (gclid) and cookie data, so we can understand how visitors reach
              our site and measure the performance of our ads.
            </p>
          </Section>

          <Section title="How we use your information">
            <p>We use the information you provide solely to:</p>
            <ul className="mt-3 list-disc space-y-1.5 pl-5">
              <li>Respond to your inquiry and provide your free case review;</li>
              <li>Contact you about your traffic-ticket matter; and</li>
              <li>Operate, maintain, and improve our website and advertising.</li>
            </ul>
          </Section>

          <Section title="We do not sell or share your information">
            <p>
              We do <strong className="text-white">not</strong> sell, rent, or trade your personal information,
              and we do not share it with third parties for their own marketing purposes. Your information is used
              only by {BUSINESS_NAME} to respond to you. We rely on standard, reputable service providers (such as
              Google) purely to receive form submissions, send our replies, and measure our advertising — never to
              market to you on their behalf.
            </p>
          </Section>

          <Section title="Cookies & advertising">
            <p>
              This site uses Google Ads and related tags to measure conversions and improve our advertising. These
              tools may set cookies in your browser. You can control or delete cookies through your browser settings,
              and you can opt out of personalized Google advertising at{" "}
              <a href="https://adssettings.google.com" className="text-gold hover:text-gold-sheen" target="_blank" rel="noopener noreferrer">
                adssettings.google.com
              </a>
              .
            </p>
          </Section>

          <Section title="How long we keep it">
            <p>
              We retain the information you submit only as long as needed to respond to your inquiry and provide our
              services, after which it is deleted or kept only as required by law or professional obligations.
            </p>
          </Section>

          <Section title="Your choices">
            <p>
              You may request access to, correction of, or deletion of the personal information you have given us at
              any time by contacting us using the details below. You may also ask us not to contact you further.
            </p>
          </Section>

          <Section title="Contact us">
            <p>For any questions about this policy or your information:</p>
            <p className="mt-3 text-white/90">
              {BUSINESS_NAME}<br />
              <a href={`mailto:${CONTACT_EMAIL}`} className="text-gold hover:text-gold-sheen">{CONTACT_EMAIL}</a>
              <br />
              <a href={`tel:${PHONE_TEL}`} className="text-gold hover:text-gold-sheen">{PHONE_DISPLAY}</a>
            </p>
          </Section>
        </div>
      </div>
      <Footer />
    </main>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="font-display text-2xl uppercase tracking-tight text-white">{title}</h2>
      <div className="mt-3">{children}</div>
    </section>
  );
}
