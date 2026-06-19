"""Generate 'Problems with Google Ads' PDF — Blottman Law.
A client-facing explanation of every obstacle faced since Stenth took over,
grouped by cause, with the campaign impact of each. Matches the brand styling
of generate_report.py."""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.platypus import PageBreak
from reportlab.lib.colors import HexColor
from reportlab.platypus import Image as RLImage
import os
from datetime import date

# ── Brand colours ────────────────────────────────────────────────────────────
NAVY      = HexColor("#0D1B2A")
GOLD      = HexColor("#C9A84C")
LIGHT_BG  = HexColor("#F5F7FA")
MID_GREY  = HexColor("#6B7280")
RULE      = HexColor("#DDE2EA")
WHITE     = colors.white
GREEN     = HexColor("#16A34A")
RED_SOFT  = HexColor("#DC2626")
AMBER     = HexColor("#B45309")

OUTPUT = "Problems with Google Ads.pdf"

doc = SimpleDocTemplate(
    OUTPUT, pagesize=letter,
    leftMargin=0.75*inch, rightMargin=0.75*inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch,
    title="Blottman Law – Problems Faced in Google Ads Management",
    author="Stenth",
)

styles = getSampleStyleSheet()

def S(name, **kw):
    base = styles[name] if name in styles else styles["Normal"]
    return ParagraphStyle(name + "_custom_" + str(id(kw)), parent=base, **kw)

H1   = S("Heading1", fontSize=22, textColor=NAVY, spaceAfter=4, leading=28, fontName="Helvetica-Bold")
H2   = S("Heading2", fontSize=13, textColor=NAVY, spaceAfter=3, leading=17, fontName="Helvetica-Bold")
H3   = S("Heading3", fontSize=10.5, textColor=NAVY, spaceAfter=2, leading=14, fontName="Helvetica-Bold")
BODY = S("Normal", fontSize=9.5, textColor=HexColor("#1F2937"), leading=14, spaceAfter=3)
BODY_SMALL = S("Normal", fontSize=8.5, textColor=MID_GREY, leading=12)
LABEL= S("Normal", fontSize=8, textColor=MID_GREY, fontName="Helvetica", leading=11)
CAP  = S("Normal", fontSize=7.5, textColor=MID_GREY, leading=10)

def rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=6, spaceBefore=6)

def section_header(text):
    return [
        Spacer(1, 10),
        Table([[Paragraph(text, S("Normal", fontSize=11, textColor=WHITE,
                                  fontName="Helvetica-Bold", leading=15))]],
              colWidths=[7*inch],
              style=TableStyle([
                  ("BACKGROUND", (0,0), (-1,-1), NAVY),
                  ("TOPPADDING",  (0,0), (-1,-1), 7),
                  ("BOTTOMPADDING",(0,0),(-1,-1), 7),
                  ("LEFTPADDING", (0,0), (-1,-1), 10),
              ])),
        Spacer(1, 6),
    ]

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S("Normal",
        fontSize=9.5, textColor=HexColor("#1F2937"), leading=14,
        leftIndent=12, spaceAfter=3))

def problem_block(num, title, what, impact, status):
    """A single problem card: number + title, What happened, Campaign impact, Status."""
    title_p = Paragraph(f"<b>{num}. {title}</b>",
                        S("Normal", fontSize=10.5, textColor=NAVY, leading=14,
                          fontName="Helvetica-Bold"))
    rows = [
        [Paragraph("What happened", LABEL), Paragraph(what, BODY)],
        [Paragraph("Effect on campaigns", LABEL),
         Paragraph(impact, S("Normal", fontSize=9.5, textColor=HexColor("#1F2937"), leading=14))],
        [Paragraph("Status", LABEL), Paragraph(status, BODY)],
    ]
    inner = Table(rows, colWidths=[1.35*inch, 5.45*inch])
    inner.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("LINEBEFORE",   (0,0), (0,-1), 2, GOLD),
    ]))
    return KeepTogether([title_p, Spacer(1,2), inner, Spacer(1, 9)])

