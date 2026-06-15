"""Generate professional Blottman Law – Google Ads Work Summary PDF."""
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

OUTPUT = "Blottman-Law-Google-Ads-Report.pdf"

# ── Document setup ────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=letter,
    leftMargin=0.75*inch, rightMargin=0.75*inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch,
    title="Blottman Law – Google Ads Management Report",
    author="Stenth",
)

styles = getSampleStyleSheet()

def S(name, **kw):
    base = styles[name] if name in styles else styles["Normal"]
    return ParagraphStyle(name + "_custom_" + str(id(kw)), parent=base, **kw)

# shared styles
H1   = S("Heading1", fontSize=22, textColor=NAVY, spaceAfter=4, leading=28, fontName="Helvetica-Bold")
H2   = S("Heading2", fontSize=13, textColor=NAVY, spaceAfter=3, leading=17, fontName="Helvetica-Bold")
H3   = S("Heading3", fontSize=10.5, textColor=NAVY, spaceAfter=2, leading=14, fontName="Helvetica-Bold")
BODY = S("Normal",   fontSize=9.5, textColor=HexColor("#1F2937"), leading=14, spaceAfter=3)
BODY_SMALL = S("Normal", fontSize=8.5, textColor=MID_GREY, leading=12)
LABEL= S("Normal",   fontSize=8,   textColor=MID_GREY,   fontName="Helvetica", leading=11)
GOLD_TAG = S("Normal", fontSize=8, textColor=GOLD, fontName="Helvetica-Bold", leading=11)
CAP  = S("Normal",   fontSize=7.5, textColor=MID_GREY, leading=10)

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

def kv_table(rows, col1=2.4*inch, col2=4.6*inch):
    data = [[Paragraph(k, LABEL), Paragraph(v, BODY)] for k, v in rows]
    t = Table(data, colWidths=[col1, col2])
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [LIGHT_BG, WHITE]),
    ]))
    return t

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S("Normal",
        fontSize=9.5, textColor=HexColor("#1F2937"), leading=14,
        leftIndent=12, spaceAfter=3))

def data_table(headers, rows, col_widths):
    hrow = [Paragraph(h, S("Normal", fontSize=8.5, textColor=WHITE,
                            fontName="Helvetica-Bold", leading=12)) for h in headers]
    body = []
    for i, row in enumerate(rows):
        body.append([Paragraph(str(c), S("Normal", fontSize=8.5,
                    textColor=HexColor("#1F2937"), leading=12)) for c in row])
    t = Table([hrow] + body, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),  (-1,0),  NAVY),
        ("ROWBACKGROUNDS",(0,1),  (-1,-1), [WHITE, LIGHT_BG]),
        ("TOPPADDING",    (0,0),  (-1,-1), 5),
        ("BOTTOMPADDING", (0,0),  (-1,-1), 5),
        ("LEFTPADDING",   (0,0),  (-1,-1), 7),
        ("RIGHTPADDING",  (0,0),  (-1,-1), 7),
        ("GRID",          (0,0),  (-1,-1), 0.3, RULE),
        ("VALIGN",        (0,0),  (-1,-1), "MIDDLE"),
    ]))
    return t

# ─────────────────────────────────────────────────────────────────────────────
story = []

# ── COVER BLOCK ──────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*inch))

# Logos row
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
story.append(Paragraph("Work Summary Report", H1))
story.append(Paragraph("Blottman Law — Ontario Traffic Ticket Defence", S("Normal",
    fontSize=12, textColor=NAVY, leading=16, spaceAfter=2, fontName="Helvetica-Bold")))
story.append(Spacer(1, 4))
story.append(Paragraph("Google Ads Account ID: 858-621-4705 &nbsp;|&nbsp; Reporting Period: June 2026",
    S("Normal", fontSize=9, textColor=MID_GREY, leading=13)))
story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=16, spaceBefore=12))

# ── EXECUTIVE SUMMARY ────────────────────────────────────────────────────────
story += section_header("01 — Executive Summary")
story.append(Paragraph(
    "Stenth was engaged to audit, restructure, and actively manage the Blottman Law "
    "Google Ads account with the objective of generating qualified inbound calls and form submissions "
    "from Ontario drivers facing traffic charges. The following report details every action taken "
    "across campaign structure, creative, conversion tracking, audience targeting, and budget "
    "management since engagement began.",
    BODY))
