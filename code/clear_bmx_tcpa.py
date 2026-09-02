"""Remove the $95 Target CPA from BMX; run plain Maximize Conversions.

CONTEXT (2026-09-02):
  BMX has produced 0 conversions Aug 26 - Sep 1 (7 days, ~$240) and only
  4 in the last 14 days. Aug-19 set the contingency: "if a 3rd near-zero
  day occurs, remove the $95 tCPA and run plain Maximize Conversions."
  We are well past three.

WHY THIS REVERSES restore_bmx_tcpa.py (2026-08-09), which argued FOR $95:
  That script was right on its evidence and is wrong on today's. Two things
  changed underneath it.
  1. VOLUME. On Aug-09 BMX had 15 biddable conv/14d, enough for tCPA to
     steer. It now has 4 (~8/mo vs the ~30/mo tCPA needs). Below that
     threshold a target does not optimise, it only throttles: it bids
     conservatively into a target it cannot reach, which cuts volume,
     which yields fewer conversions.
  2. THE SIGNAL IT WAS CALIBRATED ON IS GONE. $95 came from the stenth
     45s-call CPA. stenth has been dark since Aug-14 and Contact Us died
     (correctly) at the .ca migration. Since Aug-17 every BMX conversion
     is 'Submit Lead Form - STENTH'. The target is anchored to a signal
     that no longer contributes.
  So the Jul-28 uncapping was bad THEN (it removed a working target at
  healthy volume) and removing it is right NOW (the target is strangling
  a campaign too thin to feed it). Same action, different regime.

RULED OUT FIRST (read-only, this session):
  - Landing pages: last 14d BMX traffic is 100% blottman.ca, 0 blottman.com
    (landing_page_view). The Aug-13 migration held; FUE is not leaking.
  - Copy: all 24 enabled text assets clean (no lawyer/98%/paralegal).
  - Policy: every enabled asset APPROVED with 0 policy_topic_entries.
    ASSET_GROUP_LIMITED is the documented COMMISSION_OF_A_CRIME residual,
    no violation behind it to fix.
  - Change history (28d): no unlogged change touched BMX. Last edit was
    Aug-13 23:09 (asset automation opt-out).

REVERT: set TARGET_CPA_MICROS = 95_000_000 (or run restore_bmx_tcpa.py).
WATCH:  volume over ~1 week. Expect wider CPA variance; that is the trade.
        If cost/conversion runs away with volume restored, reintroduce a
        target calibrated on the FORM CPA, not the old call CPA.
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
TARGET_CPA_MICROS = 0          # 0 = no target, plain Maximize Conversions

Q = f"""SELECT campaign.name, campaign.bidding_strategy_type,
        campaign.maximize_conversions.target_cpa_micros,
        campaign_budget.amount_micros
 FROM campaign WHERE campaign.id = {BMX}"""


def show(label):
    print(f"--- {label} ---")
    for r in ga.search(customer_id=cid, query=Q):
        c = r.campaign
        t = c.maximize_conversions.target_cpa_micros
        print(f"  {c.name}: strategy={c.bidding_strategy_type.name} "
              f"tCPA={'(none)' if t == 0 else f'${t/1e6:.2f}'} "
              f"budget=${r.campaign_budget.amount_micros/1e6:.2f}/day")


show("before")
print("\n--- clearing BMX tCPA (-> plain Maximize Conversions) ---")
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
    raise SystemExit(1)

print()
show("verify")