def data_table(headers, rows, col_widths):
    hrow = [Paragraph(h, S("Normal", fontSize=8.5, textColor=WHITE,
                            fontName="Helvetica-Bold", leading=12)) for h in headers]
    body = [[Paragraph(str(c), S("Normal", fontSize=8.5,
            textColor=HexColor("#1F2937"), leading=12)) for c in row] for row in rows]
    t = Table([hrow] + body, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),  (-1,0),  NAVY),
        ("ROWBACKGROUNDS",(0,1),  (-1,-1), [WHITE, LIGHT_BG]),
        ("TOPPADDING",    (0,0),  (-1,-1), 5),
        ("BOTTOMPADDING", (0,0),  (-1,-1), 5),
        ("LEFTPADDING",   (0,0),  (-1,-1), 7),
        ("RIGHTPADDING",  (0,0),  (-1,-1), 7),
        ("GRID",          (0,0),  (-1,-1), 0.3, RULE),
        ("VALIGN",        (0,0),  (-1,-1), "TOP"),
    ]))
    return t

# ─────────────────────────────────────────────────────────────────────────────
story = []

STENTH_LOGO   = "STENTH LOGO.png"
BLOTTMAN_LOGO = "BLOTTMAN LOGO.png"

def logo(path, max_w, max_h):
    if os.path.exists(path):
        img = RLImage(path)
        w, h = img.imageWidth, img.imageHeight
        ratio = min(max_w/w, max_h/h)
        img.drawWidth  = w * ratio
        img.drawHeight = h * ratio
        return img
    return Paragraph("", BODY)

stenth_img   = logo(STENTH_LOGO,   1.6*inch, 0.6*inch)
blottman_img = logo(BLOTTMAN_LOGO, 1.6*inch, 0.6*inch)

logo_row = Table(
    [[stenth_img,
      Paragraph(f"Prepared: {date.today().strftime('%B %d, %Y')}",
                S("Normal", fontSize=9, textColor=MID_GREY, leading=12, alignment=TA_CENTER)),
      blottman_img]],
    colWidths=[2*inch, 3*inch, 2*inch]
)
logo_row.setStyle(TableStyle([
    ("VALIGN",  (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN",   (0,0), (0,0),   "LEFT"),
    ("ALIGN",   (2,0), (2,0),   "RIGHT"),
]))
story.append(logo_row)
story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=16, spaceBefore=8))

story.append(Paragraph("Google Ads Management", S("Normal", fontSize=13, textColor=MID_GREY,
                                                    fontName="Helvetica", leading=18)))
story.append(Paragraph("Problems Faced &amp; Their Impact", H1))
story.append(Paragraph("Blottman Law — Ontario Traffic Ticket Defence", S("Normal",
    fontSize=12, textColor=NAVY, leading=16, spaceAfter=2, fontName="Helvetica-Bold")))
story.append(Spacer(1, 4))
story.append(Paragraph("Google Ads Account ID: 858-621-4705 &nbsp;|&nbsp; Period: Engagement to date (June 2026)",
    S("Normal", fontSize=9, textColor=MID_GREY, leading=13)))
story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=16, spaceBefore=12))

# ── PURPOSE ──────────────────────────────────────────────────────────────────
story += section_header("Purpose of This Document")
story.append(Paragraph(
    "This document is an honest, plain-language account of the obstacles encountered while "
    "managing the Blottman Law Google Ads account since Stenth took over. It exists to give "
    "full transparency on <b>why results have been slower than everyone wants</b>. "
    "The core message is straightforward: the majority of these problems were either "
    "<b>inherited from the previous account setup</b> or are <b>access blockers outside our "
    "control</b> — not a lack of demand for the service or a lack of work on the account. "
    "Each problem below is shown with what happened, how it affected the campaigns, and where "
    "it stands today.", BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "The single most important takeaway is at the end (Section 5): the biggest unlock for "
    "stronger, more consistent results is restoring website and analytics access so we can "
    "track leads properly — without it, Google's automated system is effectively learning blind.",
    BODY_SMALL))
story.append(Spacer(1, 8))

