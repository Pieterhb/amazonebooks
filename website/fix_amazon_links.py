"""
Fix all Amazon links in catalog_source.html to the clean /dp/ASIN format.
Removes title slugs, spaces, trailing slashes, extra query params.
Preserves the ASIN and affiliate tag structure.
"""

import re
import os
import shutil
from datetime import datetime

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "catalog_source.html")
BACKUP_PATH = CATALOG_PATH + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def normalize_amazon_url(url):
    """
    Normalize any Amazon URL to: https://www.amazon.com/dp/ASIN
    (no title slug, no trailing slash, no extra params)
    The build process (clean_amazon_url) will add ?tag=softcoverbook-20.
    """
    if 'amazon.com' not in url:
        return url
    
    # Extract ASIN - 10 character alphanumeric after /dp/
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url, re.IGNORECASE)
    if asin_match:
        asin = asin_match.group(1)
        return f"https://www.amazon.com/dp/{asin}"
    
    # Can't normalize - return as-is
    return url

def fix_catalog():
    # Read catalog
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Backup original
    shutil.copy2(CATALOG_PATH, BACKUP_PATH)
    print(f"Backup created: {BACKUP_PATH}")
    
    # Find all Amazon href values and fix them
    pattern = r'(href=")([^"]*amazon\.com[^"]*?)(")'
    
    fixes = 0
    bad_urls = []
    
    def replace_amazon_href(match):
        nonlocal fixes
        prefix = match.group(1)
        url = match.group(2)
        suffix = match.group(3)
        
        normalized = normalize_amazon_url(url)
        if normalized != url:
            fixes += 1
            bad_urls.append((url, normalized))
            return prefix + normalized + suffix
        return match.group(0)
    
    new_content = re.sub(pattern, replace_amazon_href, content)
    
    # Write fixed content
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"\nFixed {fixes} Amazon URLs in catalog_source.html")
    print("\nChanges made:")
    for bad, good in bad_urls:
        print(f"  BAD: {bad}")
        print(f"  FIX: {good}")
        print()
    
    # Verify no bad links remain
    remaining_bad = re.findall(r'href="([^"]*amazon\.com[^"]*?)"', new_content)
    still_bad = []
    for url in remaining_bad:
        # Clean format is exactly: https://www.amazon.com/dp/ASIN (no trailing slash, no params)
        if not re.match(r'^https://www\.amazon\.com/dp/[A-Z0-9]{10}$', url):
            still_bad.append(url)
    
    if still_bad:
        print(f"\nWARNING: {len(still_bad)} URLs could not be normalized:")
        for url in still_bad:
            print(f"  {url}")
    else:
        print("\n✓ All Amazon URLs in catalog_source.html are now in clean /dp/ASIN format.")
    
    return fixes

if __name__ == "__main__":
    fix_catalog()
