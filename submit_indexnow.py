#!/usr/bin/env python3
"""
Bing IndexNow Submission Helper for ebooks.softcoverbooks.co.za
Calls website/submit_indexnow.py or runs directly.
"""
import os
import sys

website_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "website", "submit_indexnow.py")
if os.path.exists(website_script):
    import runpy
    sys.argv[0] = website_script
    runpy.run_path(website_script, run_name="__main__")
else:
    print(f"Error: {website_script} not found.", file=sys.stderr)
    sys.exit(1)
