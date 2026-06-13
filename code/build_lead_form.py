"""Create a HIGH_INTENT lead form asset and attach it to both live Search campaigns.
Anti-junk: HIGH_INTENT filter + required phone + qualifying ticket-type question +
'no parking tickets' copy. Leads land in Google Ads UI (download within 30 days)."""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

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

# resolve the two live Search campaigns by name
rows = list(ga.search(customer_id=cid, query="""
    SELECT campaign.id, campaign.name FROM campaign
    WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'
"""))
targets = {r.campaign.name: r.campaign.id for r in rows}
print("  Live Search campaigns:", targets)

def build_lead_form_op(with_custom_q: bool):
    op = client.get_type("AssetOperation")
    asset = op.create
    asset.name = "Lead Form - Free Case Review (Stenth)"
    lf = asset.lead_form_asset
    lf.business_name = "Blottman Law"
    lf.call_to_action_type = client.enums.LeadFormCallToActionTypeEnum.GET_QUOTE
    lf.call_to_action_description = "Get your free case review"
    lf.headline = "Fight Your Traffic Ticket"
    lf.description = ("Licensed paralegal defence for Ontario speeding, careless driving, "
                      "stunt driving, cell phone & suspended licence charges. Free case review. "
                      "We do not handle parking tickets.")
    lf.privacy_policy_url = "https://blottman.com/privacy-policy"
    lf.post_submit_headline = "Request received!"
    lf.post_submit_description = ("Thank you - we will call you within one business day "
                                  "to review your case.")
    lf.desired_intent = client.enums.LeadFormDesiredIntentEnum.HIGH_INTENT

    f1 = client.get_type("LeadFormField")
    f1.input_type = client.enums.LeadFormFieldUserInputTypeEnum.FULL_NAME
    f2 = client.get_type("LeadFormField")
    f2.input_type = client.enums.LeadFormFieldUserInputTypeEnum.PHONE_NUMBER
    f3 = client.get_type("LeadFormField")
    f3.input_type = client.enums.LeadFormFieldUserInputTypeEnum.EMAIL
    lf.fields.extend([f1, f2, f3])

    if with_custom_q:
        cq = client.get_type("LeadFormCustomQuestionField")
        cq.custom_question_text = "What type of ticket did you receive?"
        cq.single_choice_answers.answers.extend([
            "Speeding", "Careless driving", "Stunt driving / racing",
            "Cell phone / distracted", "Suspended licence", "Other moving violation",
        ])
        lf.custom_question_fields.append(cq)
    return op

asset_svc = client.get_service("AssetService")
asset_rn = None
for attempt, with_q in ((1, True), (2, False)):
    try:
        res = asset_svc.mutate_assets(customer_id=cid, operations=[build_lead_form_op(with_q)])
        asset_rn = res.results[0].resource_name
        print(f"\n  Lead form asset created (custom question: {with_q}): {asset_rn}")
        break
    except GoogleAdsException as e:
        msgs = "; ".join(err.message for err in e.failure.errors)
        print(f"  attempt {attempt} failed: {msgs}")
        if attempt == 2:
            raise

# attach to both Search campaigns
ca_svc = client.get_service("CampaignAssetService")
ops = []
for name, cmp_id in targets.items():
    op = client.get_type("CampaignAssetOperation")
    link = op.create
    link.campaign = f"customers/{cid}/campaigns/{cmp_id}"
    link.asset = asset_rn
    link.field_type = client.enums.AssetFieldTypeEnum.LEAD_FORM
    ops.append(op)
res = ca_svc.mutate_campaign_assets(customer_id=cid, operations=ops)
print(f"  Attached to {len(res.results)} campaigns:")
for name in targets:
    print(f"    - {name}")
print("\n  REMINDER: leads must be downloaded from Google Ads UI (Assets -> Lead forms -> Leads)")
print("  within 30 days of submission. Set a routine (or wire a webhook later).")
