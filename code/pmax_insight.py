import os, sys, logging
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()
config = {k:os.getenv(v) for k,v in {
  "developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID",
  "client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN",
  "login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
config["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(config)
ga=client.get_service("GoogleAdsService"); cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")
BMX="22979153470"; PERIOD=sys.argv[1].upper() if len(sys.argv)>1 else "LAST_7_DAYS"
def run(q): return list(ga.search(customer_id=cid, query=q))
print(f"\n=== PMAX BMX search-term INSIGHT categories ({PERIOD}) ===")
rows=run(f"""
  SELECT campaign_search_term_insight.category_label,
         metrics.impressions, metrics.clicks, metrics.conversions
  FROM campaign_search_term_insight
  WHERE segments.date DURING {PERIOD}
    AND campaign_search_term_insight.campaign_id = {BMX}
  ORDER BY metrics.clicks DESC
""")
if not rows: print("  (none)")
for r in rows:
    m=r.metrics; lbl=r.campaign_search_term_insight.category_label or "(uncategorized)"
    print(f"  {lbl[:48]:48} impr {m.impressions:>4} clk {m.clicks:>3} conv {m.conversions:.1f}")