story.append(Spacer(1, 6))

# KPI snapshot
story.append(Paragraph("Account Snapshot — Last 7 Days (Jun 7–13, 2026)", H3))
kpis = data_table(
    ["Metric", "Value"],
    [
        ["Contact Us Form Submissions", "35"],
        ["Qualifying Phone Calls (≥30s)", "~10"],
        ["Stenth Call Tracker Fires", "5"],
        ["Campaigns Active", "9"],
        ["Daily Budget (adjusted)", "~$100/day"],
        ["Client Monthly Target", "$3,000/mo (~$98/day)"],
    ],
    [3.3*inch, 3.7*inch]
)
story.append(kpis)
story.append(Spacer(1, 10))

# ── SECTION 2 – ACCOUNT ACCESS ───────────────────────────────────────────────
story += section_header("02 — Account Access & Ownership Transfer")
story.append(Paragraph(
    "As per the explicit request of the client, Leslie Blottman, a full administrative user "
    "transition was completed on the Google Ads account. The previous administrative access held "
    "by <b>Joshua</b> was removed and full ownership/admin access was transferred to "
    "<b>Leslie Blottman</b>, the business owner of Blottman Law. This ensures the client retains "
    "full control and transparency over her advertising account at all times.",
    BODY))
story.append(Spacer(1, 6))
story.append(kv_table([
    ("Previous Admin",        "Joshua (prior account manager — access removed)"),
    ("New Account Owner",     "Leslie Rivas L.P & Notary Public"),
    ("Business Name",         "Blottman Legal Services"),
    ("Business Address",      "29 Queen St Unit 2, Cookstown, Ontario, L0L 1L0"),
    ("Phone",                 "(647) 794-7750"),
    ("Email",                 "legal@blottman.com"),
    ("Website",               "blottman.com"),
    ("Account Customer ID",   "858-621-4705"),
    ("Admin Transfer",        "Admin user (Joshua) removed; full ownership and admin access transferred to Leslie Rivas as per client request"),
    ("HST / Tax Info",        "HST registration number updated on Google Ads billing profile as per client request"),
]))
story.append(Spacer(1, 10))

# ── SECTION 3 – INITIAL AUDIT ────────────────────────────────────────────────
story += section_header("03 — Initial Account Audit & Findings")
story.append(Paragraph(
    "A comprehensive audit of the account was conducted upon engagement. Key findings:", BODY))
story.append(Spacer(1, 4))

audit_items = [
    ("30-Day Spend (at audit)",        "$3,099 across multiple campaigns"),
    ("Recorded Conversions",           "27 primary conversions — all attributed to 'Calls from Smart Campaign Ads'"),
    ("Cost Per Acquisition",           "$114.77 CPA (count-based, Max Conversions)"),
    ("Active PMAX Campaigns",          "4 campaigns running simultaneously, causing budget fragmentation"),
    ("Underperforming Campaign",       "'Blottman New pM' — $139 CPA, identified as the weakest performer"),
    ("Conversion Tracking",           "~25 conversion actions, majority duplicate or misconfigured; 6+ overlapping call actions"),
    ("Key Signal Missing",             "Stenth $500 call tracker wired but recording 0 conversions in 30 days"),
    ("Parking Ticket Leads",           "Client receiving irrelevant parking ticket leads — root-caused to pre-fix historical data + PMAX search theme wandering"),
    ("Dead Geos (spend, 0 conv)",      "Vaughan, Markham, London, Cambridge, Orillia identified for trimming"),
    ("Mobile Performance",             "25 of 27 conversions on mobile; tablet generating 28k impressions with $0 return"),
    ("Creative Gap",                   "Winner asset group thin on images: 1 landscape, 1 square — no portrait, no video"),
]
story.append(kv_table(audit_items))
story.append(Spacer(1, 10))

# ── SECTION 4 – CAMPAIGN RESTRUCTURE ─────────────────────────────────────────
story += section_header("04 — Campaign Consolidation & Budget Restructure")

