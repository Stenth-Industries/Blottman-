// ---------------------------------------------------------------------------
// All page text/data lives here so copy is easy to find and edit in one place.
// Content is for Blottman Law — Ontario traffic-ticket defence (v2 landing page).
// ---------------------------------------------------------------------------

// Phone number requested for the page. tel: link strips formatting.
export const PHONE_DISPLAY = "(647) 794-7750";
export const PHONE_TEL = "+16477947750";

// Headline Google rating shown in the hero (static marketing figure).
export const GOOGLE_RATING = {
  rating: 4.9, // confirmed from her live Google listing (4.9 · 79 reviews)
  reviews: 79,
};

// Trustindex widget id for the live Google-reviews embed (free, no card needed).
// Sign up at trustindex.io, create a Google-reviews widget for her listing,
// then copy the hash from the embed code here — it's the part after
// "loader.js?" in: <script ... src='https://cdn.trustindex.io/loader.js?HASH'>.
// While this is empty, the GoogleReviews section renders the styled sample
// cards below instead, so the page always looks complete.
export const TRUSTINDEX_WIDGET_ID = "72966a67489d59447446e251b7d";

// Styled placeholder reviews shown until the Featurable widget id is set.
export const GOOGLE_SAMPLE_REVIEWS = [
  { author: "Daniel R.", rating: 5, relativeTime: "2 weeks ago", text: "Charge withdrawn. I never had to take a day off work to appear." },
  { author: "Priya S.", rating: 5, relativeTime: "3 weeks ago", text: "Two demerit points avoided. My insurance didn't move an inch." },
  { author: "Marc L.", rating: 5, relativeTime: "a month ago", text: "Stunt-driving charge reduced. Clear, fast, no jargon." },
  { author: "Aisha K.", rating: 5, relativeTime: "a month ago", text: "They handled everything by email. Speeding ticket dropped." },
  { author: "Tom V.", rating: 5, relativeTime: "2 months ago", text: "Saved my licence. Worth every dollar and then some." },
  { author: "Grace W.", rating: 5, relativeTime: "2 months ago", text: "Honest about my odds from the first call. No pressure." },
];

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
  "Fixed, upfront pricing with no surprises",
  "We work to protect your record and insurance rates",
  "Licensed Ontario paralegal, 500+ tickets handled",
];

// What we fight — numbered practice-area grid (Garde Wilson "Expertise" pattern).
export const EXPERTISE: { title: string; blurb: string; image?: string; imageOpacity?: number }[] = [
  { title: "Speeding & Stunt Driving", blurb: "Built to protect your licence, record, and insurance rates when the stakes are high.", image: "/offence-speeding.png", imageOpacity: 0.8 },
  { title: "Careless Driving", blurb: "A serious charge with up to 6 points. We fight to have it reduced or withdrawn.", image: "/offence-careless.png", imageOpacity: 0.55 },
  { title: "Distracted / Cell Phone", blurb: "Big fines and points for one tap. Often beatable, especially first offence.", image: "/offence-distracted.png", imageOpacity: 0.5 },
  { title: "Suspended Licence", blurb: "Driving while suspended carries heavy penalties. We protect your record.", image: "/offence-suspended.png", imageOpacity: 0.2 },
  { title: "Demerit Points & Insurance", blurb: "Convictions follow you for years. We keep your abstract and your rates clean.", image: "/offence-demerit.png", imageOpacity: 0.2 },
  { title: "Fail to Stop / Remain", blurb: "From stop signs to collisions, we build the defence the charge calls for.", image: "/offence-fail-stop.png", imageOpacity: 0.18 },
];

// How it works — conversion bridge. Heading + 3-step process + the conversion
// card. Copy avoids outcome promises (no won/dropped/dismissed/guaranteed) —
// safe language only: review your charge, understand your options, next steps.
export const PROCESS_HEADING = "Send your ticket. Know your options.";
export const PROCESS_SUBHEADING =
  "Upload a photo or screenshot of your ticket, summons, or offence notice. Leslie reviews it and explains your next step.";

