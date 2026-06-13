"""Side-by-side config audit: 'Traffic ticket lawyer' (23002273381) vs
'Traffic ticket lawyer broad' (23039650759): geo, bidding/CPC cap, shared neg lists,
ads, keywords (incl. DUI/off-practice), to confirm TTL is safe at $15/day."""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
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
def run(q): return list(ga.search(customer_id=cid, query=q))

CAMPS = {23002273381: "Traffic ticket lawyer", 23039650759: "Traffic ticket lawyer broad"}

for cmp_id, label in CAMPS.items():
    print(f"\n{'='*70}\n  {label} ({cmp_id})\n{'='*70}")

    rows = run(f"""
        SELECT campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros,
               campaign.geo_target_type_setting.positive_geo_target_type,
               campaign.network_settings.target_search_network,
               campaign.network_settings.target_content_network
        FROM campaign WHERE campaign.id = {cmp_id}
    """)
    c = rows[0].campaign
    print(f"  bidding={c.bidding_strategy_type.name}  "
          f"cpc_ceiling=${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f}  "
          f"geo_type={c.geo_target_type_setting.positive_geo_target_type.name}")
    print(f"  search_partners={c.network_settings.target_search_network}  "
          f"display_network={c.network_settings.target_content_network}")

    rows = run(f"""
        SELECT campaign_criterion.location.geo_target_constant,
               campaign_criterion.negative, campaign_criterion.type
        FROM campaign_criterion
        WHERE campaign.id = {cmp_id} AND campaign_criterion.type = 'LOCATION'
    """)
    geos = [r.campaign_criterion for r in rows]
    ids = [g.location.geo_target_constant.split("/")[-1] for g in geos]
    names = {}
    if ids:
        gt = run("SELECT geo_target_constant.resource_name, geo_target_constant.name "
                 "FROM geo_target_constant WHERE geo_target_constant.id IN (" + ",".join(ids) + ")")
        names = {r.geo_target_constant.resource_name: r.geo_target_constant.name for r in gt}
    print(f"  GEO ({len(geos)}): " + (", ".join(
        ("-" if g.negative else "") + names.get(g.location.geo_target_constant, "?")
        for g in geos) if geos else "!! NONE — serves wherever Google decides !!"))

    rows = run(f"""
        SELECT shared_set.name FROM campaign_shared_set
        WHERE campaign.id = {cmp_id} AND campaign_shared_set.status = 'ENABLED'
    """)
    print("  SHARED NEG LISTS: " + (", ".join(r.shared_set.name for r in rows) or "!! NONE !!"))

    rows = run(f"""
        SELECT ad_group.name, ad_group_ad.status, ad_group_ad.policy_summary.approval_status,
               ad_group_ad.ad.id, ad_group_ad.ad_strength
        FROM ad_group_ad
        WHERE campaign.id = {cmp_id} AND ad_group_ad.status != 'REMOVED'
    """)
    print(f"  ADS ({len(rows)}):")
    for r in rows:
        print(f"    [{r.ad_group.name[:24]:24}] ad {r.ad_group_ad.ad.id} {r.ad_group_ad.status.name:7} "
              f"{r.ad_group_ad.policy_summary.approval_status.name:16} strength={r.ad_group_ad.ad_strength.name}")

    rows = run(f"""
        SELECT ad_group.name, ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type, ad_group_criterion.status,
               metrics.impressions
        FROM keyword_view
        WHERE campaign.id = {cmp_id} AND ad_group_criterion.status = 'ENABLED'
          AND segments.date DURING LAST_30_DAYS
    """)
    kws = {}
    for r in rows:
        k = (r.ad_group_criterion.keyword.text, r.ad_group_criterion.keyword.match_type.name)
        kws[k] = kws.get(k, 0) + r.metrics.impressions
    print(f"  ENABLED KEYWORDS: {len(kws)}")
    flagged = [k for k in kws if any(w in k[0].lower() for w in
               ("dui", "impaired", "criminal", "dwi", "drunk", "parking"))]
    if flagged:
        print("  !! OFF-PRACTICE KEYWORDS:")
        for k in flagged:
            print(f"     [{k[1][:3]}] {k[0]}  (impr30d={kws[k]})")
    top = sorted(kws.items(), key=lambda x: -x[1])[:10]
    print("  top by 30d impressions:")
    for (text, mt), impr in top:
        print(f"     [{mt[:3]}] {text[:45]:45} {impr:>5}")
