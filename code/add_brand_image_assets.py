"""Add visual identity to the consolidated Search campaign (23971101309):
  (1) Leslie's office photo as a SQUARE image asset (the 'images' gap)
  (2) a proper square business logo (the account's only logo was 'fb ad.jpg')
  (3) a business name asset 'Blottman Law'
Each step is isolated so a verification-gated field (name/logo) can't block the
image. Image files are pre-cropped in the scratchpad. Run once.
"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
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
CAMPAIGN = f"customers/{cid}/campaigns/23971101309"
asset_svc = client.get_service("AssetService")
ca_svc = client.get_service("CampaignAssetService")
AFT = client.enums.AssetFieldTypeEnum

SCRATCH = (r"C:\Users\anshr\AppData\Local\Temp\claude\E--Blottman-law"
           r"\028b306a-7825-4963-a52e-795dfafab051\scratchpad")
LESLIE_SQ = SCRATCH + r"\leslie_square_1200.png"
LOGO_SQ = SCRATCH + r"\blottman_logo_square_1200.png"


def make_image_asset(path, name):
    o = client.get_type("AssetOperation")
    a = o.create
    a.name = name
    a.type_ = client.enums.AssetTypeEnum.IMAGE
    with open(path, "rb") as f:
        a.image_asset.data = f.read()
    a.image_asset.mime_type = client.enums.MimeTypeEnum.IMAGE_PNG
    return asset_svc.mutate_assets(customer_id=cid, operations=[o]).results[0].resource_name


def link(asset_rn, field_type, label):
    o = client.get_type("CampaignAssetOperation")
    ca = o.create
    ca.campaign = CAMPAIGN
    ca.asset = asset_rn
    ca.field_type = field_type
    ca_svc.mutate_campaign_assets(customer_id=cid, operations=[o])
    print(f"  OK   linked {label}")


# (1) Leslie square image
try:
    rn = make_image_asset(LESLIE_SQ, "Leslie Office Square (Stenth)")
    link(rn, AFT.SQUARE_MARKETING_IMAGE, "Leslie square image -> SQUARE_MARKETING_IMAGE")
except Exception as e:
    print("  FAIL image (square):", str(e).splitlines()[0][:150])

# (2) business logo
try:
    rn = make_image_asset(LOGO_SQ, "Blottman Logo Square (Stenth)")
    link(rn, AFT.BUSINESS_LOGO, "logo -> BUSINESS_LOGO")
except Exception as e:
    print("  FAIL logo:", str(e).splitlines()[0][:150])

# (3) business name (may be verification-gated)
try:
    o = client.get_type("AssetOperation")
    a = o.create
    a.name = "Blottman Law Business Name"
    a.business_name_asset.business_name = "Blottman Law"
    rn = asset_svc.mutate_assets(customer_id=cid, operations=[o]).results[0].resource_name
    link(rn, AFT.BUSINESS_NAME, "business name 'Blottman Law'")
except Exception as e:
    print("  FAIL business name:", str(e).splitlines()[0][:150])

print("\n  done")
