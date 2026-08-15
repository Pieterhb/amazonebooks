#!/usr/bin/env python3
"""
Apply all requested changes to index.html
"""

import re
import shutil

input_file = r"c:\googleamazon\website\index.html"
backup_file = r"c:\googleamazon\website\index_backup_before_changes.html"

# Backup
shutil.copy2(input_file, backup_file)
print(f"Backup created: {backup_file}")

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

original_len = len(content)

# ============================================================
# TASK 1: Remove red circle from SAHARA AVONTUUR OMNIBUS + update link
# ============================================================
old_sahara_img = (
    '<img alt="SAHARA AVONTUUR OMNIBUS - 3 EBOEKE" loading="lazy" src="/images/covers/cover_14.jpg"/>'
    '<span class="book-number" style="background-color: #ff0000; color: #ffffff;">1</span>'
)
new_sahara_img = (
    '<img alt="SAHARA AVONTUUR OMNIBUS - 3 EBOEKE" loading="lazy" src="/images/covers/cover_14.jpg"/>'
)

if old_sahara_img in content:
    content = content.replace(old_sahara_img, new_sahara_img, 1)
    print("TASK1 ✓ Removed red circle from SAHARA AVONTUUR OMNIBUS")
else:
    print("TASK1 ✗ Could not find SAHARA AVONTUUR OMNIBUS red circle span")

# Update link for SAHARA AVONTUUR OMNIBUS
old_sahara_btn = (
    '<a class="btn btn-primary" href="https://www.amazon.com/dp/B0FF57BLSC/" rel="noopener" target="_blank">View Book</a>'
)
new_sahara_btn = (
    '<a class="btn btn-primary" href="https://www.amazon.com/Sahara-Avontuur-Omnibus-Eboeke-Afrikaans-ebook/dp/B0FF56LSBW/" rel="noopener" target="_blank">View Book</a>'
)

if old_sahara_btn in content:
    content = content.replace(old_sahara_btn, new_sahara_btn, 1)
    print("TASK1 ✓ Updated SAHARA AVONTUUR OMNIBUS link")
else:
    print("TASK1 ✗ Could not find SAHARA AVONTUUR OMNIBUS link to update")

# ============================================================
# TASK 2: Remove red circle from THE MASKED ROBBER BOX SET
# ============================================================
old_masked_img = (
    '<img alt="1. THE MASKED ROBBER BOX SET - 3 EBOOKS" loading="lazy" src="/images/covers/cover_182.jpg"/>'
    '<span class="book-number" style="background-color: #ff0000; color: #ffffff;">1</span>'
)
new_masked_img = (
    '<img alt="1. THE MASKED ROBBER BOX SET - 3 EBOOKS" loading="lazy" src="/images/covers/cover_182.jpg"/>'
)

if old_masked_img in content:
    content = content.replace(old_masked_img, new_masked_img, 1)
    print("TASK2 ✓ Removed red circle from THE MASKED ROBBER BOX SET")
else:
    print("TASK2 ✗ Could not find THE MASKED ROBBER BOX SET red circle span")

# ============================================================
# TASK 3: Remove red circle from OLOFF DIE SEEROWER OMNIBUS
# ============================================================
old_oloff_img = (
    '<img alt="OLOFF DIE SEEROWER OMNIBUS - 3 EBOEKE" loading="lazy" src="/images/covers/cover_203.jpg"/>'
    '<span class="book-number" style="background-color: #ff0000; color: #ffffff;">1</span>'
)
new_oloff_img = (
    '<img alt="OLOFF DIE SEEROWER OMNIBUS - 3 EBOEKE" loading="lazy" src="/images/covers/cover_203.jpg"/>'
)

if old_oloff_img in content:
    content = content.replace(old_oloff_img, new_oloff_img, 1)
    print("TASK3 ✓ Removed red circle from OLOFF DIE SEEROWER OMNIBUS")