# ── CATEGORY 1 — INHERITED ───────────────────────────────────────────────────
story += section_header("01 — Problems Inherited From the Previous Setup")
story.append(Paragraph(
    "These issues existed in the account before Stenth took over. Much of the early work was "
    "spent cleaning these up before genuine optimisation could even begin.", BODY))
story.append(Spacer(1, 8))

story.append(problem_block(
    1, "Conversion tracking was a “junk drawer”",
    "The account had roughly 25 overlapping conversion actions — a dozen enabled at once, with "
    "6+ duplicate call actions and inconsistent values ($0 / $1 / $10 / $150 / $500).",
    "Google's automated bidding could not tell a real lead from noise, so it was optimising "
    "toward unreliable signals. This wastes budget and is a primary cause of inconsistent results.",
    "Audited and rationalised; the misleading 'Contact Us' count was correctly demoted so bidding "
    "no longer chases it. Root fix depends on website access (see Section 2)."))

story.append(problem_block(
    2, "Multiple redundant, overspending campaigns",
    "Several near-duplicate Performance Max campaigns ran simultaneously — one spending roughly "
    "double its daily budget — pushing total spend over $100/day with no real control.",
    "Budget was burned on the client's own campaigns competing against each other instead of "
    "reaching new customers, inflating cost-per-lead.",
    "Consolidated onto the single best campaign (PMAX - Blottman Max); duplicates paused. ✅ Done."))

story.append(problem_block(
    3, "A hacked old domain was still wired into the account",
    "The previous domain <b>blottmanlaw.com</b> (different from the live blottman.com) had been "
    "compromised and flagged by Google for gambling/malware content. 24 ad links plus a promotion "
    "still pointed to it, sitting disapproved in the account.",
    "A live policy liability that risked dragging down the entire account's standing with Google — "
    "the kind of thing that can lead to account-level penalties if left attached to live ads.",
    "All 24 compromised links plus the promotion were detached from every active campaign. ✅ Done "
    "(June 16)."))

story.append(problem_block(
    4, "Misleading ad claims baked into the inherited copy",
    "Phrases like “98% Win Rate”, “#1 Lawyer” and “100% Representation” are written into roughly "
    "30 ads. Google treats unverifiable statistics and superlatives as a <b>“Clickbait” policy "
    "violation</b>.",
    "This is <b>currently limiting the best campaign (PMAX)</b> — it is throttled right now because "
    "of this inherited copy. Limited campaigns serve less and produce fewer leads.",
    "Diagnosed in full; compliant replacement copy drafted and ready. Being coordinated before "
    "applying (it affects multiple campaigns at once)."))

story.append(problem_block(
    5, "Campaigns had no — or incorrect — location targeting",
    "The main PMAX campaign was set to serve <b>anywhere in the world</b> (no location limit). "
    "Other campaigns were mis-targeted to Sarnia/Windsor instead of the Greater Toronto Area.",
    "This was the direct source of the out-of-province and out-of-area leads the client reported "
    "(including calls from New York and Massachusetts). Money spent reaching people who could never "
    "become clients.",
    "Corrected to Ontario-only, presence-based targeting; mis-targeted duplicates paused. ✅ Done."))

# ── CATEGORY 2 — EXTERNAL BLOCKERS ───────────────────────────────────────────
story += section_header("02 — External Blockers Outside Our Control (the biggest drag)")
story.append(Paragraph(
    "These are the most significant constraints on results — and they are not advertising "
    "decisions. They are access and infrastructure problems that limit what any advertiser could "
    "achieve on this account.", BODY))
story.append(Spacer(1, 8))

story.append(problem_block(
    6, "Website access was lost — nobody has it",
    "No one currently has access to edit blottman.com, so we cannot install the proper conversion "
    "tracking tag on the website.",
    "Form submissions do not register as conversions. This is the root of the tracking problem "
    "described in #9 below and the single largest constraint on performance.",
    "Recovery paths documented; installation guide is written and ready the moment access is "
    "restored. ⏳ Waiting on client."))

