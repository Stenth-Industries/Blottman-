"""Generate the updated Blottman Legal Services - Google Ads engagement report PDF.

Covers the full engagement Jun 8 - Jul 5, 2026. Reuses the visual style of
generate_report.py (Jun-14 report). Run from the project root:
    python code/generate_report_v2.py
"""
import os
from datetime import date

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image as RLImage,
)

# -- Brand colours ------------------------------------------------------------
NAVY     = HexColor("#0D1B2A")
GOLD     = HexColor("#C9A84C")
LIGHT_BG = HexColor("#F5F7FA")
MID_GREY = HexColor("#6B7280")
RULE     = HexColor("#DDE2EA")
WHITE    = colors.white
GREEN    = HexColor("#16A34A")
RED_SOFT = HexColor("#DC2626")

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, "Blottman-Legal-Services-Ads-Report-Jul-2026.pdf")

doc = SimpleDocTemplate(
    OUTPUT, pagesize=letter,
    leftMargin=0.75*inch, rightMargin=0.75*inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch,
    title="Blottman Legal Services - Google Ads Engagement Report",
    author="Stenth",
)

styles = getSampleStyleSheet()

def S(name, **kw):
    base = styles[name] if name in styles else styles["Normal"]
    return ParagraphStyle(name + "_c" + str(id(kw)), parent=base, **kw)

H1   = S("Heading1", fontSize=22, textColor=NAVY, spaceAfter=4, leading=28, fontName="Helvetica-Bold")
H3   = S("Heading3", fontSize=10.5, textColor=NAVY, spaceAfter=2, leading=14, fontName="Helvetica-Bold")
BODY = S("Normal", fontSize=9.5, textColor=HexColor("#1F2937"), leading=14, spaceAfter=3)
CAP  = S("Normal", fontSize=7.5, textColor=MID_GREY, leading=10)
LABEL = S("Normal", fontSize=8, textColor=MID_GREY, leading=11)

def section_header(text):
    return [
        Spacer(1, 10),
        Table([[Paragraph(text, S("Normal", fontSize=11, textColor=WHITE,
                                  fontName="Helvetica-Bold", leading=15))]],
              colWidths=[7*inch],
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                  ("TOPPADDING", (0, 0), (-1, -1), 7),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                  ("LEFTPADDING", (0, 0), (-1, -1), 10),
              ])),
        Spacer(1, 6),
    ]

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S("Normal",
        fontSize=9.5, textColor=HexColor("#1F2937"), leading=14,
        leftIndent=12, spaceAfter=3))

def kv_table(rows, col1=2.4*inch, col2=4.6*inch):
    data = [[Paragraph(k, LABEL), Paragraph(v, BODY)] for k, v in rows]
    t = Table(data, colWidths=[col1, col2])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_BG, WHITE]),
    ]))
    return t

def data_table(headers, rows, col_widths):
    hrow = [Paragraph(h, S("Normal", fontSize=8.5, textColor=WHITE,
                           fontName="Helvetica-Bold", leading=12)) for h in headers]
    body = [[Paragraph(str(c), S("Normal", fontSize=8.5,
             textColor=HexColor("#1F2937"), leading=12)) for c in row] for row in rows]
    t = Table([hrow] + body, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t

def logo(path, max_w, max_h):
    if os.path.exists(path):
        img = RLImage(path)
        w, h = img.imageWidth, img.imageHeight
        ratio = min(max_w / w, max_h / h)
        img.drawWidth = w * ratio
        img.drawHeight = h * ratio
        return img
    return Paragraph("", BODY)

# ------------------------------------------------------------------------------
story = []

# -- COVER ---------------------------------------------------------------------
story.append(Spacer(1, 0.3*inch))
stenth_img = logo(os.path.join(ROOT, "STENTH LOGO.png"), 1.6*inch, 0.6*inch)
blottman_img = logo(os.path.join(ROOT, "ad-images", "blottman_logo_black_1200.png"),
                    0.8*inch, 0.8*inch)
logo_row = Table(
    [[stenth_img,
      Paragraph(f"Prepared: {date.today().strftime('%B %d, %Y')}",
                S("Normal", fontSize=9, textColor=MID_GREY, leading=12, alignment=TA_CENTER)),
      blottman_img]],
    colWidths=[2*inch, 3*inch, 2*inch])
logo_row.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (0, 0), (0, 0), "LEFT"),
    ("ALIGN", (2, 0), (2, 0), "RIGHT"),
]))
story.append(logo_row)
story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=16, spaceBefore=8))

