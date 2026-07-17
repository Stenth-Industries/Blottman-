"""VALIDATE-ONLY probe: which qualifying-question TEXTS will Google accept?
Google only allows question text from its own supported library — the June
"vertical restriction" note was wrong. Nothing is created here.
"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
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
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
svc = client.get_service("AssetService")

CHARGES = ["Speeding", "Careless driving", "Stunt driving", "Cell phone / distracted",
           "Suspended licence", "Other moving violation"]

def probe(qtext, answers=CHARGES):
    op = client.get_type("AssetOperation")
    a = op.create
    a.name = "probe"
    lf = a.lead_form_asset
    lf.business_name = "Blottman Legal Services"
    lf.headline = "Fight Your Traffic Ticket"
    lf.description = "Licensed defence for Ontario traffic charges. Free case review."
    lf.call_to_action_type = client.enums.LeadFormCallToActionTypeEnum.GET_QUOTE
    lf.call_to_action_description = "Get your free case review"
    lf.privacy_policy_url = "https://blottman.ca/privacy"
    for ft in ("FULL_NAME", "EMAIL", "PHONE_NUMBER"):
        f = client.get_type("LeadFormField")
        f.input_type = getattr(client.enums.LeadFormFieldUserInputTypeEnum, ft)
        lf.fields.append(f)
    q = client.get_type("LeadFormCustomQuestionField")
    q.custom_question_text = qtext
    for ans in answers:
        q.single_choice_answers.answers.append(ans)
    lf.custom_question_fields.append(q)
    req = client.get_type("MutateAssetsRequest")
    req.customer_id = cid
    req.operations.append(op)
    req.validate_only = True
    try:
        svc.mutate_assets(request=req)
        return True, ""
    except GoogleAdsException as e:
        return False, "; ".join(err.error_code.field_error.name if err.error_code.field_error else str(err.error_code)
                                for err in e.failure.errors)

CANDIDATES = [
    "Which service do you need?",
    "What service are you interested in?",
    "What type of service do you need?",
    "Which service are you interested in?",
    "What service do you need?",
    "How can we help you?",
    "What are you looking for?",
    "What is the reason for your inquiry?",
    "Tell us about your needs",
    "Which product are you interested in?",
    "What type of help do you need?",
    "What is your legal issue?",
    "What were you charged with?",
]

print("=== Which question TEXTS does Google accept? (answers = charge list) ===")
allowed = []
for c in CANDIDATES:
    ok, err = probe(c)
    print(f"  {'ACCEPTED' if ok else 'rejected'}  {c!r}" + ("" if ok else f"   [{err}]"))
    if ok:
        allowed.append(c)

print("\n=== For each ACCEPTED question, do our charge answers survive? ===")
for c in allowed:
    ok, err = probe(c, CHARGES)
    print(f"  {c!r} + 6 charge answers -> {'ACCEPTED' if ok else 'rejected ' + err}")