story.append(problem_block(
    7, "The website rebuild was promised, then cancelled",
    "Our optimisation plan (Phase 1) depended on a new website with clean tracking and working "
    "landing pages. The client withdrew from the rebuild partway through.",
    "We had to re-scope the entire plan around the existing, partly-broken site — limiting how far "
    "the campaigns can be optimised.",
    "Plan re-scoped to the existing site. Ongoing constraint."))

story.append(problem_block(
    8, "A key landing page was broken",
    "blottman.com/traffic-tickets — the page several ads pointed to — was returning a broken page "
    "(confirmed by the client).",
    "Ads were sending paid clicks to a dead page, wasting spend and losing leads that had already "
    "been paid for.",
    "All affected ads immediately repointed to the working homepage. ✅ Done."))

story.append(problem_block(
    9, "ROOT CAUSE — too few tracked leads for the system to learn from",
    "Because the form tag cannot be installed (no website access) and analytics access was also "
    "lost, Google only “sees” about 5 confirmed quality conversions per month. Automated bidding "
    "needs roughly 15–30 per month to optimise properly.",
    "This is the #1 technical reason results are inconsistent: the system literally cannot learn "
    "with so little data. It is a tracking and access problem — not a demand problem.",
    "Fully diagnosed. Resolving it depends on restoring website + analytics access. ⏳ Waiting on client."))

# ── CATEGORY 3 — PLATFORM & POLICY ───────────────────────────────────────────
story += section_header("03 — Google Platform &amp; Policy Issues")
story.append(Paragraph(
    "These stem from how Google's platform and its policies treat legal/criminal-defence "
    "advertising. They affect every advertiser in this category, not just this account.", BODY))
story.append(Spacer(1, 8))

story.append(problem_block(
    10, "The “calls went dark” incident (June 9–11)",
    "Ad delivery collapsed from 721 impressions (Jun 9) to 66 (Jun 10) to effectively zero "
    "(Jun 11). Cause: Google's “Commission of a crime in personalised advertising” policy, which "
    "automatically throttles delivery for legal/criminal-defence content.",
    "Roughly three days of near-zero leads — the most visible “slow” period the client experienced.",
    "Diagnosed and fixed the same day; delivery recovered. PMAX is now the account's strongest "
    "lead source again. ✅ Resolved."))

story.append(problem_block(
    11, "Legal/criminal content is permanently policy-restricted",
    "Traffic and criminal-defence content carries a permanent Google policy label that limits the "
    "use of personalised targeting tools.",
    "A structural headwind for any law-firm advertiser: it removes some of the targeting levers "
    "available to other industries, making delivery more fragile.",
    "Managed by avoiding the triggers (e.g. no audience signals on these asset groups). Ongoing."))

story.append(problem_block(
    12, "Performance Max auto-expands beyond our direct control",
    "Performance Max automatically spreads ads across Search, Display, YouTube and Gmail. Keywords "
    "are treated as “hints”, not hard limits.",
    "Some irrelevant impressions and calls (parking, immigration, etc.) slip through despite "
    "extensive negative-keyword work — a known platform limitation we continuously manage.",
    "Ongoing: large negative-keyword lists maintained; final URL expansion turned off; junk "
    "campaigns paused."))

# ── CATEGORY 4 — OPERATIONAL ─────────────────────────────────────────────────
story += section_header("04 — Operational &amp; Coordination Issues")
story.append(Paragraph(
    "These relate to how leads are handled once generated, and to the pace of changes requested — "
    "areas where the outcome depends on factors beyond the ad platform itself.", BODY))
story.append(Spacer(1, 8))

story.append(problem_block(
    13, "Speed-to-answer on incoming calls",
    "Of roughly 1,100 total calls generated, about half were under 30 seconds — i.e. missed calls "
    "or voicemail hang-ups.",
    "We are delivering the phone calls, but a large share are not being answered. Leads generated "
    "is not the same as leads captured — unanswered calls look like “no results” even when the ads "
    "are working.",
    "Flagged for the client; faster call answering would directly convert existing volume."))

