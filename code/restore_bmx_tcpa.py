"""Restore BMX Target CPA to $95 after the unlogged Jul-28 removal.

CONTEXT (2026-08-09):
  Change history shows tCPA on PMAX - Blottman Max was set to 0 (removed)
  on 2026-07-28 15:23 by info@stenth.com, with no CLAUDE.md entry.
  Jul-16 had walked it $51 -> $60 -> $95; Jul-28 wiped it to uncapped.

EVIDENCE (code/tcpa_calib.py):
  BMX bids on essentially ONE action: 'Inbound call - Blottman (stenth)'.
  Contact Us / Phone Click are observe-only (0 biddable), so tCPA is
  calibrated directly against the stenth 45s-call CPA.
    Jul 14-27 (tCPA $95):  $947.16 / 15 biddable = $63.14 CPA (stenth $78.93)
    Jul 28-Aug 8 (uncapped): $711.55 / 6 biddable = $118.59 CPA
  Uncapping ~doubled cost per real conversion and halved volume.

WHY $95 and not tighter/looser:
  achieved stenth CPA under the cap was $78.93 -> $95 keeps headroom.
  Targeting at/below achieved is the Jul-06 mistake ($51 vs ~$57 achieved)
  that throttled BMX for 11 days. Uncapped is demonstrably worse ($118.59).
  $95 is also the value the campaign already learned under = least churn.

REVERT: set TARGET_CPA_MICROS back to 0 to return to uncapped
        (not recommended - that is the state this script is fixing).
"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv()
cfg = {
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
}
client = GoogleAdsClient.load_from_dict(cfg)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

BMX = 22979153470
TARGET_CPA_MICROS = 95_000_000

print("--- before ---")
for r in ga.search(customer_id=cid, query=f"""
 SELECT campaign.name, campaign.bidding_strategy_type,
        campaign.maximize_conversions.target_cpa_micros
 FROM campaign WHERE campaign.id = {BMX}"""):
    c = r.campaign
    print(f"  {c.name}: strategy={c.bidding_strategy_type.name} "
          f"tCPA=${c.maximize_conversions.target_cpa_micros/1e6:.2f}")

print(f"\n--- setting BMX tCPA -> ${TARGET_CPA_MICROS/1e6:.2f} ---")
csvc = client.get_service("CampaignService")
op = client.get_type("CampaignOperation")
camp = op.update
camp.resource_name = csvc.campaign_path(cid, BMX)
camp.maximize_conversions.target_cpa_micros = TARGET_CPA_MICROS
op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
try:
    res = csvc.mutate_campaigns(customer_id=cid, operations=[op])
    print(f"  OK: {res.results[0].resource_name}")
except Exception as e:
    print(f"  FAILED: {str(e)[:400]}")

print("\n--- verify ---")
for r in ga.search(customer_id=cid, query=f"""
 SELECT campaign.name, campaign.bidding_strategy_type,
        campaign.maximize_conversions.target_cpa_micros
 FROM campaign WHERE campaign.id = {BMX}"""):
    c = r.campaign
    print(f"  {c.name}: strategy={c.bidding_strategy_type.name} "
          f"tCPA=${c.maximize_conversions.target_cpa_micros/1e6:.2f}")