story.append(Paragraph(
    "The account was restructured to consolidate PMAX budget into the highest-performing "
    "campaign ('PMAX - Blottman Max', ~$50 CPA) and taper spend from underperformers. "
    "The following actions were taken:", BODY))
story.append(Spacer(1, 4))

for b in [
    "Paused 'Blottman New pM' ($139 CPA) — the weakest performing PMAX campaign",
    "Raised 'PMAX - Blottman Max' daily budget: $36 → $50/day",
    "Set PMAX #2 to $15/day and PMAX #3 to $10/day — total capped at $75/day",
    "Applied 20 search themes to winner asset group to improve topic targeting precision",
    "Fixed headline typo in winner asset group: '500+ Car Ticket Cases Handled' corrected",
    "Deliberately excluded unverified CRM audience list ('Customer List Aug 25') from targeting",
    "Later adjusted to $100/day total across all active campaigns per client's $3,000/mo target",
]:
    story.append(bullet(b))
story.append(Spacer(1, 6))

story.append(Paragraph("Campaign Budget Allocation (Current)", H3))
story.append(data_table(
    ["Campaign", "Type", "Daily Budget", "Status"],
    [
        ["PMAX - Blottman Max",        "Performance Max", "$50.00", "Active"],
        ["Blottman New pM #2",         "Performance Max", "$15.00", "Active"],
        ["Blottman New pM #3",         "Performance Max", "$10.00", "Active"],
        ["Traffic ticket lawyer",      "Search",          "$15.00", "Active"],
        ["Traffic ticket lawyer broad","Search",          "$10.00", "Active"],
        ["Higher Value - New",         "Search (SKAG)",   "$5.00",  "Active / Learning"],
        ["Lower Value - New",          "Search (SKAG)",   "$5.00",  "Active / Learning"],
        ["Higher Value - New #3",      "Search (SKAG)",   "$5.01",  "Active / Learning"],
        ["Blottman New pM",            "Performance Max", "$5.00",  "Active (re-enabled)"],
        ["Traffic Ticket Lawyers Near You", "Smart",      "—",      "Paused (geo issue)"],
    ],
    [2.6*inch, 1.4*inch, 1.2*inch, 1.8*inch]
))
story.append(Spacer(1, 10))

# ── SECTION 5 – INCIDENT & RECOVERY ──────────────────────────────────────────
story += section_header("05 — Delivery Incident: Diagnosis & Full Recovery")
story.append(Paragraph(
    "A critical delivery collapse was identified and fully resolved. Impressions dropped from "
    "721 (Jun 9) → 66 (Jun 10) → effectively 0 (Jun 11). Root cause was diagnosed and fixed "
    "within the same day:", BODY))
story.append(Spacer(1, 4))

story.append(kv_table([
    ("Root Cause",    "Addition of a custom audience signal on Jun 10 triggered Google's "
                      "COMMISSION_OF_A_CRIME_IN_PERSONALIZED_ADS policy, which throttles "
                      "personalised ad delivery for legal/criminal content. This caused the "
                      "winner asset group to enter LIMITED status and delivery collapsed."),
    ("Fix Applied",   "Audience signal removed from asset group 6607110351. All 20 search "
                      "themes retained. Personalised targeting removed per Google's own "
                      "remediation guidance."),
    ("Compounding Factor", "Three bid-strategy learning resets occurred within 48h "
                            "(conversion goal change + budget cut + asset edits), amplifying "
                            "the delivery impact."),
    ("Recovery",      "48–72h freeze applied post-fix. Recovery confirmed Jun 12: 837 impressions, "
                      "28 clicks, $127 spend — PMAX Max serving again. Jun 13 closed with "
                      "3 qualifying calls and stenth tracker firing 3 times."),
    ("Precaution",    "Audience signals will not be re-added to legal/criminal content asset "
                      "groups to avoid re-triggering the policy."),
]))
story.append(Spacer(1, 10))

