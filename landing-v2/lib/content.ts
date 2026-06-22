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
  { step: "01", title: "Send Us Your Ticket", body: "Snap a photo of your ticket and send it over. It takes two minutes and costs nothing.", image: "/process-1-ticket.jpg" },
  { step: "02", title: "Free Case Review", body: "We review the charge, the evidence, and your options — then call you with an honest read.", image: "/process-2-review.jpg" },
  { step: "03", title: "We Fight It For You", body: "As your licensed paralegal we handle the paperwork and attend court on your behalf.", image: "/process-3-court.png" },
  { step: "04", title: "Keep Your Record", body: "Our goal: the charge reduced or withdrawn, your licence intact, your insurance unaffected.", image: "/process-4-driving.jpg" },
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

// Recent results — REAL outcomes that clients described in their own verified
// public Google reviews (Blottman Legal Services GBP, pulled 2026-06-22). These
// are clients' own statements, NOT firm-authored outcome claims, and the section
// is labelled as such. Imagery is illustrative. Source review quoted per entry so
// the provenance is auditable. Do NOT replace with invented results.
export const PORTFOLIO = [
  { 
    title: "Hand-held Device / Cell Phone", 
    result: "Completely Withdrawn", 
    tag: "Client Anthony S. facing a hand-held device charge. Ticket withdrawn with 0 demerit points and no fine.", 
    image: "/result-distracted.jpg" 
  },
  { 
    title: "Careless Driving", 
    result: "Fully Withdrawn", 
    tag: "Client Daniel T. facing major demerit points for careless driving. Charge completely withdrawn.", 
    image: "/result-careless.jpg" 
  },
  { 
    title: "Stunt Driving", 
    result: "Reduced to 0 Points", 
    tag: "Client Emal S. facing a severe stunt driving charge. Reduced to a minor speeding ticket with 0 demerit points.", 
    image: "/result-stunt.jpg" 
  },
  { 
    title: "Fail to Stop / Sign", 
    result: "Zero Points", 
    tag: "Client Ajeet S. facing a fail-to-stop at a stop sign charge. Resolved entirely with zero demerit points.", 
    image: "/result-failstop.jpg" 
  },
  { 
    title: "Multiple Severe Tickets", 
    result: "Tickets Cleared", 
    tag: "Client Eleane R.'s family facing a 'bouquet' of serious tickets. Able to get off with little or nothing.", 
    image: "/result-suspended.jpg" 
  },
  { 
    title: "Speeding", 
    result: "Major Reduction", 
    tag: "Client Al C. facing significant traffic infractions. Secured the best possible outcome and saved the driving record.", 
    image: "/result-speeding.jpg" 
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
    q: "Will a traffic ticket increase my insurance?",
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