else:
    print("TASK3 ✗ Could not find OLOFF DIE SEEROWER OMNIBUS red circle span")

# ============================================================
# TASK 4: SA Polisie Reeks - Delete books 13 through end
# ============================================================
# Find book 13 "MONSTER UIT DIE MIS" article start
sa_book13_marker = '<article class="book-card">\r\n<div class="book-img-wrapper">\r\n<img alt="MONSTER UIT DIE MIS"'
# End marker: the closing </div></section> of SA Polisie, followed by SA Police Series section
sa_end_marker = '</div>\r\n</section>\r\n<section class="view" id="sa-police-series">'

pos_book13 = content.find(sa_book13_marker)
pos_end = content.find(sa_end_marker, pos_book13 if pos_book13 != -1 else 0)

print(f"TASK4 Book13 pos: {pos_book13}, End pos: {pos_end}")

if pos_book13 != -1 and pos_end != -1:
    before = content[:pos_book13]
    after = content[pos_end:]
    content = before + after
    print("TASK4 ✓ Removed SA Polisie Reeks books 13+")
else:
    print(f"TASK4 ✗ Could not find SA Polisie deletion range")

# Update SA Polisie Reeks count in section header (was 30, now 12)
old_count = '<p>Explore the complete collection of 30 books in this series.</p>'
new_count = '<p>Explore the complete collection of 12 books in this series.</p>'
if old_count in content:
    content = content.replace(old_count, new_count, 1)
    print("TASK4 ✓ Updated SA Polisie count to 12")

# Update sidebar count
content = content.replace(
    'SA Polisie Reeks <span class="count">(30)</span>',
    'SA Polisie Reeks <span class="count">(12)</span>',
    1
)

# ============================================================
# TASK 5: Swerwer Speurder - Delete books 10+
# ============================================================
ss_book10_marker = "<article class=\"book-card\">\r\n<div class=\"book-img-wrapper\">\r\n<img alt=\"MET 'N DRUPPEL WYN\""
ss_end_marker = '</div>\r\n</section>\r\n<section class="view" id="wanderer-detective-series">'

pos_ss10 = content.find(ss_book10_marker)
pos_ss_end = content.find(ss_end_marker, pos_ss10 if pos_ss10 != -1 else 0)

print(f"TASK5 SS Book10 pos: {pos_ss10}, SS End pos: {pos_ss_end}")

if pos_ss10 != -1 and pos_ss_end != -1:
    before = content[:pos_ss10]
    after = content[pos_ss_end:]
    content = before + after
    print("TASK5 ✓ Removed Swerwer Speurder books 10+")
else:
    print(f"TASK5 ✗ Could not find Swerwer Speurder deletion range")

# Update Swerwer Speurder count (was 16, now 9)
old_ss_count = '<p>Explore the complete collection of 16 books in this series.</p>'
new_ss_count = '<p>Explore the complete collection of 9 books in this series.</p>'
if old_ss_count in content:
    content = content.replace(old_ss_count, new_ss_count, 1)
    print("TASK5 ✓ Updated Swerwer Speurder count to 9")

content = content.replace(
    'Swerwer Speurder Reeks <span class="count">(16)</span>',
    'Swerwer Speurder Reeks <span class="count">(9)</span>',
    1
)

# ============================================================
# TASK 5b: Update links for various books
# Using exact titles from the HTML
# ============================================================
def update_book_link(content, exact_title, new_url):
    """Find book card with exact h3 title and update the View Book link href."""
    h3_escaped = re.escape(exact_title)
    # Pattern matches from article start through h3, then finds the next href in the card
    pattern = r'(<article class="book-card">.*?<h3>' + h3_escaped + r'</h3>.*?<a class="btn btn-primary" href=")[^"]*(")'
    replacement = r'\g<1>' + new_url + r'\g<2>'
    new_content, count = re.subn(pattern, replacement, content, count=1, flags=re.DOTALL)
    if count > 0:
        print(f"  LINK ✓ Updated: {exact_title}")
    else:
        print(f"  LINK - Not found: {exact_title}")
    return new_content

