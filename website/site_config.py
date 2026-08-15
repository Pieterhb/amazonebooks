"""
Site Configuration for ebooks.softcoverbooks.co.za
"""

import os

# Base URL for canonical tags, sitemaps, open graph
SITE_URL = "https://ebooks.softcoverbooks.co.za"

# Site Identity
SITE_NAME = "Softcover Books | Vintage Pulp Fiction Kindle Ebooks"
SITE_TITLE_SUFFIX = " | Softcover Books"
SITE_TAGLINE = "Your Gateway to Classic Pulp Fiction Ebooks on Amazon Kindle"
DEFAULT_DESCRIPTION = "Explore over 300+ classic vintage pulp fiction ebooks on Amazon Kindle. Featuring French Foreign Legion desert adventures, swashbuckling pirates, hardboiled detectives, safari mysteries, and retro sci-fi."

# Amazon Affiliate Configuration
# Set your Amazon Associate Tag here (e.g., 'softcoverbook-20')
# Can also be overridden via environment variable AMAZON_AFFILIATE_TAG
AMAZON_AFFILIATE_TAG = os.environ.get("AMAZON_AFFILIATE_TAG", "softcoverbook-20")

# Contact & Publisher Info
PUBLISHER_NAME = "Softcover Books"
PUBLISHER_LOGO = f"{SITE_URL}/favicon.svg"
DEFAULT_OG_IMAGE = f"{SITE_URL}/images/covers/cover_14.jpg"
