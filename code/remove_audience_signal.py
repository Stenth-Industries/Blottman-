"""Remove ONLY the audience signal from PMAX - Blottman Max asset group.
Keeps all SEARCH_THEME signals intact. Lists everything first, then removes
just the AUDIENCE-type signal(s). Run: python remove_audience_signal.py"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
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

# Target the winner's asset group on PMAX - Blottman Max
rows = list(ga.search(customer_id=cid, query="""
    SELECT asset_group_signal.resource_name, asset_group_signal.asset_group,
           asset_group_signal.audience.audience, asset_group_signal.search_theme.text,
           asset_group.name, campaign.name
    FROM asset_group_signal
    WHERE campaign.name = 'PMAX - Blottman Max'
"""))

audience_signals, theme_count = [], 0
print("\n  Signals on PMAX - Blottman Max asset group(s):")
for r in rows:
    sig = r.asset_group_signal
    if sig.audience.audience:
        audience_signals.append(sig.resource_name)
        print(f"   [AUDIENCE]  {sig.audience.audience}   <-- WILL REMOVE")
    elif sig.search_theme.text:
        theme_count += 1
print(f"   [SEARCH_THEMES] {theme_count} found   <-- KEEPING ALL")

if not audience_signals:
    print("\n  No audience signal found — nothing to remove.\n")
    raise SystemExit

svc = client.get_service("AssetGroupSignalService")
ops = []
for rn in audience_signals:
    op = client.get_type("AssetGroupSignalOperation")
    op.remove = rn
    ops.append(op)

resp = svc.mutate_asset_group_signals(customer_id=cid, operations=ops)
print(f"\n  REMOVED {len(resp.results)} audience signal(s):")
for res in resp.results:
    print(f"   {res.resource_name}")
print()