# Exact title -> new URL mapping (using exact title strings from HTML)
link_updates = [
    # Sahara Avontuur Reeks
    ("DIE VERRAAIER VAN DINI-SALAM", "https://www.amazon.com/dp/B0F48T9FVN/"),
    # Sahara Adventure Series (English equivalent)
    ("THE TRAITOR OF DINI SALAM", "https://www.amazon.com/dp/B0F6329BR7"),
    ("DIE VERRAAIER", "https://www.amazon.com/dp/B0F7J6DC9Z"),
    ("VLAM VAN DIE LAEVELD", "https://www.kobo.com/ww/en/ebook/vlam-van-die-laeveld?sId=c013af80-c4a7-48a8-be19-3280c1d77dcc&ssId=g44TicNl0mVdMaahOFQ7c"),
    ("DIE POORT VAN TRANE", "https://www.kobo.com/ww/en/ebook/die-poort-van-trane?sId=2a6357b6-180a-43e5-a501-36d740f33d75&ssId=f1e8APRkm1v98p6mToGzu"),
    ("BEMINDE VERRAAIER", "https://www.kobo.com/ww/en/ebook/beminde-verraaier?sId=dff846d8-0d49-4222-9853-99bd7683e09a&ssId=onAoeCpqfvwhekePOqvKM"),
    ("SPORE IN DIE DOU", "https://www.kobo.com/ww/en/ebook/spore-in-die-dou?sId=bd99605a-abcd-40ef-a445-750c661aac5f&ssId=G0wI-IT9D_vBb_5PugBLO"),
    ("GEEN VERGIFFENIS", "https://www.kobo.com/ww/en/ebook/geen-vergiffenis?sId=190b335e-be58-4dd7-871c-05b86ff11cd0&ssId=n4J06SgyIaW3v9uv_IdMu"),
    ("HOEFSLAE TEEN MIDDERNAG", "https://www.kobo.com/ww/en/ebook/hoefslae-teen-middernag?sId=36a50306-23c8-4a7b-8c7c-af17e29b3d60&ssId=2PYEuFyEqqb_awGQdLlv_"),
    ("RUITERS VAN DIE DOOD", "https://www.kobo.com/ww/en/ebook/ruiters-van-die-dood?sId=4dbde55b-b685-46e8-80f3-3c6aa76d0597&ssId=ncdC_8SRdWkdnwSJW8sbV"),
    # Oerwoudvalk Reeks (exact title is "1. OERWOUDVALK OMNIBUS - 3 EBOEKE")
    ("1. OERWOUDVALK OMNIBUS - 3 EBOEKE", "https://www.kobo.com/ww/en/ebook/oerwoudvalk-omnibus?sId=2f84c095-9373-46a2-82ca-8cfcb5fa6c01&ssId=ScpeyCtuGwYFIsdRX19l2"),
    ("GOUDSTAD VAN SKEBA", "https://www.kobo.com/ww/en/ebook/goudstad-van-skeba?sId=daef186d-17cc-4155-861c-1ec21542faa4&ssId=dcidrR5lzueIIH-srbor3"),
    ("DIE SEEKAT", "https://www.kobo.com/ww/en/ebook/die-seekat?sId=13e15195-6bfe-4e29-ab34-9425fafb4bb4&ssId=d1n1H-UtiPqPlA4VlOpUD"),
    ("OERVALLEI", "https://www.kobo.com/ww/en/ebook/oervallei?sId=6b56eb72-0727-4996-b222-d6f92fea86e0&ssId=OWGe66SuFi2jS3xldJIXn"),
    ("JAGTERS VAN ZARSJATA", "https://www.kobo.com/ww/en/ebook/jagters-van-zarsjata?sId=23e6c89c-07d6-43f9-a8a8-8764604a87b7&ssId=F7h4XLTeCnIuzM0J_oAmf"),
    ("DIE LUIPERDBENDE", "https://www.kobo.com/ww/en/ebook/die-luiperdbende?sId=7e30391d-27f6-4863-af43-e32400c61fc2&ssId=73bvPvfn4TEIaunFX0MSp"),
    ("REWOLUSIE IN DIE OERWOUD", "https://www.kobo.com/ww/en/ebook/rewolusie-in-die-oerwoud?sId=097e71c4-316e-418c-8bf1-29e833e297c3&ssId=033I7NS2u1xpHpmT0XSJr"),
    ("LAND VAN DIE VAMPIERE", "https://www.kobo.com/ww/en/ebook/land-van-die-vampiere?sId=231f8adf-e17a-424a-a7e1-50f5a531c075&ssId=6iI9N9P8foGRRc1lIr-aI"),
    # Sahara Reeks
    ("BLOEDSPORE IN DIE SAHARA", "https://www.kobo.com/ww/en/ebook/bloedspore-in-die-sahara?sId=523ce785-bca6-4895-bb66-500d03e82402&ssId=3lYQ_FjY1lBZA6v-uQrC3"),
    ("BLOEDHOND IN DIE SAHARA", "https://www.kobo.com/ww/en/ebook/bloedhond-in-die-sahara?sId=efd32198-4bc5-450c-88b2-3c1815aa0b7a&ssId=t3XDAU5GlQekkT-AWJYVC"),
    ("SKADUWEE OOR DIE SAHARA", "https://www.kobo.com/ww/en/ebook/skaduwee-oor-die-sahara?sId=3c3aad1a-e6df-45b8-b1b5-53a854d23c19&ssId=3dCllnoJRATP8sOVNsSsO"),
    ("WRAAK TREK OOR DIE SAHARA", "https://www.kobo.com/ww/en/ebook/wraak-trek-oor-die-sahara?sId=447f4366-cc64-4838-9a2c-0ef61b1e55ff&ssId=PDLaPY6P-ptuaKSjkwsov"),
    ("MAKKERS VAN DIE DOOD", "https://www.kobo.com/ww/en/ebook/makkers-van-die-dood?sId=0142e299-3579-4c88-9527-a1c2b1a62068&ssId=0UeKlwtDAZyvMKyK3X5TX"),
    ("BLOEDIGE ROBYN", "https://www.kobo.com/ww/en/ebook/bloedige-robyn?sId=0487df12-ae26-407a-a081-4406c477eef2&ssId=e7IReGNyZNcz5yfBdQWjV"),
    ("GEBIED ZERO", "https://www.kobo.com/ww/en/ebook/gebied-zero?sId=fc07622d-edbc-4534-8595-319774a0e6f5&ssId=tVgj0EYa_qsZw_Jdf0Ftp"),
    ("DIE MUITERS", "https://www.kobo.com/ww/en/ebook/die-muiters?sId=ffb43752-8b5f-424e-9f27-e1750b7aee38&ssId=7hi5pJQuNWZCWOLyGwbyA"),
    ("SO DONKER DIE WRAAK", "https://www.kobo.com/ww/en/ebook/so-donker-die-wraak?sId=41a3b629-d9b6-4e72-958c-45c14bdde55d&ssId=7NLLW0jrk_Uc46E14Ql4w"),
    ("SO SOET DIE WRAAK", "https://www.kobo.com/ww/en/ebook/so-soet-die-wraak?sId=a50156bb-5e14-4ea2-93fa-8f1f18a19a59&ssId=hOHbo9Z_VUoa2mqycuVAw"),
    ("TEMPEL VAN GEWELD", "https://www.kobo.com/ww/en/ebook/tempel-van-geweld?sId=9806a0eb-7ce9-45d8-8a98-4c1b0fb6203e&ssId=bTOZ1KYWFnFzpiWqTZSRy"),
    ("STRAF EKSPEDISIE", "https://www.kobo.com/ww/en/ebook/straf-ekspedisie?sId=2b6d1267-e9c2-4475-87e1-c1d2c4702a10&ssId=Bz_gmJSEXR4_Y-VUhqke5"),
    ("GIL IN DIE NAG", "https://www.kobo.com/ww/en/ebook/gil-in-die-nag?sId=c314fb04-4336-407c-8dd3-7aa0fbef7a66&ssId=RVC02QzbHnkeNqYTiCKOU"),
    # Maagd van die See nr 1 - update "MAAGD VAN DIE SEE" (single book, not omnibus)
    ("MAAGD VAN DIE SEE", "https://www.amazon.com/dp/B09LJ4W49R"),
    # Red Ruby Series Box Set - exact title is "RED RUBY BOX SET - 3 EBOOKS"
    ("RED RUBY BOX SET - 3 EBOOKS", "https://www.amazon.com/dp/B0FFK5WPJJ"),
    # The Pirates Treasure Book 2 - exact title is "THE PIRATE'S TREASURE"
    # NOTE: This title appears TWICE (Oloff die Seerower AND Red Ruby). User says "Book 2"
    # We'll update both as same link
    ("THE PIRATE'S TREASURE", "https://www.amazon.com/dp/B0DW6HZFHV"),
    # Emerald of the high seas
    ("EMERALD OF THE HIGH SEAS", "https://www.amazon.com/dp/B0DW6BX4SH/"),
    # Vonnis van die berge (exact title)
    ("VONNIS VAN DIE BERGE", "https://www.kobo.com/ww/en/ebook/vonnis-van-die-berge?sId=c50a0f89-e999-411b-8dbd-f55af133af8b&ssId=3AqHZnLx_77zrzHBA3dX"),
]

