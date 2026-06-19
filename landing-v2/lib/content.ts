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
  { title: "Speeding & Stunt Driving", blurb: "Built to protect your licence, record, and insurance rates when the stakes are high.", image: "/offence-speeding.png", imageOpacity: 0.9 },
  { title: "Careless Driving", blurb: "A serious charge with up to 6 points. We fight to have it reduced or withdrawn.", image: "/offence-careless.png", imageOpacity: 0.72 },
  { title: "Distracted / Cell Phone", blurb: "Big fines and points for one tap. Often beatable, especially first offence.", image: "/offence-distracted.png", imageOpacity: 0.68 },
  { title: "Suspended Licence", blurb: "Driving while suspended carries heavy penalties. We protect your record.", image: "/offence-suspended.png", imageOpacity: 0.42 },
  { title: "Demerit Points & Insurance", blurb: "Convictions follow you for years. We keep your abstract — and your rates — clean.", image: "/offence-demerit.png", imageOpacity: 0.42 },
  { title: "Fail to Stop / Remain", blurb: "From stop signs to collisions, we build the defence the charge calls for.", image: "/offence-fail-stop.png", imageOpacity: 0.4 },
];

// How it works — numbered step process (Garde Wilson "What happens" pattern).
export const PROCESS = [
  { step: "01", title: "Send Us Your Ticket", body: "Snap a photo of your ticket and send it over. It takes two minutes and costs nothing." },
  { step: "02", title: "Free Case Review", body: "We review the charge, the evidence, and your options — then call you with an honest read." },
  { step: "03", title: "We Fight It For You", body: "As your licensed paralegal we handle the paperwork and attend court on your behalf." },
  { step: "04", title: "Keep Your Record", body: "Our goal: the charge reduced or withdrawn, your licence intact, your insurance unaffected." },
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
    q: "Will a speeding ticket increase my insurance?",
    a: "Insurance consequences vary depending on the type of offence, your driving history, and your insurer. Before paying a ticket, it may be beneficial to understand the potential impact and explore your available options.",
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