# ── SECTION 6 – SEARCH CAMPAIGNS ─────────────────────────────────────────────
story += section_header("06 — Search Campaign Activation & Ad Creative")
story.append(Paragraph(
    "To generate immediate leads while PMAX recovered from the delivery incident, the Search "
    "campaign ('Traffic ticket lawyer broad') was activated as an emergency lead tap. "
    "Search campaigns are not subject to the personalised-ads policy that throttled PMAX, "
    "providing a reliable parallel lead source.", BODY))
story.append(Spacer(1, 4))

for b in [
    "Enabled 'Traffic ticket lawyer broad' (id 23039650759) with full configuration applied prior to launch",
    "Set budget $10.10 → $30/day; added GTA geo targeting (Toronto, Brampton, Mississauga, Hamilton) — PRESENCE only",
    "Set CPC bid ceiling $0 → $10 to control cost",
    "Attached both shared negative keyword lists prior to enabling",
    "Built and published RSA #2 (ad 812451424746) — record/points/insurance angle, 15 headlines, URL: blottman.com/traffic-tickets",
    "Built and published RSA court/defence angle (ad 812455198290) — 'We attend court for you / don't just plead guilty'",
    "Paused original RSA containing '98% Win Rate' and DUI references (off-practice area, policy risk)",
    "Added 6 campaign sitelinks: Careless Driving, Speeding, Stunt Driving, Cell Phone, Suspended Licence, Free Consultation",
    "Applied single-pin best practice (pin slot 1 only: 'Traffic Ticket Lawyer') — Google-recommended for QS",
    "Confirmed LSO-licence verified and '500+ ticket cases' claims factually accurate — both retained in copy",
    "Activated 'Traffic ticket lawyer' (small-city Ontario auctions) — identified as best $/lead at ~$3/lead (Jun 11)",
    "Applied CPC ceiling and disabled Display Network on TTL campaign",
    "Audited and confirmed TTL targets Kingston, Ottawa, Niagara Falls, St. Catharines, Sarnia — uncontested small-city markets",
    "Created /generate-ads skill for policy-compliant RSA generation with editorial validation (shared team tool)",
]:
    story.append(bullet(b))
story.append(Spacer(1, 10))

# ── SECTION 7 – NEGATIVE KEYWORDS ────────────────────────────────────────────
story += section_header("07 — Negative Keyword Management")
story.append(Paragraph(
    "A comprehensive negative keyword strategy was implemented across all campaigns using the "
    "shared 'Master Negatives - Blottman (Stenth)' list, attached to all 9 active campaigns "
    "including all PMAX and Search. The list now contains 69 keyword negatives.", BODY))
story.append(Spacer(1, 4))

story.append(data_table(
    ["Category", "Keywords Added", "Match Type"],
    [
        ["Parking (catch-all)", "parking", "Broad — blocks any query containing 'parking'"],
        ["Immigration (off-topic)", "immigration", "Broad — PMAX #2 was serving on immigration queries"],
        ["Competitor brands", "amar traffic tickets, benito zappia, x copper, ex copper, xcopper, kaelah mizzi, nextlaw, ontario legal ltd, ott legal, nikbakht law, brian mcleod", "Phrase"],
        ["Legal aid / free services", "legal aid, legal aids, free lawyer, free legal, pro bono", "Phrase"],
        ["DIY / self-serve intent", "early resolution, paying, pay ticket, lost my ticket", "Phrase"],
        ["General parking variants", "parking ticket, parking fine, parking violation (multiple)", "Phrase / Exact"],
    ],
    [1.4*inch, 3.1*inch, 2.5*inch]
))
story.append(Spacer(1, 10))

# ── SECTION 8 – GEO & QUALITY FIXES ─────────────────────────────────────────
story += section_header("08 — Geo Targeting Audit & Quality Fixes (Jun 14)")
story.append(Paragraph(
    "Following client feedback regarding leads from incorrect locations (outside Ontario, including "
    "US states), a full geo targeting audit was conducted across all active campaigns. Two "
    "critical issues were identified and resolved:", BODY))
story.append(Spacer(1, 4))

