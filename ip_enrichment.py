import requests

def enrich_ip(ip):
    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": "YOUR_API_KEY",
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "ip": ip,
            "abuse_score": data["data"]["abuseConfidenceScore"]
        }
    else:
        return {"error": "API call failed"}
