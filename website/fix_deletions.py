#!/usr/bin/env python3
"""
Fix TASK4 and TASK5: Delete SA Polisie books 13+ and Swerwer Speurder books 10+
These deletions failed because the file is now read in text mode (LF only after Python conversion)
"""

import re

input_file = r"c:\googleamazon\website\index.html"

# Read with newline='' to preserve original line endings
with open(input_file, "r", encoding="utf-8", newline='') as f:
    content = f.read()

print(f"File length: {len(content)} chars")
print(f"Contains CRLF: {chr(13)+chr(10) in content}")

# ============================================================
# TASK 4: SA Polisie Reeks - Delete books 13 through end
# ============================================================
# Book 13 starts with MONSTER UIT DIE MIS
# After deletion, next is SA Police Series

sa_book13_crlf = '<article class="book-card">\r\n<div class="book-img-wrapper">\r\n<img alt="MONSTER UIT DIE MIS"'
sa_book13_lf = '<article class="book-card">\n<div class="book-img-wrapper">\n<img alt="MONSTER UIT DIE MIS"'
sa_end_crlf = '</div>\r\n</section>\r\n<section class="view" id="sa-police-series">'
sa_end_lf = '</div>\n</section>\n<section class="view" id="sa-police-series">'

pos13 = content.find(sa_book13_crlf)
if pos13 == -1:
    pos13 = content.find(sa_book13_lf)
    print(f"SA Book13 found with LF at pos: {pos13}")
else:
    print(f"SA Book13 found with CRLF at pos: {pos13}")

pos_sa_end = content.find(sa_end_crlf, pos13 if pos13 != -1 else 0)
if pos_sa_end == -1:
    pos_sa_end = content.find(sa_end_lf, pos13 if pos13 != -1 else 0)
    print(f"SA End found with LF at pos: {pos_sa_end}")
else:
    print(f"SA End found with CRLF at pos: {pos_sa_end}")

if pos13 != -1 and pos_sa_end != -1:
    before = content[:pos13]
    after = content[pos_sa_end:]
    content = before + after
    print("TASK4 OK: Removed SA Polisie books 13+")
else:
    # Try searching for context differently - search for MONSTER UIT DIE MIS directly
    idx = content.find('alt="MONSTER UIT DIE MIS"')
    print(f"  Direct search for MONSTER UIT DIE MIS alt: {idx}")
    if idx != -1:
        print(f"  Context: {repr(content[max(0,idx-100):idx+50])}")

# ============================================================
# TASK 5: Swerwer Speurder - Delete books 10+
# ============================================================
ss10_crlf = '<article class="book-card">\r\n<div class="book-img-wrapper">\r\n<img alt="MET \'N DRUPPEL WYN"'
ss10_lf = '<article class="book-card">\n<div class="book-img-wrapper">\n<img alt="MET \'N DRUPPEL WYN"'
ss_end_crlf = '</div>\r\n</section>\r\n<section class="view" id="wanderer-detective-series">'
ss_end_lf = '</div>\n</section>\n<section class="view" id="wanderer-detective-series">'

pos_ss10 = content.find(ss10_crlf)
if pos_ss10 == -1:
    pos_ss10 = content.find(ss10_lf)
    print(f"SS Book10 found with LF at pos: {pos_ss10}")
else:
    print(f"SS Book10 found with CRLF at pos: {pos_ss10}")

pos_ss_end = content.find(ss_end_crlf, pos_ss10 if pos_ss10 != -1 else 0)
if pos_ss_end == -1:
    pos_ss_end = content.find(ss_end_lf, pos_ss10 if pos_ss10 != -1 else 0)
    print(f"SS End found with LF at pos: {pos_ss_end}")
else:
    print(f"SS End found with CRLF at pos: {pos_ss_end}")

if pos_ss10 != -1 and pos_ss_end != -1:
    before = content[:pos_ss10]
    after = content[pos_ss_end:]
    content = before + after
    print("TASK5 OK: Removed Swerwer Speurder books 10+")
else:
    idx = content.find("DRUPPEL WYN")
    print(f"  Direct search for DRUPPEL WYN: {idx}")
    if idx != -1:
        print(f"  Context: {repr(content[max(0,idx-100):idx+50])}")

# Write back preserving line endings
with open(input_file, "w", encoding="utf-8", newline='') as f:
    f.write(content)

print(f"\nFinal file length: {len(content)}")