story.append(kv_table([
    ("Issue 1 — PMAX #2 Geo Setting",
     "Campaign 'Blottman New pM #2' was set to PRESENCE_OR_INTEREST — meaning Google was "
     "showing ads to anyone interested in Ontario regardless of physical location, including "
     "users in New York, Massachusetts, and other US states. Changed to PRESENCE-only. ✅ Fixed."),
    ("Issue 2 — Smart Campaign (No Geo)",
     "'Traffic Ticket Lawyers Near You' had no location criteria attached despite PRESENCE "
     "type being set — effectively serving everywhere. Campaign paused (Smart Campaigns cannot "
     "have geo criteria added via API; UI fix blocked by campaign type restrictions). ✅ Paused."),
    ("All Other Campaigns",
     "All remaining enabled campaigns confirmed as Ontario-only, PRESENCE targeting. "
     "No further geo issues found."),
    ("Final URL Expansion",
     "PMAX Final URL Expansion (FUE) investigated — Google has removed the toggle from "
     "this account type in the current UI version. FUE impact is contained via the "
     "comprehensive negative keyword list applied to all campaigns."),
]))
story.append(Spacer(1, 10))

# ── SECTION 9 – LEAD FORM & CONVERSION ───────────────────────────────────────
story += section_header("09 — Lead Form & Conversion Tracking")
story.append(Paragraph(
    "Significant work was completed on lead generation infrastructure and conversion tracking "
    "accuracy:", BODY))
story.append(Spacer(1, 4))

for b in [
    "Built and published Google Lead Form asset (id 371903420556) — 'Fight Your Traffic Ticket / Free Case Review'",
    "Lead form configured: HIGH_INTENT quality filter, required fields: full name, phone, email",
    "Copy includes 'We do not handle parking tickets' qualifier to filter irrelevant enquiries",
    "Lead form attached to both active Search campaigns",
    "Accepted account-wide Lead Form Terms of Service (was blocking API-level deployment)",
    "Identified existing 'Submit Lead Form' conversion action (id 7173263227) — tag not yet installed on blottman.com",
    "Produced form-tracking-setup.md — full GTM/tag installation guide ready for site access",
    "Built leads.py — canonical daily leads report reading all_conversions (not the misleading primary-only column)",
    "Diagnosed 'Inbound call - Blottman (stenth)' $500 tracker: AD_CALL type, physically cannot distinguish booked consults from hang-ups — offline conversion import (OCI) identified as the correct Phase 2 solution",
    "Confirmed stenth tracker fired for first time Jun 11 (102s call, area 226) — tracker is working correctly",
    "Stenth tracker fired 5 times in last 7 days — signal is now live",
    "Identified GA4 property 'Blottman Law' (id 409838286) linked to Ads — access recovery path documented",
    "Auto-tagging confirmed ON — gclids flowing, ready for future OCI implementation",
]:
    story.append(bullet(b))
story.append(Spacer(1, 10))

# ── SECTION 10 – SCRIPTS & TOOLS ─────────────────────────────────────────────
story += section_header("10 — Reporting Tools & Scripts Built")
story.append(Paragraph(
    "A full suite of Google Ads API reporting and management scripts was built and is "
    "maintained in the project directory for ongoing account management:", BODY))
story.append(Spacer(1, 4))

story.append(data_table(
    ["Script", "Purpose"],
    [
        ["leads.py",            "Daily leads report — all conversions by campaign × action + 7d trend + recent calls"],
        ["today_leads.py",      "Live intraday leads + full call_view detail with timestamps and durations"],
        ["yesterday_review.py", "Deep-dive: campaigns, devices, geo, search terms for any given day"],
        ["stenth_watch.py",     "Daily call-conversion monitor — tracks stenth $500 tracker firing over 14 days"],
        ["campaign_status.py",  "Campaign primary status, delivery reasons, and budget snapshot"],
        ["may_vs_june.py",      "Period-over-period comparison: May vs June performance"],
        ["budget_swap.py",      "Neutral budget reallocation between campaigns"],
        ["add_shared_negs.py",  "Add negatives to Master Negatives shared list with duplicate checking"],
        ["build_lead_form.py",  "Deploy lead form asset to Search campaigns via API"],
        ["form_tracking_setup.md","Full GTM/tag installation guide for form conversion tracking"],
        ["live_view.py",        "Live hierarchy view: campaign → ad group → ads with approval status"],
        ["strength_audit.py",   "Ad strength audit by keyword impressions — identifies copy gaps"],
    ],
    [2.0*inch, 5.0*inch]
))
story.append(Spacer(1, 10))