print("\nUpdating links:")
for title, url in link_updates:
    content = update_book_link(content, title, url)

# ============================================================
# TASK 5c: Add red circle to Oerwoudvalk Omnibus (if not present)
# The title "1. OERWOUDVALK OMNIBUS - 3 EBOEKE" has no red circle currently
# ============================================================
old_oerwoud_img = '<img alt="1. OERWOUDVALK OMNIBUS - 3 EBOEKE" loading="lazy" src="/images/covers/cover_111.jpg"/>\r\n<span class="store-badge badge-afrikaans">Afrikaans</span>'
new_oerwoud_img = '<img alt="1. OERWOUDVALK OMNIBUS - 3 EBOEKE" loading="lazy" src="/images/covers/cover_111.jpg"/><span class="book-number" style="background-color: #ff0000; color: #ffffff;">1</span>\r\n<span class="store-badge badge-afrikaans">Afrikaans</span>'

# Alternative: span on same line
old_oerwoud_img2 = '<img alt="1. OERWOUDVALK OMNIBUS - 3 EBOEKE" loading="lazy" src="/images/covers/cover_111.jpg"/>'
if old_oerwoud_img in content:
    content = content.replace(old_oerwoud_img, new_oerwoud_img, 1)
    print("\nTASK5c ✓ Added red circle to OERWOUDVALK OMNIBUS")
elif old_oerwoud_img2 in content:
    content = content.replace(old_oerwoud_img2, old_oerwoud_img2 + '<span class="book-number" style="background-color: #ff0000; color: #ffffff;">1</span>', 1)
    print("\nTASK5c ✓ Added red circle to OERWOUDVALK OMNIBUS (alt method)")
else:
    print("\nTASK5c ✗ Could not find OERWOUDVALK OMNIBUS img")

# Also check and add red circle to Jungle Hawk Box Set if doesn't have one 
# (The Oerwoudvalk in Afrikaans series is handled; Jungle Hawk English already has no circle per HTML)

# ============================================================
# Write the modified content
# ============================================================
with open(input_file, "w", encoding="utf-8") as f:
    f.write(content)

new_len = len(content)
print(f"\nDone! File size: {original_len} -> {new_len} bytes (diff: {new_len - original_len})")
