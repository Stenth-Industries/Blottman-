// ---------------------------------------------------------------------------
// All page text/data lives here so copy is easy to find and edit in one place.
// Content is for Blottman Law — Ontario traffic-ticket defence (v2 landing page).
// ---------------------------------------------------------------------------

// Phone number requested for the page. tel: link strips formatting.
export const PHONE_DISPLAY = "(647) 794-7750";
export const PHONE_TEL = "+16477947750";

// Trust widget numbers (placeholder Trustpilot data).
export const TRUSTPILOT = {
  rating: 4.7,
  reviews: 67,
};

// Logo bar — businesses / outlets we've worked with (placeholders for now).
export const BRAND_LOGOS = [
  "Globe Daily",
  "City Press",
  "Auto Club",
  "Driver Co.",
  "Fleet Group",
  "North Media",
  "Civic Times",
  "Road Watch",
  "Metro News",
];

// Bullet-point benefits (skim-friendly, minimal copy).
export const BENEFITS = [
  "Most clients never set foot in court",
  "Fixed, upfront pricing - no surprises",
  "We work to protect your record and insurance rates",
  "Licensed Ontario paralegal, 500+ tickets handled",
];

// What we fight — numbered practice-area grid (Garde Wilson "Expertise" pattern).
export const EXPERTISE: { title: string; blurb: string; image?: string; imageOpacity?: number }[] = [
  { title: "Speeding & Stunt Driving", blurb: "Built to protect your licence, record, and insurance rates when the stakes are high.", image: "/offence-speeding.png", imageOpacity: 0.8 },
  { title: "Careless Driving", blurb: "A serious charge with up to 6 points. We fight to have it reduced or withdrawn.", image: "/offence-careless.png", imageOpacity: 0.55 },
  { title: "Distracted / Cell Phone", blurb: "Big fines and points for one tap. Often beatable, especially first offence.", image: "/offence-distracted.png", imageOpacity: 0.5 },
  { title: "Suspended Licence", blurb: "Driving while suspended carries heavy penalties. We protect your record.", image: "/offence-suspended.png", imageOpacity: 0.2 },
  { title: "Demerit Points & Insurance", blurb: "Convictions follow you for years. We keep your abstract — and your rates — clean.", image: "/offence-demerit.png", imageOpacity: 0.2 },
  { title: "Fail to Stop / Remain", blurb: "From stop signs to collisions, we build the defence the charge calls for.", image: "/offence-fail-stop.png", imageOpacity: 0.18 },
];

// How it works — numbered step process (Garde Wilson "What happens" pattern).
export const PROCESS = [
  { step: "01", title: "Send Us Your Ticket", body: "Snap a photo of your ticket and send it over. It takes two minutes and costs nothing." },
  { step: "02", title: "Free Case Review", body: "We review the charge, the evidence, and your options — then call you with an honest read." },
  { step: "03", title: "We Fight It For You", body: "As your licensed paralegal we handle the paperwork and attend court on your behalf." },
  { step: "04", title: "Keep Your Record", body: "Our goal: the charge reduced or withdrawn, your licence intact, your insurance unaffected." },
];

// 9 written testimonials (3x3 grid). Placeholder names + dates (review-card style).
export const WRITTEN_TESTIMONIALS = [
  { name: "Daniel R.", location: "Toronto", date: "March 2026", quote: "Charge withdrawn. I never had to take a day off work to appear." },
  { name: "Priya S.", location: "Mississauga", date: "March 2026", quote: "Two demerit points avoided. My insurance didn't move an inch." },
  { name: "Marc L.", location: "Brampton", date: "February 2026", quote: "Stunt-driving charge reduced. Clear, fast, no jargon." },
  { name: "Aisha K.", location: "Hamilton", date: "February 2026", quote: "They handled everything by email. Speeding ticket dropped." },
  { name: "Tom V.", location: "Vaughan", date: "January 2026", quote: "Saved my licence. Worth every dollar and then some." },
  { name: "Grace W.", location: "Markham", date: "January 2026", quote: "Honest about my odds from the first call. No pressure." },
  { name: "Sven N.", location: "Scarborough", date: "December 2025", quote: "Careless-driving charge beaten. Could not be happier." },
  { name: "Owen B.", location: "Etobicoke", date: "December 2025", quote: "Quick response, fair price, great result on my cell-phone ticket." },
  { name: "Lena M.", location: "North York", date: "November 2025", quote: "Professional start to finish. Kept my clean record intact." },
];

// 9 video testimonials (3x3 grid) — placeholders until real footage arrives.
export const VIDEO_TESTIMONIALS = Array.from({ length: 9 }, (_, i) => ({
  id: i + 1,
  name: `Client ${i + 1}`,
  caption: "Video testimonial coming soon",
}));

// Portfolio / recent results gallery (placeholders).
export const PORTFOLIO = [
  { title: "Speeding 140 in a 100", result: "Withdrawn", tag: "Highway 401" },
  { title: "Stunt driving (50+ over)", result: "Reduced to minor", tag: "Licence saved" },
  { title: "Careless driving", result: "Dismissed at trial", tag: "6 points avoided" },
  { title: "Distracted / cell phone", result: "Withdrawn", tag: "First offence" },
  { title: "Suspended licence", result: "Reduced charge", tag: "Kept driving" },
  { title: "Fail to stop", result: "Withdrawn", tag: "No conviction" },
];

// 2 before/after case studies.
export const CASE_STUDIES = [
  {
    title: "From licence suspension to back on the road",
    before: {
      label: "Before",
      points: ["Stunt-driving charge (50+ km/h over)", "Facing 7-day roadside suspension + 6 demerit points", "Insurance renewal at risk"],
    },
    after: {
      label: "After",
      points: ["Charge reduced to a minor speeding offence", "Zero demerit points recorded", "Licence kept — no insurance increase"],
    },
  },
  {
    title: "From a record-ending charge to a clean abstract",
    before: {
      label: "Before",
      points: ["Careless driving after a collision", "Risk of conviction on permanent record", "Court date scheduled, client unable to attend"],
    },
    after: {
      label: "After",
      points: ["Charge dismissed at trial", "We attended court — client never appeared", "Driving record stayed clean"],
    },
  },
];

// FAQ — the biggest objection handles for traffic-ticket defence.
export const FAQS = [
  {
    q: "Is it even worth fighting my ticket?",
    a: "Almost always. Paying a ticket is a guilty plea — it adds demerit points and can raise your insurance for years. We often get charges reduced or withdrawn for less than the long-term cost of paying.",
  },
  {
    q: "Do I have to go to court?",
    a: "In most cases, no. As your licensed paralegal we attend court on your behalf. Most clients never appear.",
  },
  {
    q: "How much does it cost?",
    a: "Fixed, upfront pricing quoted before we start — no hourly surprises. Most clients save more on insurance than the fee itself.",
  },
  {
    q: "Will this raise my insurance?",
    a: "That's exactly what we work to prevent. A conviction is what your insurer sees — getting the charge reduced or withdrawn protects your rate.",
  },
  {
    q: "What are my actual chances?",
    a: "We give you an honest read on your first call — no false promises. If we don't think we can help, we'll tell you.",
  },
  {
    q: "How fast can you help?",
    a: "Send us your ticket today and we'll review it and call you back. The sooner we start, the more options you have.",
  },
];
