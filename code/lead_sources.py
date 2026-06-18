"""Where did YESTERDAY's conversions actually come from — search terms (Search) + PMAX insight categories."""
import os, sys, logging
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()
config = {
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
}
client = GoogleAdsClient.load_from_dict(config)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
PERIOD = sys.argv[1].upper() if len(sys.argv) > 1 else "YESTERDAY"
def run(q): return list(ga.search(customer_id=cid, query=q))
def usd(m): return m/1_000_000

print(f"\n=== {PERIOD}: SEARCH terms that CONVERTED (all_conversions>0) ===")
rows = run(f"""
  SELECT campaign.name, search_term_view.search_term, segments.keyword.info.text,
         metrics.clicks, metrics.cost_micros, metrics.all_conversions, metrics.conversions
  FROM search_term_view
  WHERE segments.date DURING {PERIOD} AND metrics.all_conversions > 0
  ORDER BY metrics.all_conversions DESC
""")
if not rows: print("  (none)")
for r in rows:
    m=r.metrics
    print(f"  [{r.campaign.name[:22]:22}] \"{r.search_term_view.search_term}\"")
    print(f"      kw=\"{r.segments.keyword.info.text}\" | clk {m.clicks} ${usd(m.cost_micros):.2f} | allconv {m.all_conversions:.1f} (bid {m.conversions:.1f})")

print(f"\n=== {PERIOD}: PMAX search-term INSIGHT categories (with conv) ===")
try:
    rows = run(f"""
      SELECT campaign_search_term_insight.category_label,
             metrics.impressions, metrics.clicks, metrics.conversions
      FROM campaign_search_term_insight
      WHERE segments.date DURING {PERIOD}
      ORDER BY metrics.clicks DESC
    """)
    if not rows: print("  (none)")
    for r in rows:
        m=r.metrics; lbl=r.campaign_search_term_insight.category_label or "(uncategorized)"
        print(f"  {lbl[:50]:50} impr {m.impressions:>4} clk {m.clicks:>3} conv {m.conversions:.1f}")
except Exception as e:
    print("  insight query error:", e)
