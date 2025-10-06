#!/usr/bin/env python3
import requests

# Test the RapidAPI endpoint without API key first
url = "https://nepalicalendarapi.p.rapidapi.com/festivals"
params = {"year": "2082"}

# Test without key
try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test with mock key
headers = {
    "X-RapidAPI-Key": "test-key",
    "X-RapidAPI-Host": "nepalicalendarapi.p.rapidapi.com"
}

try:
    response = requests.get(url, headers=headers, params=params, timeout=10)
    print(f"\nWith headers - Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error with headers: {e}")