"""Tests the Google Ads API connection.

Reads creds from .env, pulls one campaign to confirm everything works.
"""

from dotenv import load_dotenv
import os
from google.ads.googleads.client import GoogleAdsClient

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
ga_service = client.get_service("GoogleAdsService")

customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
query = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        metrics.impressions,
        metrics.clicks,
        metrics.ctr,
        metrics.average_cpc,
        metrics.cost_micros,
        metrics.conversions,
        metrics.cost_per_conversion,
        metrics.conversions_value
    FROM campaign
    WHERE campaign.status = 'ENABLED'
      AND segments.date DURING LAST_30_DAYS
"""

response = ga_service.search(customer_id=customer_id, query=query)
print(f"\n{'Campaign':<35} {'Impressions':>12} {'Clicks':>8} {'CTR':>7} {'Avg CPC':>9} {'Spend':>10} {'Conv':>7} {'CPA':>10} {'Conv Value':>12} {'ROAS':>7}")
print("-" * 125)
for row in response:
    m = row.metrics
    spend = m.cost_micros / 1_000_000
    avg_cpc = m.average_cpc / 1_000_000 if m.clicks else 0
    cpa = m.cost_per_conversion / 1_000_000 if m.conversions else 0
    roas = m.conversions_value / spend if spend else 0
    print(
        f"  {row.campaign.name:<33} "
        f"{m.impressions:>12,} "
        f"{m.clicks:>8,} "
        f"{m.ctr*100:>6.2f}% "
        f"${avg_cpc:>8.2f} "
        f"${spend:>9.2f} "
        f"{m.conversions:>7.1f} "
        f"${cpa:>9.2f} "
        f"${m.conversions_value:>11.2f} "
        f"{roas:>7.2f}x"
    )
