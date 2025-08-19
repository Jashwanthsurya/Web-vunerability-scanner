import requests
from bs4 import BeautifulSoup

def tiny_scanner():
    print("Hi! I'm a tiny web safety checker robot 🤖")
    url = input("Paste the website address you own or a training site URL: ").strip()

    if not url.startswith("http"):
        url = "http://" + url  # add http if missing

    print("\n🔍 Scanning:", url)

    try:
        response = requests.get(url, timeout=10)
        print("✅ Status Code:", response.status_code)
    except Exception as e:
        print("❌ Error fetching the site:", e)
        return

    # --- Page Title ---
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title else "No title found"
    print("📄 Page Title:", title)

    # --- HTTPS Check ---
    if url.startswith("https://"):
        print("🔒 Secure Connection (HTTPS)")
    else:
        print("⚠️ Not using HTTPS (data may be insecure!)")

    # --- Security Headers ---
    print("\n🛡️ Security Headers Check:")
    security_headers = ["Content-Security-Policy", "X-Frame-Options", 
                        "Strict-Transport-Security", "X-Content-Type-Options"]
    for header in security_headers:
        if header in response.headers:
            print(f"  ✅ {header}: {response.headers[header]}")
        else:
            print(f"  ⚠️ Missing {header}")

    # --- Form Check ---
    forms = soup.find_all("form")
    if forms:
        print(f"\n📝 Found {len(forms)} form(s) on the page.")
        for i, form in enumerate(forms, start=1):
            action = form.get("action", "No action")
            method = form.get("method", "GET").upper()
            print(f"   Form {i}: method={method}, action={action}")
            if method == "GET":
                print("   ⚠️ Uses GET (not secure for passwords)")
    else:
        print("\n📝 No forms found.")

    print("\n✅ Scan complete!")

if __name__ == "__main__":
    tiny_scanner()
