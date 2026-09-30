api_fuzzer.py
"""
API Endpoint Fuzzer
Discovers hidden or common API endpoints by appending common suffixes and paths.
Useful for finding undocumented API routes.
"""
import requests
from urllib.parse import urljoin

# Common API path variations
paths = [
    "/api/v1/users",
    "/api/users",
    "/v1/users",
    "/users",
    "/admin",
    "/admin/users",
    "/api/v1/data",
    "/data",
    "/graphql",
    "/api",
    "/rest",
    "/dashboard",
    "/status"
]

def fuzz_api(base_url):
    print(f"[*] Fuzzing API endpoints for: {base_url}")
    print("-" * 40)

    for path in paths:
        target_url = urljoin(base_url, path)
        try:
            response = requests.get(target_url, timeout=5)
            status_code = response.status_code
            
            # Highlight successful endpoints (2xx) and interesting ones (4xx/5xx)
            if status_code == 200:
                print(f"[+] {target_url} (200 OK)")
                if len(response.content) < 500:
                    print(f"    Content: {response.text[:100]}")
            elif status_code == 401:
                print(f"[?] {target_url} (401 Unauthorized - Likely working API)")
            elif status_code == 404:
                pass # Not found, skip
            elif status_code >= 500:
                print(f"[!] {target_url} (500+ Error - Possible bug)")
        except requests.RequestException:
            pass

if __name__ == "__main__":
    base = input("Enter base URL (e.g., http://target.com): ")
    fuzz_api(base)