story.append(Paragraph("Google Ads Management", S("Normal", fontSize=13, textColor=MID_GREY, leading=18)))
story.append(Paragraph("Engagement Report", H1))
story.append(Paragraph("Blottman Legal Services — Ontario Traffic Ticket Defence",
    S("Normal", fontSize=12, textColor=NAVY, leading=16, spaceAfter=2, fontName="Helvetica-Bold")))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Google Ads Account ID: 858-621-4705 &nbsp;|&nbsp; Reporting Period: June 8 – July 5, 2026",
    S("Normal", fontSize=9, textColor=MID_GREY, leading=13)))
story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=14, spaceBefore=12))

# -- 01 EXECUTIVE SUMMARY --------------------------------------------------------
story += section_header("01 — Executive Summary")
story.append(Paragraph(
    "Stenth was engaged to audit, restructure, and actively manage the Blottman Legal Services "
    "Google Ads account, with the objective of generating qualified inbound calls and case-review "
    "requests from Ontario drivers facing traffic charges. Over the reporting period the account was "
    "consolidated from a sprawl of overlapping campaigns into a focused two-campaign structure, two "
    "Google policy incidents were diagnosed and resolved, targeting and negative-keyword gaps that "
    "produced irrelevant calls were closed, conversion tracking was rebuilt around verified signals, "
    "and a new conversion-focused website (blottman.ca) was designed, built, and wired into the account.",
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph("Headline results — engagement start vs. now", H3))
story.append(data_table(
    ["Metric", "At engagement (early June)", "Now (early July)"],
    [
        ["Cost per verified lead", "$114.77", "~$53 (verified 30s+ calls, PMAX)"],
        ["Active campaigns", "9+ overlapping, uncoordinated", "2 focused (1 PMAX + 1 Search)"],
        ["Daily spend control", ">$100/day, uncapped ceilings", "~$95/day, aligned to $3K/mo target"],
        ["Geo targeting", "None / worldwide on key campaigns", "Ontario, presence-only, verified"],
        ["Irrelevant calls (parking, immigration, out-of-province)", "Frequent — client complaints", "Substantially eliminated"],
        ["Conversion tracking", "~25 overlapping actions, unreliable", "Verified call tracker firing + website form tracking live"],
        ["Website lead capture", "Single bottom-of-page form, 5 required fields", "2-step hero QuickForm + instant auto-reply, 2 required fields"],
    ],
    [2.2*inch, 2.4*inch, 2.4*inch]))
story.append(Spacer(1, 6))
story.append(Paragraph("Last 7 days (Jun 29 – Jul 5)", H3))
story.append(data_table(
    ["Signal", "Count", "Note"],
    [
        ["Verified inbound calls (30s+)", "5", "All from PMAX; all Ontario callers, no junk"],
        ["Website form leads (blottman.ca)", "3", "New tracked signal — first full week live"],
        ["Phone-number clicks", "2", "Mobile users tapping the number on the site"],
        ["Contact Us form events", "14", "Untracked legacy signal — reported for reference only"],
    ],
    [2.6*inch, 0.9*inch, 3.5*inch]))
story.append(Spacer(1, 10))

# -- 02 CLIENT & OBJECTIVE -------------------------------------------------------
story += section_header("02 — Client & Objective")
story.append(kv_table([
    ("Client", "Leslie Rivas — Blottman Legal Services (Licensed in Ontario, Notary Public)"),
    ("Practice", "Ontario traffic ticket defence: speeding, careless driving, stunt driving, "
                 "cell phone / distracted driving, driving under suspension, no insurance. "
                 "Parking tickets are not handled."),
    ("Service area", "All of Ontario; core converting market is the GTA (Toronto, Brampton, Mississauga, Hamilton)"),
    ("Office", "29 Queen St Unit 2, Cookstown, Ontario"),
    ("Websites", "blottman.com (legacy) and blottman.ca (new landing site, built by Stenth)"),
    ("Monthly ad budget target", "$3,000/month (~$98/day)"),
    ("Objective", "Qualified phone calls and case-review form submissions from Ontario drivers"),
]))
story.append(Spacer(1, 10))

# -- 03 RESTRUCTURE ---------------------------------------------------------------
story += section_header("03 — Account Restructure & Consolidation")
story.append(Paragraph(
    "The account was inherited with more than nine overlapping campaigns — multiple duplicate "
    "Performance Max campaigns, fragmented Search campaigns, and a Smart Campaign — competing with "
    "each other, splitting Google's learning data, and spending past the client's budget target with "
    "no cost-per-click ceilings. Actions taken:", BODY))
story.append(Spacer(1, 4))
for b in [
    "Identified the one Performance Max campaign with a proven cost per call (<b>PMAX - Blottman Max</b>) "
    "and consolidated budget behind it; paused duplicate PMAX campaigns that were mis-targeted "
    "(one served only Sarnia and Windsor) and produced irrelevant calls.",
    "Replaced four fragmented Search campaigns — which spent roughly $1,000/month without a single "
    "verified phone call — with one consolidated Search campaign: ten ad groups, one offence each "
    "(speeding, careless driving, stunt driving, etc.), each landing on its matching blottman.ca page, "
    "with a full extension stack (sitelinks, callouts, call asset, lead form, business logo).",
    "Set cost-per-click ceilings on campaigns that had none, and aligned total daily budgets to the "
    "client's $3,000/month target.",
    "Applied account-level content exclusions to steer spend away from low-quality display placements.",
]:
    story.append(bullet(b))
story.append(Spacer(1, 6))
story.append(Paragraph("Current live structure", H3))
story.append(data_table(
    ["Campaign", "Type", "Budget", "Role"],
    [
        ["PMAX - Blottman Max", "Performance Max", "$65/day", "Primary call generator — produces all verified calls"],
        ["Search - Ontario Traffic Tickets (Consolidated)", "Search", "$30/day", "Offence-specific search coverage — generates website form leads"],
    ],
    [2.6*inch, 1.1*inch, 0.8*inch, 2.5*inch]))
story.append(Spacer(1, 10))

# -- 04 POLICY -----------------------------------------------------------------
story += section_header("04 — Google Policy Incidents Resolved")
for b in [
    "<b>Personalized-ads policy throttle (mid-June).</b> Ad delivery collapsed to near zero for three days. "
    "Diagnosed the cause — Google's personalized-advertising policy for legal-services content had "
    "throttled the main campaign after an audience signal was attached. Removed the trigger per Google's "
    "own remediation guidance; delivery fully recovered.",
    "<b>Unsubstantiated-claims cleanup.</b> Inherited ad copy across the account carried claims Google "
    "flags as clickbait in the legal vertical ('98% Win Rate', '#1'). Replaced every flagged asset with "
    "compliant copy built on verifiable claims (500+ cases handled, 4.8-star rating with 300+ reviews, "
    "Licensed in Ontario). The cleanup also aligned all ad copy with Law Society of Ontario "
    "advertising rules.",
    "<b>Compromised legacy domain.</b> Discovered assets in the account still pointing to the old "
    "blottmanlaw.com domain, which had been compromised and repurposed by a third party. Detached every "
    "such asset from live campaigns.",
]:
    story.append(bullet(b))
story.append(Spacer(1, 10))

# -- 05 TARGETING ----------------------------------------------------------------
story += section_header("05 — Targeting Cleanup: Ending the Irrelevant Calls")
story.append(Paragraph(
    "The client's most persistent complaint — calls about parking tickets, immigration, legal aid, and "
    "callers from outside Ontario — traced to concrete targeting gaps, each of which was closed:", BODY))
story.append(Spacer(1, 4))
for b in [
    "<b>Geography:</b> the main campaign had <b>no geographic targeting at all</b> (it could serve "
    "worldwide — the source of New York and Massachusetts callers), and others targeted the wrong "
    "cities. All live campaigns now target Ontario only, restricted to people physically in Ontario.",
    "<b>Negative keywords:</b> built a ~100-term master negative list, attached to every live campaign, "
    "blocking parking tickets, immigration, legal aid, lawsuits and other practice areas, competitor "
    "brand names, do-it-yourself intent ('how to pay a ticket'), and municipal payment-portal searches. "
    "The list was grown iteratively from real search-term and call data each time a leak appeared.",
    "<b>Result:</b> the last two weeks of verified calls are all Ontario callers with traffic-ticket "
    "intent — no parking, no immigration, no out-of-province. Note: Performance Max matches searches "
    "semantically, so occasional off-target calls can still occur; a 10-second phone triage line "
    "('we fight tickets — for payments call 311') is the recommended handling.",
]:
    story.append(bullet(b))
story.append(Spacer(1, 10))

# -- 06 TRACKING -----------------------------------------------------------------
story += section_header("06 — Conversion Tracking Rebuilt")
for b in [
    "Inherited ~25 overlapping conversion actions with inconsistent values. Identified the one trustworthy "
    "signal — the call tracker that fires on real inbound calls of 30 seconds or longer — and confirmed it "
    "now fires consistently (it had recorded zero for weeks).",
    "Demoted unreliable signals (an untagged 'Contact Us' counter that inflated lead reports) so campaign "
    "bidding optimizes only toward verified calls and real form submissions.",
    "Built real website form tracking on blottman.ca: every form submission now fires a tracked conversion "
    "and captures the Google click ID — the foundation for eventually telling Google which leads became "
    "signed clients, so bidding can chase clients rather than callers.",
    "Built a standard daily reporting toolkit so lead counts quoted to the client always come from "
    "verified data.",
]:
    story.append(bullet(b))
story.append(Spacer(1, 10))
story.append(PageBreak())

# -- 07 WEBSITE ------------------------------------------------------------------
story += section_header("07 — New Website: blottman.ca")
story.append(Paragraph(
    "Stenth designed, built, and deployed a conversion-focused landing site at blottman.ca, now the "
    "destination for all Search ad traffic:", BODY))
story.append(Spacer(1, 4))
for b in [
    "<b>Two-step QuickForm</b> directly under the hero on every page — charge type + phone number first, "
    "name second — cutting required fields from five to two. Verified end-to-end with automated browser tests.",
    "<b>Instant lead handling:</b> every submission emails the team in real time and sends the lead a "
    "professional confirmation auto-reply signed by Leslie, so leads are never left waiting silently.",
    "<b>Nine offence-specific landing pages</b> (speeding, careless driving, stunt driving, cell phone, "
    "and more), each with accurate Highway Traffic Act penalty content pulled from the practice's "
    "materials — built, reviewed for Law Society of Ontario compliance, and held ready for the wider "
    "rollout the client approved in principle ('once we see consistent traction').",
    "<b>Compliance-first copy sitewide:</b> no outcome guarantees, no 'lawyer' terminology, no ticket-upload "
    "feature (all Law Society of Ontario requirements flagged by the client) — and the site brand updated "
    "to the confirmed legal name, Blottman Legal Services.",
]:
    story.append(bullet(b))
story.append(Spacer(1, 10))

# -- 08 PERFORMANCE ----------------------------------------------------------------
story += section_header("08 — Where Performance Stands")
story.append(Paragraph(
    "The account now runs a clean two-campaign structure at ~$95/day. PMAX - Blottman Max produces all "
    "verified phone calls at roughly $53 per verified call — down from $114.77 at engagement — with call "
    "quality confirmed clean (all Ontario, GTA-dominant, including multi-minute consultations). The "
    "consolidated Search campaign is in its ramp-up phase and has begun producing tracked website form "
    "leads, its intended role. Current weekly output is approximately 8–10 verified leads (calls + forms) "
    "plus additional untracked form activity.", BODY))
story.append(Spacer(1, 10))

# -- 09 BOTTLENECKS -----------------------------------------------------------------
story += section_header("09 — What Is Capping Lead Volume Now")
story.append(Paragraph(
    "The advertising layer is tuned: targeting is clean, policy issues are resolved, tracking is "
    "trustworthy, and cost per lead has been cut by more than half. The two constraints on caseload "
    "growth now sit <b>outside the ad auction</b>:", BODY))
story.append(Spacer(1, 6))
story.append(Paragraph("1. Call answer rate — the single largest leak", H3))
story.append(Paragraph(
    "Roughly half of all paid inbound calls end in under 30 seconds or go unanswered entirely. On July 3 "
    "alone, three calls were missed and a fourth lasted seven seconds — approximately four paid leads lost "
    "in one day. Ticket shoppers typically call several firms in a row; the first to answer wins the case. "
    "Fixing pickup is worth more than any possible budget or bidding change.", BODY))
story.append(Spacer(1, 4))
for b in [
    "<b>Missed-call text-back</b> on the business line: any unanswered call instantly receives a text "
    "('Sorry we missed you — reply with your ticket type and we'll call back within the hour').",
    "<b>Callback booking link</b> on the website thank-you page and in the lead auto-reply, so a missed "
    "connection still becomes a scheduled conversation.",
    "<b>Answering coverage</b> for court hours — a live answering service or trained assistant with a "
    "short, compliant intake script.",
]:
    story.append(bullet(b))
story.append(Spacer(1, 6))
story.append(Paragraph("2. Brand creative — the untapped growth lever", H3))
story.append(Paragraph(
    "The top-performing campaign runs on only two images, with no portrait imagery and no video. "
    "Supplying a small creative package — a half-day photo shoot (office, professional portraits) and one "
    "30–60 second introduction video — would unlock significantly more ad inventory on the same budget. "
    "Stenth will script the video for Law Society compliance and handle all editing and rollout; the only "
    "requirement from the client is the shoot itself.", BODY))
story.append(Spacer(1, 10))

# -- 10 NEXT STEPS ------------------------------------------------------------------
story += section_header("10 — Recommended Next Steps")
story.append(data_table(
    ["#", "Action", "Owner", "Impact"],
    [
        ["1", "Missed-call text-back + callback booking link", "Leslie (line setup) + Stenth (build)", "Recover ~half of paid calls currently lost"],
        ["2", "Brand creative package (photos + 1 video)", "Leslie (shoot) + Stenth (script, edit, rollout)", "Unlock PMAX inventory on the same budget"],
        ["3", "Client-signed tracking loop (mark which leads retained)", "Leslie (30 sec/lead) + Stenth (upload to Google)", "Teach Google to find clients, not just callers"],
        ["4", "Google Business Profile optimization + review velocity", "Stenth", "Free calls from the local map pack"],
        ["5", "Search Console + sitemap for the 9 blottman.ca pages", "Stenth", "Free organic leads over time"],
    ],
    [0.35*inch, 2.5*inch, 2.05*inch, 2.1*inch]))
story.append(Spacer(1, 14))
story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=8, spaceBefore=4))
story.append(Paragraph(
    "Prepared by Stenth — info@stenth.com | Google Ads account 858-621-4705 | "
    f"{date.today().strftime('%B %d, %Y')}", CAP))

doc.build(story)
print(f"OK -> {OUTPUT}")
