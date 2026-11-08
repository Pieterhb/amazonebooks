#!/usr/bin/env python3
"""
Bing IndexNow Submission Helper for ebooks.softcoverbooks.co.za

Submits URLs to IndexNow (Bing, Yandex, Seznam, Naver) for immediate discovery and indexing.
Specification: https://www.indexnow.org/documentation
"""

import sys
import os
import re
import json
import argparse
import urllib.request
import urllib.error

INDEXNOW_API_ENDPOINT = "https://api.indexnow.org/IndexNow"
DEFAULT_HOST = "ebooks.softcoverbooks.co.za"
DEFAULT_KEY = "bc56a5896c0f4892bb71c444fc8123eb"
DEFAULT_KEY_LOCATION = f"https://{DEFAULT_HOST}/{DEFAULT_KEY}.txt"
BATCH_SIZE = 10000  # IndexNow max URLs per submission payload

DEFAULT_URLS = [
    f"https://{DEFAULT_HOST}/",
    f"https://{DEFAULT_HOST}/books/",
    f"https://{DEFAULT_HOST}/authors/",
    f"https://{DEFAULT_HOST}/genres/",
    f"https://{DEFAULT_HOST}/themes/",
    f"https://{DEFAULT_HOST}/collections/",
    f"https://{DEFAULT_HOST}/series/",
]

STATUS_DESCRIPTIONS = {
    200: "200 OK: URLs successfully submitted and indexed/validated.",
    202: "202 Accepted: URL submission received; IndexNow key validation pending or queued.",
    400: "400 Bad Request: Invalid payload or request syntax.",
    403: "403 Forbidden: Key not valid (key not found at keyLocation or key mismatch).",
    422: "422 Unprocessable Entity: In-payload URLs do not match the specified host.",
    429: "429 Too Many Requests: Rate limit exceeded.",
}


def extract_urls_from_sitemap(sitemap_path: str) -> list[str]:
    """Extract <loc> URLs from a sitemap XML file."""
    if not os.path.isfile(sitemap_path):
        return []
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    return re.findall(r"<loc>(https?://[^<]+)</loc>", content)


def collect_sitemap_urls(base_dir: str) -> list[str]:
    """Collect all unique URLs from sitemap files in the directory."""
    sitemap_files = [
        "sitemap-pages.xml",
        "sitemap-books.xml",
        "sitemap-authors.xml",
        "sitemap-genres.xml",
        "sitemap-series.xml",
        "sitemap-themes.xml",
        "sitemap-collections.xml",
    ]
    all_urls = []
    seen = set()

    for s_file in sitemap_files:
        for candidate_dir in [base_dir, os.path.join(base_dir, "public")]:
            target_path = os.path.join(candidate_dir, s_file)
            if os.path.exists(target_path):
                urls = extract_urls_from_sitemap(target_path)
                for u in urls:
                    if u not in seen:
                        seen.add(u)
                        all_urls.append(u)
                break

    return all_urls


def submit_batch(host: str, key: str, key_location: str, url_list: list[str]) -> bool:
    """Send a batch of URLs to IndexNow."""
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": url_list,
    }

    data = json.dumps(payload, indent=2).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "IndexNow-Submitter/1.0",
    }

    req = urllib.request.Request(INDEXNOW_API_ENDPOINT, data=data, headers=headers, method="POST")

    print(f"Submitting {len(url_list)} URLs to IndexNow ({INDEXNOW_API_ENDPOINT})...")
    print(f"Host: {host}")
    print(f"Key: {key}")
    print(f"Key Location: {key_location}")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.getcode()
            body = resp.read().decode("utf-8", errors="replace")
            desc = STATUS_DESCRIPTIONS.get(code, f"HTTP {code}")
            print(f"[SUCCESS] Response status: {desc}")
            if body.strip():
                print(f"Response body: {body.strip()}")
            return True
    except urllib.error.HTTPError as e:
        code = e.code
        body = e.read().decode("utf-8", errors="replace")
        desc = STATUS_DESCRIPTIONS.get(code, f"HTTP {code}")
        print(f"[HTTP {code}] {desc}", file=sys.stderr)
        if body.strip():
            print(f"Response body: {body.strip()}", file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(f"[ERROR] Connection error: {e.reason}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Submit URLs to Bing IndexNow.")
    parser.add_argument("urls", nargs="*", help="Optional URLs to submit. If omitted, default URLs are submitted.")
    parser.add_argument("--sitemaps", action="store_true", help="Submit all URLs extracted from project sitemaps.")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Domain host (default: {DEFAULT_HOST})")
    parser.add_argument("--key", default=DEFAULT_KEY, help=f"IndexNow API key (default: {DEFAULT_KEY})")
    parser.add_argument("--key-location", default=DEFAULT_KEY_LOCATION, help=f"Key location URL (default: {DEFAULT_KEY_LOCATION})")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if args.urls:
        urls_to_submit = args.urls
    elif args.sitemaps:
        urls_to_submit = collect_sitemap_urls(script_dir)
        if not urls_to_submit:
            print("[WARN] No sitemap URLs found. Falling back to default top-level pages.")
            urls_to_submit = DEFAULT_URLS
    else:
        urls_to_submit = DEFAULT_URLS

    print(f"Found {len(urls_to_submit)} URL(s) to submit.")

    # Submit in batches
    success_all = True
    for i in range(0, len(urls_to_submit), BATCH_SIZE):
        batch = urls_to_submit[i : i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = ((len(urls_to_submit) - 1) // BATCH_SIZE) + 1
        if total_batches > 1:
            print(f"\n--- Batch {batch_num}/{total_batches} ({len(batch)} URLs) ---")
        ok = submit_batch(args.host, args.key, args.key_location, batch)
        if not ok:
            success_all = False

    if success_all:
        print("\nAll IndexNow submissions completed successfully.")
        sys.exit(0)
    else:
        print("\nSome or all IndexNow submissions reported errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
