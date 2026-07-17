"""Read-only: what does the Google-hosted in-ad lead form ask, and what came through?"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv(r"E:\Blottman-law\.env")
client = GoogleAdsClient.load_from_dict({
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
})
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
def run(q): return list(ga.search(customer_id=cid, query=q))

print("\n=== LEAD FORM ASSET definition (what it asks) ===")
for r in run("""
    SELECT asset.id, asset.name, asset.lead_form_asset.headline,
           asset.lead_form_asset.description,
           asset.lead_form_asset.fields,
           asset.lead_form_asset.custom_question_fields,
           asset.lead_form_asset.call_to_action_type,
           asset.lead_form_asset.post_submit_headline
    FROM asset WHERE asset.type = 'LEAD_FORM'
"""):
    a = r.asset
    lf = a.lead_form_asset
    print(f"  asset {a.id} | {a.name}")
    print(f"    headline: {lf.headline}")
    print(f"    description: {lf.description}")
    print(f"    CTA: {lf.call_to_action_type.name}")
    print("    FIELDS asked:")
    for f in lf.fields:
        print(f"       - {f.input_type.name}")
    print("    CUSTOM QUESTIONS:")
    if not lf.custom_question_fields:
        print("       (none)")
    for q in lf.custom_question_fields:
        print(f"       - {q.custom_question_text}")

print("\n=== Recent in-ad lead form SUBMISSIONS (what people actually sent) ===")
rows = run("""
    SELECT lead_form_submission_data.id,
           lead_form_submission_data.submission_date_time,
           lead_form_submission_data.lead_form_submission_fields,
           campaign.name
    FROM lead_form_submission_data
    ORDER BY lead_form_submission_data.submission_date_time DESC
    LIMIT 12
""")
for r in rows:
    d = r.lead_form_submission_data
    vals = {f.field_type.name: f.field_value for f in d.lead_form_submission_fields}
    print(f"  {d.submission_date_time} | {r.campaign.name[:28]:<28} | {vals}")

print("\n=== Do we have CAMERA / RED LIGHT negatives anywhere? ===")
hits = 0
for r in run("""
    SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type,
           shared_set.name
    FROM shared_criterion
"""):
    t = r.shared_criterion.keyword.text.lower()
    if "camera" in t or "red light" in t or "photo" in t:
        print(f"  FOUND: [{r.shared_criterion.keyword.match_type.name}] {r.shared_criterion.keyword.text}  ({r.shared_set.name})")
        hits += 1
if not hits:
    print("  NONE — no camera/red-light/photo-radar negatives exist.")

print("\n=== Search terms mentioning camera / red light / photo (LAST_30_DAYS) ===")
rows = run("""
    SELECT search_term_view.search_term, campaign.name,
           metrics.impressions, metrics.clicks, metrics.all_conversions
    FROM search_term_view
    WHERE segments.date DURING LAST_30_DAYS
    ORDER BY metrics.clicks DESC
""")
found = 0
for r in rows:
    t = r.search_term_view.search_term.lower()
    if "camera" in t or "red light" in t or "photo" in t:
        print(f"  clk {r.metrics.clicks:>3} | impr {r.metrics.impressions:>4} | conv {r.metrics.all_conversions:.1f} | {r.search_term_view.search_term}  [{r.campaign.name[:24]}]")
        found += 1
if not found:
    print("  (no literal camera/red-light search terms — likely PMAX semantic match or the in-ad form)")
