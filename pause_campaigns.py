import requests
import json

CLIENT_ID = ''
PROFILE_ID = ''
CLIENT_SECRET = ''
REFRESH_TOKEN = ('')

def get_access_token(client_id, client_secret, refresh_token):
    token_url = "https://api.amazon.com/auth/o2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Failed to obtain access token: {response.status_code} - {response.text}")
        return None


def pause_campaigns(access_token, profile_id, campaign_ids):
    for campaign_id in campaign_ids:
        url = "https://advertising-api.amazon.com/sp/campaigns"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Amazon-Advertising-API-ClientId': CLIENT_ID,
            'Amazon-Advertising-API-Scope': profile_id,
            'Content-Type': 'application/vnd.spcampaign.v3+json',
            'Accept': 'application/vnd.spcampaign.v3+json',
            'Prefer': 'return=representation'
        }
        payload = {
            "campaigns": [
                {"campaignId": campaign_id, "state": "PAUSED"}
                for campaign_id in campaign_ids
            ]
        }
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 207:
            print(f"Successfully paused campaign {campaign_id}")
        else:
            print(f"Failed to pause campaign {campaign_id}: {response.status_code} - {response.text}")

campaign_ids_to_pause = [
    '315255339089650',   # UBK Bed Frames | SP | Manual | "platform bed" phrase | AH
    '418379906041310',   # Marriott Pad | SP | Auto | All Match Types | AH
    '416785644046961',   # Sanford HB | SP | Auto | All Match Types
    '380191754017916',   # Jacquard Pillows | SP | Auto | All Match Types | AH
    '496923053226697',   # Snap Beds | SP | Auto | All Match Types | AH
    '495950145156294',   # UBK Bed Frames | SP | Auto | All Match Types | AH
    '430047458106039',   # Extra Thick Bamboo Pad | SP | Auto | All Match Types | AH
    '512454777583541',   # Snap Bed Mega Listing | SP | Manual | All Other KWs | AH
    '514520043711934',   # LiveSmart Fabric | SP | Auto | All Match Types | AH
    '477383971163806',   # Non LiveSmart Fabric | SP | Manual | Top 10 KWs | AH
    '474410404079186',    # Bed Frames | SP | Auto | CA | AH
    '326120897587568',   # Chevron Bed | SP | Auto | Close Match | AH
    '364474998509496',   # Marriott Pad | SP | Manual | Size Specific KWs | AH
    '446752927022629',   # Bamboo Pad | SP | Auto | Close Match | AH
    '421612140122582',   # Chevron Bed | SP | Auto | Loose/Comp/Sub Match Types | AH
    '484966078057126',   # Mattress Pads | Auto | Mattress Pads CA | AH
    '304984303746832',   # Slant Chair | SP | Auto | All Match Types | AH
    '487393207749903'    # Slant Chairs | SP | Manual | "Modern Chair" + "Accent Chair" Root | AH
]

access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
if access_token:
    pause_campaigns(access_token, PROFILE_ID, campaign_ids_to_pause)
