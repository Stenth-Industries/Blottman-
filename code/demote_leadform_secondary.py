"""Demote the Google-hosted in-ad lead-form action 'Lead form - Submit'
(7645568580) to SECONDARY so bidding optimizes on the website form
('Submit Lead Form' 7173263227) only. Sets primary_for_goal = False.
Website lead action is left Primary. Call actions are untouched."""
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
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
ACTION_ID = "7645568580"  # Lead form - Submit (GOOGLE_HOSTED / LEAD_FORM_SUBMIT)

svc = client.get_service("ConversionActionService")
op = client.get_type("ConversionActionOperation")
ca = op.update
ca.resource_name = svc.conversion_action_path(cid, ACTION_ID)
ca.primary_for_goal = False
op.update_mask.paths.append("primary_for_goal")

resp = svc.mutate_conversion_actions(customer_id=cid, operations=[op])
print("  Updated:", resp.results[0].resource_name)
print("  'Lead form - Submit' (7645568580) -> primary_for_goal = False (SECONDARY)")
