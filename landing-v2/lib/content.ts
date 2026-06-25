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

// Trustindex widget id for the live Google-reviews embed.
// ⚠️ Left EMPTY on purpose (2026-06-25): the Trustindex free trial expired and now
// requires a paid plan. We don't need it — GoogleReviews.tsx falls back to our OWN
// on-brand reviews section (dark/gold cards, Google badge, 4.9/81 rating) populated
// from the real verified GOOGLE_SAMPLE_REVIEWS below. This also avoids Trustindex's
// rating-only ("left a rating", no text) entries that look empty to visitors.
// Only put a widget id back here if you re-subscribe and want the live auto-updating embed.
export const TRUSTINDEX_WIDGET_ID = "";

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
  // Optional offence illustration shown beside the intro (OffenseDetails).
  image?: string;
  bgImage?: string;
  // Rich "Potential Penalties" cards rendered by OffenseDetails. Penalty data is
  // sourced from blottman.com's per-offence pages (HTA/CAIA sections, demerit
  // points, fines, suspensions) — facts kept, the site's "#1 lawyer / 98%"
  // marketing claims deliberately dropped for LSO compliance.
  consequences?: { icon?: "fine" | "suspend" | "impound" | "points" | "insurance" | "record" | "jail"; titleValue: string; titleLabel: string; description: string }[];
  // Legacy flat penalty list (kept for reference; not currently rendered — the
  // OffenseDetails component renders `consequences` instead).
  penaltiesHeading?: string;
  penalties?: string[];
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
      "Speeding is more than just a fine. A conviction stays on your record, adds demerit points, and can raise your insurance for years.",
        bgImage: "/speeding_dark_bg.png",
    consequences: [
      { icon: "points", titleValue: "Up to 6", titleLabel: "Demerit Points", description: "Up to 6 points added to your record, depending on your speed." },
      { icon: "insurance", titleValue: "Up to 3 Years", titleLabel: "Insurance Increases", description: "Your premiums can spike for up to 3 years." },
      { icon: "fine", titleValue: "Hundreds", titleLabel: "In Fines", description: "Fines scale with your speed, potentially costing hundreds of dollars." }
    ],
    penaltiesHeading: "A speeding conviction can result in:",
    penalties: [
      "Demerit points on your record",
      "A possible licence suspension",
      "Insurance premiums that can stay high for years",
    ],
  },

  "careless-driving": {
    slug: "careless-driving",
    metaTitle: "Fight a Careless Driving Charge | Blottman Legal Services — Ontario",
    metaDescription:
      "Charged with careless driving in Ontario? A licensed paralegal fights the charge to protect your record, demerit points and insurance. Free case review.",
    eyebrow: "Ontario Careless-Driving Defence",
    titleLine1: "Fight your careless driving charge.",
    titleLine2: "Protect your",
    titleHighlight: "record.",
    benefits: [
      "Careless driving can carry 6 demerit points — we fight to avoid them",
      "Most clients never set foot in court",
      "We work to protect your record and insurance rates",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Careless Driving",
    introHeading: "Charged with careless driving in Ontario?",
    introBody:
      "Careless driving is the most serious non-criminal driving charge in Ontario. A conviction can ruin your record, spike your insurance, and potentially lead to jail time.",
        bgImage: "/careless_dark_bg.png",
    consequences: [
      { titleValue: "6", titleLabel: "Demerit Points", description: "Careless driving carries a heavy penalty that severely impacts your record." },
      { icon: "suspend", titleValue: "Up to 2 Years", titleLabel: "Licence Suspension", description: "You face a potential suspension of your driver's licence for up to 2 years." },
      { titleValue: "Up to $2,000", titleLabel: "Fines & Jail Time", description: "Fines range from $400 to $2,000, with a possibility of up to 6 months in jail." }
    ],
    penaltiesHeading: "A careless driving conviction can result in:",
    penalties: [
      "6 demerit points",
      "A licence suspension of up to 2 years",
      "A fine between $400 and $2,000",
      "Up to 6 months of imprisonment",
    ],
  },

  "stunt-driving": {
    slug: "stunt-driving",
    metaTitle: "Fight a Stunt Driving Charge | Blottman Legal Services — Ontario",
    metaDescription:
      "Charged with stunt driving in Ontario? A licensed paralegal fights the charge — your licence, your insurance, your record. Free, confidential case review.",
    eyebrow: "Ontario Stunt-Driving Defence",
    titleLine1: "Fight your stunt driving charge.",
    titleLine2: "Protect your",
    titleHighlight: "licence.",
    benefits: [
      "Stunt driving brings an immediate roadside suspension and impound — we fight back",
      "Most clients never set foot in court",
      "We work to protect your record and insurance rates",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Stunt Driving",
    introHeading: "Charged with stunt driving or racing in Ontario?",
    introBody:
      "A stunt driving charge means an immediate roadside suspension and vehicle impoundment. If convicted, the long-term impact on your life and insurance is devastating.",
    bgImage: "/stunt_driving_bg.png",
    consequences: [
      { titleValue: "30 Days", titleLabel: "Licence Suspension", description: "A 30-day licence suspension and a 14-day vehicle impound the day you're charged — before any trial." },
      { titleValue: "$2,000–$10,000", titleLabel: "Fine & Jail", description: "On conviction under s.172(2), with up to 6 months in jail on a first offence and harsher penalties for repeats." },
      { titleValue: "1 to 3 Years", titleLabel: "Suspension", description: "A conviction carries a long licence suspension and major insurance fallout — often cancellation or massive premium hikes." }
    ],
    penaltiesHeading: "Under s.172(2), a stunt driving conviction can result in:",
    penalties: [
      "A fine of $2,000 to $10,000",
      "A licence suspension of 1 to 3 years",
      "Up to 6 months in jail on a first conviction",
      "Harsher penalties, including longer jail time, for repeat offences",
    ],
  },

  "fail-to-stop": {
    slug: "fail-to-stop",
    metaTitle: "Fight a Fail to Stop Ticket | Blottman Legal Services — Ontario",
    metaDescription:
      "Got a fail to stop at a stop sign ticket in Ontario? A licensed paralegal fights it to protect your demerit points, record and insurance. Free case review.",
    eyebrow: "Ontario Fail-to-Stop Defence",
    titleLine1: "Fight your fail to stop ticket.",
    titleLine2: "Protect your",
    titleHighlight: "record.",
    benefits: [
      "A fail-to-stop conviction adds demerit points — we work to keep them off",
      "Most clients never set foot in court",
      "We work to protect your record and insurance rates",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Fail to Stop",
    introHeading: "Ticketed for failing to stop in Ontario?",
    introBody:
      "Failing to stop at a sign or red light might feel minor, but it adds demerit points and can quietly increase your insurance premiums at renewal.",
        bgImage: "/careless_dark_bg.png",
    consequences: [
      { icon: "points", titleValue: "3", titleLabel: "Demerit Points", description: "A conviction automatically adds 3 points to your driving record." },
      { titleValue: "Increases", titleLabel: "Insurance Impact", description: "Considered a minor conviction, but can still lead to increased premiums." },
      { titleValue: "Set Fine", titleLabel: "Traffic Fines", description: "You will face a set fine along with a victim surcharge." }
    ],
    penaltiesHeading: "Under s.136(1), a fail to stop conviction can result in:",
    penalties: [
      "3 demerit points",
      "A set fine",
      "Higher insurance premiums at renewal",
    ],
  },

  "disobey-sign": {
    slug: "disobey-sign",
    metaTitle: "Fight a Disobey Sign Ticket | Blottman Legal Services — Ontario",
    metaDescription:
      "Charged with disobeying a sign in Ontario? A licensed paralegal fights the ticket to protect your demerit points, record and insurance. Free case review.",
    eyebrow: "Ontario Disobey-Sign Defence",
    titleLine1: "Fight your disobey sign ticket.",
    titleLine2: "Protect your",
    titleHighlight: "record.",
    benefits: [
      "A disobey-sign conviction adds demerit points — we work to keep them off",
      "Most clients never set foot in court",
      "We work to protect your record and insurance rates",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Disobey Sign",
    introHeading: "Ticketed for disobeying a sign in Ontario?",
    introBody:
      "Disobeying a sign adds demerit points to your driving record. Paying the ticket is an automatic guilty plea—fight it to protect your abstract.",
        bgImage: "/disobey_dark_bg.png",
    consequences: [
      { icon: "points", titleValue: "2 to 3", titleLabel: "Demerit Points", description: "Most disobey sign tickets carry 2 to 3 demerit points." },
      { icon: "record", titleValue: "3 Years", titleLabel: "On Your Record", description: "The conviction stays on your abstract for three years." },
      { icon: "fine", titleValue: "Set Fine", titleLabel: "Fines & Surcharges", description: "A standard fine applies upon conviction." }
    ],
    penaltiesHeading: "A disobey sign conviction can result in:",
    penalties: [
      "3 demerit points",
      "A set fine",
      "Higher insurance premiums at renewal",
    ],
  },

  "no-insurance": {
    slug: "no-insurance",
    metaTitle: "Fight a No Insurance Ticket | Blottman Legal Services — Ontario",
    metaDescription:
      "Charged with driving with no insurance in Ontario? Fines start in the thousands. A licensed paralegal fights the charge — free, confidential case review.",
    eyebrow: "Ontario No-Insurance Defence",
    titleLine1: "Fight your no insurance ticket.",
    titleLine2: "Protect your",
    titleHighlight: "wallet.",
    benefits: [
      "No-insurance fines can start in the thousands — we fight to reduce the damage",
      "Most clients never set foot in court",
      "We work to protect your record and insurance options",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Driving With No Insurance",
    introHeading: "Charged with driving with no insurance in Ontario?",
    introBody:
      "Driving without insurance carries staggering fines starting in the thousands of dollars, plus the real risk of a licence suspension.",
        bgImage: "/abstract_siren_bg.png",
    consequences: [
      { icon: "fine", titleValue: "Up to $25,000", titleLabel: "In Fines", description: "A first conviction ranges from $5,000 to $25,000 (rising to $10,000–$50,000 for a subsequent one), plus a 25% surcharge." },
      { icon: "suspend", titleValue: "Up to 1 Year", titleLabel: "Licence Suspension", description: "Your licence can be suspended for up to one year." },
      { icon: "impound", titleValue: "Up to 3 Months", titleLabel: "Vehicle Impound", description: "Your vehicle may be impounded for up to 3 months." }
    ],
    penaltiesHeading: "A no insurance conviction can result in:",
    penalties: [
      "A fine of $5,000 to $25,000 on a first conviction",
      "A fine of $10,000 to $50,000 on a subsequent conviction",
      "A licence suspension of up to 1 year",
    ],
  },

  "driving-under-suspension": {
    slug: "driving-under-suspension",
    metaTitle: "Fight a Driving Under Suspension Charge | Blottman Legal Services",
    metaDescription:
      "Charged with driving under suspension in Ontario? A licensed paralegal fights the charge — your licence, your record, your future. Free case review.",
    eyebrow: "Ontario Suspended-Driving Defence",
    titleLine1: "Fight your driving under suspension charge.",
    titleLine2: "Protect your",
    titleHighlight: "licence.",
    benefits: [
      "Driving under suspension can mean more fines, a longer suspension and impound — we fight it",
      "Most clients never set foot in court",
      "We work to protect your record and insurance rates",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Driving Under Suspension",
    introHeading: "Charged with driving under suspension in Ontario?",
    introBody:
      "Driving while suspended is heavily penalized. You face a mandatory further 6-month suspension, steep fines, and even potential jail time.",
        bgImage: "/no_licence_dark_bg.png",
    consequences: [
      { titleValue: "6 Months", titleLabel: "Further Suspension", description: "A mandatory additional 6-month licence suspension." },
      { titleValue: "7 Days", titleLabel: "Vehicle Impoundment", description: "Immediate 7-day impoundment of the vehicle you were driving." },
      { titleValue: "Up to $5,000", titleLabel: "Fines & Jail Time", description: "Fines starting at $1,000, with potential for up to 6 months in jail." }
    ],
    penaltiesHeading: "A drive under suspension conviction can result in:",
    penalties: [
      "A fine of $1,000 to $5,000",
      "Up to 6 months of imprisonment",
      "An additional 6-month licence suspension",
    ],
  },

  "no-licence": {
    slug: "no-licence",
    metaTitle: "Fight a No Licence Ticket | Blottman Legal Services — Ontario",
    metaDescription:
      "Charged with driving without a licence in Ontario? A licensed paralegal fights the ticket to protect your record and insurance. Free, confidential review.",
    eyebrow: "Ontario No-Licence Defence",
    titleLine1: "Fight your no licence ticket.",
    titleLine2: "Protect your",
    titleHighlight: "record.",
    benefits: [
      "A no-licence conviction can follow your record — we work to limit the impact",
      "Most clients never set foot in court",
      "We work to protect your record and insurance rates",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Driving Without a Licence",
    introHeading: "Charged with driving without a licence in Ontario?",
    introBody:
      "Driving without a valid licence stays on your driving record and can severely affect your future ability to get insured.",
        bgImage: "/no_licence_dark_bg.png",
    consequences: [
      { titleValue: "From $200", titleLabel: "In Fines", description: "Tickets for driving without a valid licence carry fines starting at $200." },
      { titleValue: "Rate Hikes", titleLabel: "Insurance Consequences", description: "Can cause issues with your policy or lead to rate increases." },
      { titleValue: "On Record", titleLabel: "No Demerit Points", description: "While there are no points, the conviction still appears on your abstract." }
    ],
    penaltiesHeading: "A no licence charge can result in:",
    penalties: [
      "Significant fines",
      "A court date",
      "A possible driving prohibition",
      "Lasting damage to your driving record",
    ],
  },

  "cell-phone": {
    slug: "cell-phone",
    metaTitle: "Fight a Cell Phone Ticket | Blottman Legal Services — Ontario",
    metaDescription:
      "Got a distracted driving or hand-held cell phone ticket in Ontario? A licensed paralegal fights it to protect your record and insurance. Free case review.",
    eyebrow: "Ontario Distracted-Driving Defence",
    titleLine1: "Fight your cell phone ticket.",
    titleLine2: "Protect your",
    titleHighlight: "record.",
    benefits: [
      "A distracted driving conviction adds demerit points and can suspend your licence — we fight it",
      "Most clients never set foot in court",
      "We work to protect your record and insurance rates",
      "Licensed Ontario paralegal, 500+ tickets handled",
    ],
    introEyebrow: "Cell Phone / Distracted Driving",
    introHeading: "Charged with distracted driving in Ontario?",
    introBody:
      "Distracted driving carries brutal penalties in Ontario, including steep fines, heavy demerit points, and an immediate licence suspension.",
        bgImage: "/cell_phone_dark_bg.png",
    consequences: [
      { icon: "points", titleValue: "3", titleLabel: "Demerit Points", description: "A conviction adds 3 demerit points to your driving record." },
      { icon: "suspend", titleValue: "3 Days", titleLabel: "Immediate Suspension", description: "A 3-day licence suspension for first-time fully licensed drivers." },
      { icon: "fine", titleValue: "Up to $1,000", titleLabel: "In Fines", description: "A hefty fine if convicted or if you lose at trial." }
    ],
    penaltiesHeading: "A handheld device conviction can result in:",
    penalties: [
      "A monetary fine",
      "A 3-day driver's licence suspension",
      "3 demerit points",
      "Higher penalties for repeat offences",
    ],
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
