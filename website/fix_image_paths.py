import re, os

with open("main.js", "r", encoding="utf-8") as f:
    content = f.read()

def get_local_path(url):
    parts = url.split("/")
    filename = parts[-1]
    if len(parts) >= 3:
        prefix = parts[-3]
        filename = f"{prefix}_{filename}"
    local_file = os.path.join("public", "images", "covers", filename)
    if not os.path.exists(local_file):
        print(f"  Missing: {filename} -- using fallback")
        filename = "www.softcoverbooks.co.za_Swart%20Luiperd%20Logo.jpg"
    return f"/images/covers/{filename}"

pattern = r'https://(?:app\.sqrindle\.com|www\.softcoverbooks\.co\.za)/[^\s\'"]+\.jpg'
urls = set(re.findall(pattern, content))

replacements = {}
for url in urls:
    local = get_local_path(url)
    replacements[url] = local
    print(f"{url}\n  -> {local}")

for url, local in replacements.items():
    content = content.replace(url, local)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone. Replaced {len(replacements)} unique URLs.")
