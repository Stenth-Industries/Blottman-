"""Read-only diagnosis of Leslie's "I keep getting calls for courthouse" complaint
(Jul 17). Same shape as the Jul-5 "how do I pay parking tickets" issue: callers
who want the COURT OFFICE (address / date / fine payment / trial scheduling),
not representation.

Prints, for both enabled campaigns:
  1. Search Consolidated  -> real search terms (search_term_view) w/ court-ish tokens
  2. PMAX BMX             -> insight categories (semantic groupings, not literal)
  3. every court-ish term regardless of campaign, so nothing hides
  4. current court-related negatives already in Master Negatives

Usage: python code/courthouse_diag.py [LAST_14_DAYS]
"""
import os, sys, logging
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()
config = {k: os.getenv(v) for k, v in {
    "developer_token": "GOOGLE_ADS_DEVELOPER_TOKEN", "client_id": "GOOGLE_ADS_CLIENT_ID",
    "client_secret": "GOOGLE_ADS_CLIENT_SECRET", "refresh_token": "GOOGLE_ADS_REFRESH_TOKEN",
    "login_customer_id": "GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
config["use_proto_plus"] = True
client = GoogleAdsClient.load_from_dict(config)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

PERIOD = sys.argv[1].upper() if len(sys.argv) > 1 else "LAST_14_DAYS"
BMX = "22979153470"
SEARCH_CONSOLIDATED = "23971101309"
SHARED_SET = f"customers/{cid}/sharedSets/12109076551"

# tokens that signal "I want the courthouse/court office", not a defence rep
COURT_TOKENS = ["court", "courthouse", "court house", "trial", "hearing", "docket",
                "adjourn", "summons", "notice of trial", "first appearance",
                "early resolution", "prosecutor", "crown", "clerk", "jp",
                "justice of the peace", "address", "phone number", "hours",
                "where is", "when is", "reschedule", "date"]


def run(q):
    return list(ga.search(customer_id=cid, query=q))


def courtish(text):
    t = text.lower()
    return [tok for tok in COURT_TOKENS if tok in t]


print(f"\n{'='*72}\n COURTHOUSE-CALL DIAGNOSIS  ({PERIOD})\n{'='*72}")

# ---------------------------------------------------------------- 1. Search terms
print("\n--- 1. Search Consolidated: real search terms containing court-ish tokens ---")
rows = run(f"""
  SELECT search_term_view.search_term, campaign.name, ad_group.name,
         metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
  FROM search_term_view
  WHERE segments.date DURING {PERIOD}
  ORDER BY metrics.clicks DESC
""")
hits = [r for r in rows if courtish(r.search_term_view.search_term)]
if not hits:
    print("  (no court-ish search terms at all — Search side is clean)")
for r in hits:
    m = r.metrics
    print(f"  {r.search_term_view.search_term[:44]:44} impr {m.impressions:>4} "
          f"clk {m.clicks:>3} ${m.cost_micros/1e6:>6.2f} conv {m.conversions:.1f}"
          f"  [{r.campaign.name[:22]}]")
print(f"\n  ({len(rows)} search terms total in period, {len(hits)} court-ish)")

# --------------------------------------------------- 2. PMAX insight categories
print("\n--- 2. PMAX (BMX) insight categories — court-ish ---")
rows = run(f"""
  SELECT campaign_search_term_insight.category_label,
         metrics.impressions, metrics.clicks, metrics.conversions
  FROM campaign_search_term_insight
  WHERE segments.date DURING {PERIOD}
    AND campaign_search_term_insight.campaign_id = {BMX}
  ORDER BY metrics.clicks DESC
""")
hits = [r for r in rows if courtish(r.campaign_search_term_insight.category_label or "")]
if not hits:
    print("  (no court-ish categories)")
for r in hits:
    m = r.metrics
    lbl = r.campaign_search_term_insight.category_label or "(uncategorized)"
    print(f"  {lbl[:48]:48} impr {m.impressions:>5} clk {m.clicks:>3} conv {m.conversions:.1f}")

print("\n  --- BMX top 25 categories by clicks (full context) ---")
for r in rows[:25]:
    m = r.metrics
    lbl = r.campaign_search_term_insight.category_label or "(uncategorized)"
    flag = "  <-- COURT" if courtish(lbl) else ""
    print(f"  {lbl[:48]:48} impr {m.impressions:>5} clk {m.clicks:>3} conv {m.conversions:.1f}{flag}")

# ------------------------------------------------- 3. existing court negatives
print("\n--- 3. Court-related negatives already in Master Negatives ---")
rows = run(f"""
  SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type
  FROM shared_criterion
  WHERE shared_criterion.shared_set = '{SHARED_SET}'
    AND shared_criterion.type = 'KEYWORD'
""")
all_negs = [(r.shared_criterion.keyword.text, r.shared_criterion.keyword.match_type.name) for r in rows]
court_negs = [(t, mt) for t, mt in all_negs if courtish(t)]
for t, mt in sorted(court_negs):
    print(f"  [{mt[:3]}] {t}")
print(f"\n  ({len(all_negs)} negatives in list, {len(court_negs)} court-related)")