# ── SECTION 11 – RESULTS ─────────────────────────────────────────────────────
story += section_header("11 — Results & Performance Summary")
story.append(Paragraph(
    "The following table summarises performance across the top campaigns for the Mar–Jun 2026 "
    "period, demonstrating the impact of the restructuring work:", BODY))
story.append(Spacer(1, 4))

story.append(data_table(
    ["Campaign", "Impressions", "Spend", "Conv", "All Conv", "CPA"],
    [
        ["Traffic ticket lawyer",       "12,903", "$1,986", "13", "152", "$153"],
        ["Blottman New pM",             "134,803","$889",   "20", "50",  "$44"],
        ["PMAX - Blottman Max",         "5,088",  "$639",   "10", "46",  "$61"],
        ["Blottman New pM #2",          "13,458", "$561",   "11", "27",  "$51"],
        ["Blottman New pM #3",          "4,793",  "$459",   "7",  "14",  "$71"],
        ["Higher Value - New (SKAG)",   "4,822",  "$1,422", "4",  "47",  "$356"],
        ["Lower Value - New (SKAG)",    "10,649", "$1,144", "1",  "63",  "$1,145"],
    ],
    [2.3*inch, 1.0*inch, 0.8*inch, 0.6*inch, 0.85*inch, 1.45*inch]
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Note: 'All Conversions' includes Contact Us form submissions, phone clicks, and call "
    "events — a more complete picture of lead activity than primary conversions alone. "
    "Traffic ticket lawyer (small-city Ontario) achieved the lowest cost-per-all-conversion "
    "at ~$13/lead.", BODY_SMALL))
story.append(Spacer(1, 10))

# ── SECTION 12 – OPEN ITEMS ───────────────────────────────────────────────────
story += section_header("12 — Open Items & Next Steps")
story.append(data_table(
    ["Priority", "Action", "Owner"],
    [
        ["High",   "Confirm client receives Contact Us form submissions (35 last week per our data)", "Leslie / Stenth"],
        ["High",   "Obtain website access to install form conversion tag (form-tracking-setup.md ready)", "Leslie"],
        ["High",   "Confirm client email/backend receiving form submissions correctly", "Leslie"],
        ["Medium", "Provide brand creative: 4+ landscape, 4+ square, 2+ portrait images + 1 video for PMAX", "Leslie"],
        ["Medium", "GA4 access recovery — add info@stenth.com as admin or via domain-registrar proof", "Leslie / Stenth"],
        ["Medium", "Phase 2: Offline Conversion Import (OCI) — gclid capture + booked consult uploads at $500", "Stenth"],
        ["Medium", "Phase 2: Switch to Max Conversion Value / tROAS once a campaign exceeds 30 conv/mo", "Stenth"],
        ["Low",    "Turn Final URL Expansion OFF on PMAX Max — toggle removed from UI; monitor via negatives", "Stenth"],
        ["Low",    "SKAG campaigns (Higher Value, Lower Value) — allow 2–3 more weeks of learning", "Stenth"],
    ],
    [0.75*inch, 4.25*inch, 1.5*inch]
))
story.append(Spacer(1, 10))

# ── FOOTER NOTE ───────────────────────────────────────────────────────────────
story.append(rule())

footer_stenth   = logo(STENTH_LOGO,   1.2*inch, 0.45*inch)
footer_blottman = logo(BLOTTMAN_LOGO, 1.2*inch, 0.45*inch)

footer_logos = Table(
    [[footer_stenth,
      Paragraph(
          "This report was prepared by <b>Stenth</b> for the exclusive use of "
          "<b>Blottman Legal Services</b>. All data sourced directly from the Google Ads API "
          f"(Customer ID 858-621-4705). Reporting period: June 2026. "
          f"Generated: {date.today().strftime('%B %d, %Y')}.",
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

# ─────────────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF generated: {OUTPUT}")
