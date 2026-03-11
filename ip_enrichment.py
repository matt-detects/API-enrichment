# Usage:
# Set API key once in your shell session
# export ABUSEIPDB_API_KEY=your_key_here

import os
import requests
from ipaddress import ip_address, AddressValueError

ABUSEIPDB_URL   = "https://api.abuseipdb.com/api/v2/check"
REQUEST_TIMEOUT = 10   # seconds — always set a timeout

def validate_ip(ip):
    """Return True if ip is a valid, publicly routable IP address."""
    try:
        parsed = ip_address(ip)
    except (AddressValueError, ValueError):
        return False, f"'{ip}' is not a valid IP address"

    if parsed.is_private or parsed.is_loopback or parsed.is_reserved:
        return False, f"{ip} is a private/reserved address — AbuseIPDB won't have data for it"

    return True, ""

def enrich_ip(ip):
    # Load API key from environment variable, not hardcoded in source
    api_key = os.environ.get("ABUSEIPDB_API_KEY")
    if not api_key:
        print("Error: ABUSEIPDB_API_KEY environment variable is not set.")
        print("Set it with: export ABUSEIPDB_API_KEY=your_key_here")
        return None

    # Validate before making the request
    valid, reason = validate_ip(ip)
    if not valid:
        print(f"Skipping {ip}: {reason}")
        return None

    headers = {
        "Key":    api_key,
        "Accept": "application/json",
    }
    params = {
        "ipAddress":    ip,
        "maxAgeInDays": 90,
    }

    try:
        response = requests.get(
            ABUSEIPDB_URL,
            headers=headers,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {REQUEST_TIMEOUT}s for {ip}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to AbuseIPDB — check your network")
        return None

    # Handle specific error codes so you know what actually went wrong
    if response.status_code == 401:
        print("Error: API key was rejected (401) — check ABUSEIPDB_API_KEY is correct")
        return None
    if response.status_code == 422:
        print(f"Error: AbuseIPDB rejected '{ip}' as invalid (422)")
        return None
    if response.status_code == 429:
        print("Error: Rate limit hit (429) — you may have exhausted your daily quota")
        return None
    if response.status_code != 200:
        print(f"Error: Unexpected response status {response.status_code} for {ip}")
        return None

    # Guard against unexpected response structure
    try:
        data = response.json()["data"]
    except (ValueError, KeyError):
        print(f"Error: Could not parse AbuseIPDB response for {ip}")
        return None

    return {
        "ip":               ip,
        "abuse_score":      data.get("abuseConfidenceScore"),
        "country_code":     data.get("countryCode"),
        "isp":              data.get("isp"),
        "domain":           data.get("domain"),
        "total_reports":    data.get("totalReports"),
        "last_reported_at": data.get("lastReportedAt"),
        "is_whitelisted":   data.get("isWhitelisted"),
        "is_tor":           data.get("isTor"),
    }

if __name__ == "__main__":
    result = enrich_ip("185.220.101.5")
    if result:
        for key, value in result.items():
            print(f"{key}: {value}")