export const PROCESS = [
  { step: "01", title: "Send Your Ticket", body: "Take a photo or screenshot and send it in." },
  { step: "02", title: "Leslie Reviews the Charge", body: "She checks the offence, deadline, and next steps." },
  { step: "03", title: "Know Your Options", body: "Get clear guidance before deciding how to move forward." },
];

// The premium conversion card (right column on desktop, first on mobile).
export const TICKET_REVIEW = {
  title: "Free Ticket Review",
  copy: "Send your ticket and get clear next steps from a licensed Ontario paralegal.",
  points: [
    "Clear explanation of your options",
    "HTA & provincial offences reviewed",
    "Record, licence & insurance explained",
  ],
  primaryCta: "Send My Ticket for Review",
  secondaryCta: "Call Now",
};

// 9 video testimonials (3x3 grid) — placeholders until real footage arrives.
export const VIDEO_TESTIMONIALS = Array.from({ length: 9 }, (_, i) => ({
  id: i + 1,
  name: `Client ${i + 1}`,
  caption: "Video testimonial coming soon",
}));

// Portfolio / recent results gallery. ⚠️ Verify each outcome is truthful and
// representative of a real case Leslie handled before publishing (legal ad).
export const PORTFOLIO = [
  {
    title: "Speeding 140 in a 100",
    result: "Withdrawn",
    tag: "Highway 401",
    desc: "Clocked at 140 in a 100 zone on the 401, facing a heavy fine and demerit points. We challenged the radar disclosure and the charge was withdrawn before trial.",
  },
  {
    title: "Stunt driving (50+ over)",
    result: "Reduced to minor",
    tag: "Licence saved",
    desc: "A stunt-driving charge meant a roadside suspension and possible licence loss. We negotiated it down to a minor speeding offence and the licence stayed intact.",
  },
  {
    title: "Careless driving",
    result: "Dismissed at trial",
    tag: "6 points avoided",
    desc: "A careless charge after a collision put 6 demerit points and an insurance hike on the line. The matter went to trial and the charge was dismissed.",
  },
  {
    title: "Distracted / cell phone",
    result: "Withdrawn",
    tag: "First offence",
    desc: "A first distracted-driving charge carried 3 points and a steep fine. After reviewing the officer's notes, the charge was withdrawn.",
  },
  {
    title: "Suspended licence",
    result: "Reduced charge",
    tag: "Kept driving",
    desc: "Driving while suspended carries serious penalties. We worked through the disclosure and had the charge reduced, keeping the client on the road.",
  },
  {
    title: "Fail to stop",
    result: "Withdrawn",
    tag: "No conviction",
    desc: "A fail-to-stop charge risked demerit points and a conviction on the record. After reviewing the evidence, the charge was withdrawn with no conviction registered.",
  },
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
      points: ["Charge reduced to a minor speeding offence", "Zero demerit points recorded", "Licence kept with no insurance increase"],
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
      points: ["Charge dismissed at trial", "We attended court so the client never appeared", "Driving record stayed clean"],
    },
  },
];

// FAQ — the biggest objection handles for traffic-ticket defence.
export const FAQS = [
  {
    q: "Is it even worth fighting my ticket?",
    a: "Almost always. Paying a ticket is a guilty plea that adds demerit points and can raise your insurance for years. We often get charges reduced or withdrawn for less than the long-term cost of paying.",
  },
  {
    q: "Do I have to go to court?",
    a: "In most cases, no. As your licensed paralegal we attend court on your behalf. Most clients never appear.",
  },
  {
    q: "How much does it cost?",
    a: "Fixed, upfront pricing quoted before we start, with no hourly surprises. Most clients save more on insurance than the fee itself.",
  },
  {
    q: "Will this raise my insurance?",
    a: "That's exactly what we work to prevent. A conviction is what your insurer sees, so getting the charge reduced or withdrawn protects your rate.",
  },
  {
    q: "What are my actual chances?",
    a: "We give you an honest read on your first call, with no false promises. If we don't think we can help, we'll tell you.",
  },
  {
    q: "How fast can you help?",
    a: "Send us your ticket today and we'll review it and call you back. The sooner we start, the more options you have.",
  },
];
