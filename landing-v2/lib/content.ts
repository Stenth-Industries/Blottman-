// ---------------------------------------------------------------------------
// All page text/data lives here so copy is easy to find and edit in one place.
// Content is for Blottman Law — Ontario traffic-ticket defence (v2 landing page).
// ---------------------------------------------------------------------------

// Phone number requested for the page. tel: link strips formatting.
export const PHONE_DISPLAY = "(647) 794-7750";
export const PHONE_TEL = "+16477947750";

// Business identity — used in the footer, privacy policy, and legal copy.
export const BUSINESS_NAME = "Blottman Legal Services";
export const CONTACT_EMAIL = "legal@blottman.com";

// Trust widget numbers (placeholder Trustpilot data).
export const TRUSTPILOT = {
  rating: 4.7,
  reviews: 67,
};

// Headline Google rating shown in the GoogleReviews fallback (from her live listing).
// Verified 2026-06-22 from the live Google Business Profile feed (Trustindex): 4.9 / 81.
export const GOOGLE_RATING = {
  rating: 4.9,
  reviews: 81,
};

// Trustindex widget id for the live Google-reviews embed (free, no card needed).
// ⚠️ Left EMPTY on purpose: the live widget surfaces the newest Google entries, many
// of which are rating-only ("left a rating", no text) and look empty to visitors.
// We instead render the curated written reviews below so every card has real words.
// Put the widget id back here to re-enable the live embed.
export const TRUSTINDEX_WIDGET_ID = "72966a67489d59447446e251b7d";

// REAL verified written Google reviews from blottman.com. These are shown directly
// (not just as a fallback) so the section always displays reviews with actual words,
// not rating-only entries. Never show fabricated reviews to real visitors.
export const GOOGLE_SAMPLE_REVIEWS = [
  { author: "Anthony Sweeney", rating: 5, relativeTime: "Verified Google review", text: "I retained Blottman Law, represented by Leslie Rivas, for a hand-held device charge. On the first day of proceedings she had the ticket withdrawn — no demerit points, no suspension, nothing on my record, and over $200 saved versus the fine. She explained everything clearly and delivered excellent results. Strongly recommend." },
  { author: "Daniel Tran", rating: 5, relativeTime: "Verified Google review", text: "Leslie was outstanding. She got my careless driving withdrawn and amended my speeding ticket to disobey sign, which saved me from major demerit points. Great communication and very professional service. Highly recommend." },
  { author: "Emal S", rating: 5, relativeTime: "Verified Google review", text: "Amazing work — they reduced my stunt driving to just a speeding ticket with 0 demerit points. I recommend them if you are in a crazy situation like I was." },
  { author: "Al C", rating: 5, relativeTime: "Verified Google review", text: "Communication, professionalism, and RESULTS — three of the reasons why you should look no further than Blottman Legal Services for any traffic needs. My experience was phenomenal. Best service and results in the GTA. Thank you." },
  { author: "Eleane Reid", rating: 5, relativeTime: "Verified Google review", text: "Our family is eternally grateful for your legal team. The experience was seamless from beginning to end. Both my grandsons were handed bouquets of tickets and were able to get off with little or nothing. Thank you Leslie for all your hard work." },
  { author: "Ajeet Sahijwani", rating: 5, relativeTime: "Verified Google review", text: "Blottman Legal Services takes care of traffic tickets professionally. They resolved my fail-to-stop at a stop sign issue with zero points." },
  { author: "Spencer Hauser", rating: 5, relativeTime: "Verified Google review", text: "Leslie has helped me with multiple tickets and has always been great with communication and customer service skills!" },
  { author: "Joshua Alba", rating: 5, relativeTime: "Verified Google review", text: "Thank you for your excellent service. Your expertise, clear communication, and professionalism greatly eased a challenging process. I would highly recommend your services." },
  { author: "Tom Zhang", rating: 5, relativeTime: "Verified Google review", text: "The fee was very reasonable and the work was excellent. Thank you very much." },
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
  "Fixed, upfront pricing - no surprises",
  "We work to protect your record and insurance rates",
  "Licensed Ontario paralegal, 500+ tickets handled",
];