story.append(problem_block(
    14, "Uncertainty over whether form submissions are received",
    "Our data showed about 35 form fills in one week; the client reported receiving only 5–10. "
    "Without website access we cannot verify where the others went (spam folder, broken email "
    "forwarding, etc.).",
    "Real leads may be arriving but never reaching the client's inbox — which would explain a "
    "perceived lack of results despite recorded activity.",
    "Requires website/email-backend access to confirm. ⏳ Waiting on client."))

story.append(problem_block(
    15, "Frequent reactive changes forced by urgent requests",
    "Repeated urgent requests to “bring back the old campaigns” and “get leads now” forced several "
    "major changes within short windows (the Jun 9–11 period alone saw three learning resets in "
    "48 hours).",
    "Every major change resets Google's learning phase. Stacking changes suppresses delivery — "
    "stability is what produces consistent results, and constant changes work directly against it.",
    "Ongoing: we now recommend spacing major changes and avoiding bundling them."))

# ── CATEGORY 5 — THE PATH FORWARD ────────────────────────────────────────────
story += section_header("05 — What This Means &amp; The Fastest Path to Better Results")
story.append(Paragraph(
    "The honest summary: the slowdown is real, but its causes are overwhelmingly (a) inherited "
    "problems we have been cleaning up, and (b) access blockers outside our control — not a lack "
    "of effort or a lack of market demand.", BODY))
story.append(Spacer(1, 6))
story.append(Paragraph("Two things are already going right:", H3))
story.append(bullet("<b>The lead engine is working and improving.</b> PMAX produced 4 quality calls "
                    "in a single recent day, and 10 quality calls in the last 7 days — versus only "
                    "5 in the entire prior month. The trend is clearly upward."))
story.append(bullet("<b>The account is now clean and healthy.</b> Compromised assets removed, geo "
                    "fixed, junk campaigns paused, delivery recovered, negatives in place."))
story.append(Spacer(1, 8))

story.append(Paragraph("What we need from the client to accelerate:", H3))
story.append(data_table(
    ["Priority", "What we need", "Why it matters"],
    [
        ["1 — Highest", "Website access (or the web developer's contact)",
         "Lets us install proper lead tracking so Google can finally learn — the single biggest "
         "unlock for consistent results."],
        ["2 — High", "Confirm form submissions are reaching the inbox",
         "Determines whether real leads are being lost before they reach the client."],
        ["3 — High", "Faster answering of incoming calls",
         "Roughly half of calls go unanswered today; answering them converts volume we already "
         "generate."],
        ["4 — Medium", "Analytics (GA4) access",
         "Allows us to import website lead data as conversions without any code change."],
        ["5 — Medium", "Brand creative (images + a short video)",
         "Strengthens Performance Max, which is currently thin on visual assets."],
    ],
    [0.95*inch, 2.35*inch, 3.7*inch]
))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "With tracking restored, Google's automated bidding moves from ~5 signals per month to 30+ — "
    "the threshold where it can genuinely optimise. That, more than any single campaign change, is "
    "what will turn recovering momentum into consistent, predictable lead flow.", BODY))
story.append(Spacer(1, 10))

# ── FOOTER ────────────────────────────────────────────────────────────────────
story.append(rule())

footer_stenth   = logo(STENTH_LOGO,   1.2*inch, 0.45*inch)
footer_blottman = logo(BLOTTMAN_LOGO, 1.2*inch, 0.45*inch)

footer_logos = Table(
    [[footer_stenth,
      Paragraph(
          "This document was prepared by <b>Stenth</b> for the exclusive use of "
          "<b>Blottman Legal Services</b>. All performance data sourced directly from the Google "
          f"Ads API (Customer ID 858-621-4705). Generated: {date.today().strftime('%B %d, %Y')}.",
          S("Normal", fontSize=8, textColor=MID_GREY, leading=12, alignment=TA_CENTER)
      ),
      footer_blottman]],
    colWidths=[1.4*inch, 4.2*inch, 1.4*inch]
)
footer_logos.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN",  (0,0), (0,0),   "LEFT"),
    ("ALIGN",  (2,0), (2,0),   "RIGHT"),
]))
story.append(footer_logos)

doc.build(story)
print(f"PDF generated: {OUTPUT}")