// ---------------------------------------------------------------------------
// Per-ticket SKAG landing pages. Each entry is one keyword-matched page (e.g.
// /speeding) that reuses the shared sections but swaps the hero headline + the
// intro copy so the page mirrors the search term (SKAG message-match). To ship
// a new page: add an entry here + a 3-line route at app/<slug>/page.tsx.
// ---------------------------------------------------------------------------
export type TicketPage = {
  slug: string;
  metaTitle: string;
  metaDescription: string;
  eyebrow: string;        // hero eyebrow label
  titleLine1: string;     // hero H1, line 1 (carries the matched keyword)
  titleLine2: string;     // hero H1, line 2 lead-in
  titleHighlight: string; // hero H1, gold emphasis word
  benefits: string[];     // hero skim bullets
  introEyebrow: string;
  introHeading: string;
  introBody: string;
};

export const TICKET_PAGES: Record<string, TicketPage> = {
  speeding: {
    slug: "speeding",
    metaTitle: "Fight Your Speeding Ticket | Blottman Legal Services — Ontario",
    metaDescription:
      "Charged with speeding in Ontario? A licensed paralegal fights your speeding ticket — protecting your record, demerit points and insurance. Free case review.",
    eyebrow: "Ontario Speeding-Ticket Defence",
    titleLine1: "Fight your speeding ticket.",
    titleLine2: "Protect your",
    titleHighlight: "record.",
    benefits: [
      "Fight the demerit points a speeding conviction adds",
      "Most clients never set foot in court",
      "We work to protect your record and insurance rates",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Speeding Tickets",
    introHeading: "Charged with speeding in Ontario?",
    introBody:
      "A speeding ticket is more than a fine. A conviction adds demerit points, stays on your record, and can raise your insurance for years — and the higher the alleged speed, the steeper the penalty. We review the officer's evidence, the radar or lidar reliability, and the disclosure for the weaknesses that help us fight your speeding charge. In most cases, you never have to set foot in court.",
  },
};

// What we fight — practice-area grid mirroring blottman.com's "Trusted Legal
// Experts" cards (same 9 charges + wording). Source copy says "our lawyers";
// kept paralegal-accurate here ("we"/"our team") since Leslie is a licensed
// Ontario paralegal. Order/wording follow the existing site per client request.
export const EXPERTISE: { title: string; blurb: string; image: string }[] = [
  { title: "Driving Under Suspension", blurb: "Protect your licence, avoid costly fines, and regain control — our suspension defence works to keep your record clean and your future secure.", image: "/result-suspended.jpg" },
  { title: "Driving With No Experience", blurb: "Don't let inexperience cost you — we work to minimize penalties, protect your record, and fight for your driving freedom.", image: "/inexperienced-driver-lhd.png" },
  { title: "Failure To Stop", blurb: "One mistake shouldn't wreck your record — our team fights tickets, reduces penalties, and helps you keep your insurance rates low.", image: "/result-failstop.jpg" },
  { title: "Unsafe Turn", blurb: "We challenge unsafe turn charges head-on — fighting points, safeguarding your licence, and protecting you from years of higher insurance premiums.", image: "/unsafe-turn-real.png" },
  { title: "Stunt Driving", blurb: "Serious charge? We defend aggressively — challenging licence suspensions, steep fines, and criminal records to protect your freedom and driving future.", image: "/result-stunt.jpg" },
  { title: "Careless Driving", blurb: "We fight careless driving charges — working to reduce fines, avoid demerit points, and protect your driving record with a strong, persuasive defence.", image: "/result-careless.jpg" },
  { title: "Speeding Ticket", blurb: "Beat your speeding ticket — our defence works to reduce fines, fight licence points, and save you money by keeping insurance rates low.", image: "/result-speeding.jpg" },
  { title: "Cell Phone Ticket", blurb: "From minor infractions to serious tickets — we protect your licence, work to reduce penalties, and save you money long-term.", image: "/result-distracted.jpg" },
  { title: "Traffic Violations", blurb: "We fight traffic violations fiercely, working to minimize consequences, protect your record, and keep you on the road without penalties.", image: "/process-1-ticket.jpg" },
];

// How it works — numbered step process (Garde Wilson "What happens" pattern).
export const PROCESS = [
  { step: "01", title: "Send Us a Message", body: "Tell us what happened and send us a quick message. It takes two minutes and costs nothing.", image: "/process-1-ticket.jpg" },
  { step: "02", title: "Free Case Review", body: "We review the charge, the evidence, and your options — then call you with an honest read.", image: "/process-2-review.jpg" },
  { step: "03", title: "We Fight It For You", body: "As your licensed paralegal we handle the paperwork and attend court on your behalf.", image: "/process-3-court.png" },
  { step: "04", title: "Keep Your Record", body: "Our goal: protect your licence, your record, and your insurance rate every step of the way.", image: "/process-4-driving.jpg" },
];

// Real verified Google reviews, pulled from blottman.com (Trustindex Google widget).
// Source: https://blottman.com/ — keep verbatim; these are genuine client reviews.
export const WRITTEN_TESTIMONIALS = [
  {
    name: "Anthony Sweeney",
    quote:
      "I retained Blottman Law, represented by Leslie Rivas, for a Highway Traffic Act, s.78.1(1) – Driving with Hand-Held Communication Device charge. On the first day of proceedings, Ms. Rivas successfully had the ticket withdrawn. This meant no loss of demerit points, no licence suspension, nothing on my record, and over $200 saved compared to paying the fine, while also sparing me long-term insurance implications and added stress. Ms. Rivas explained the potential consequences clearly, guided me through the process with confidence, and delivered excellent results. I strongly recommend her and Blottman Law to anyone facing traffic charges in York Region or across Ontario.",
  },
  {
    name: "Daniel Tran",
    quote:
      "Leslie was outstanding. She got my careless driving withdrawn and amended my speeding ticket to disobey sign, which saved me from major demerit points. Great communication and very professional service. Highly recommend.",
  },
  {
    name: "Emal S",
    quote:
      "Amazing work — they reduced my stunt driving to just a speeding ticket with 0 demerit points. I recommend them if you are in a crazy situation like I was.",
  },
  {
    name: "Al C",
    quote:
      "Communication, professionalism, and RESULTS — three of the reasons why you should look no further than Blottman Legal Services for any traffic needs you might have. My experience was phenomenal. They provided me with the best possible outcome for my traffic infractions, and were upfront with me from the beginning. Best service and results in the GTA. THANK YOU.",
  },
  {
    name: "Eleane Reid",
    quote:
      "Our family is eternally grateful for your Legal Team. The experience was seamless from beginning to end. Both my grandsons were handed bouquets of tickets and were able to get off with little or nothing. Thank you Leslie for all your hard work. — The Reid Family",
  },
  {
    name: "Spencer Hauser",
    quote:
      "Leslie has helped me with multiple tickets and has always been great with communication and customer service skills!",
  },
  {
    name: "Ajeet Sahijwani",
    quote:
      "Blottman Legal Services takes care of traffic tickets professionally. They resolved my fail-to-stop at a stop sign issue with zero points.",
  },
  {
    name: "Joshua Alba",
    quote:
      "Thank you for your excellent service. Your expertise, clear communication, and professionalism greatly eased a challenging process. I truly appreciated your dedication and thoughtful guidance throughout. I would highly recommend your services.",
  },
  {
    name: "Tom Zhang",
    quote: "The fee was very reasonable and the work was excellent. Thank you very much.",
  },
];

// 9 video testimonials (3x3 grid) — placeholders until real footage arrives.
export const VIDEO_TESTIMONIALS = Array.from({ length: 9 }, (_, i) => ({
  id: i + 1,
  name: `Client ${i + 1}`,
  caption: "Video testimonial coming soon",
}));

// NOTE: the "Recent Results / snapshot of outcomes" PORTFOLIO section was removed
// (2026-06-23) at the client's request — publicizing specific client charges and
// outcomes breaches Law Society of Ontario paralegal advertising rules. Do NOT
// reintroduce per-client result cards. Genuine third-party Google reviews (below)
// are kept; firm-authored outcome claims are not.

// 2 before/after case studies (dormant — not rendered; kept for reference only).
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
    a: "Almost always. Paying a ticket is a guilty plea — it adds demerit points and can raise your insurance for years. We often resolve charges for less than the long-term cost of paying.",
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
    q: "Will a traffic ticket increase my insurance?",
    a: "Insurance consequences vary depending on the type of offence, your driving history, and your insurer. Before paying a ticket, it may be beneficial to understand the potential impact and explore your available options.",
  },
  {
    q: "What are my actual chances?",
    a: "We give you an honest read on your first call — no false promises. If we don't think we can help, we'll tell you.",
  },
  {
    q: "How fast can you help?",
    a: "Send us a message today and we'll review your charge and call you back. The sooner we start, the more options you have.",
  },
];
