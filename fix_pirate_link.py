import re

input_file = r"c:\googleamazon\website\index.html"

with open(input_file, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# Fix "THE PIRATE'S TREASURE" links:
# - Oloff the Pirate Series (book 14) should revert to original: B0DXFML6K1
# - Red Ruby Series (book 2) should get the new link: B0DW6HZFHV

# Find the Oloff Pirate section and Red Ruby section separately
# Both have "THE PIRATE'S TREASURE" as the h3

# Strategy: use section anchors to find each occurrence
# Oloff the Pirate Series section
oloff_section_start = content.find('<section class="view" id="oloff-the-pirate-series">')
oloff_section_end = content.find('</section>', oloff_section_start) + len('</section>')

red_ruby_section_start = content.find('<section class="view" id="red-ruby-series">')
red_ruby_section_end = content.find('</section>', red_ruby_section_start) + len('</section>')

print(f"Oloff section: {oloff_section_start} -> {oloff_section_end}")
print(f"Red Ruby section: {red_ruby_section_start} -> {red_ruby_section_end}")

def fix_link_in_range(content, start, end, title, old_href, new_href):
    """Fix link for a book in a specific range"""
    section = content[start:end]
    # Find the article with this title
    pattern = r'(<article class="book-card">.*?<h3>' + re.escape(title) + r'</h3>.*?<a class="btn btn-primary" href=")' + re.escape(old_href) + r'(")'
    replacement = r'\g<1>' + new_href + r'\g<2>'
    new_section, count = re.subn(pattern, replacement, section, count=1, flags=re.DOTALL)
    if count:
        content = content[:start] + new_section + content[end:]
        print(f"  Fixed link in section for: {title}")
    else:
        print(f"  Could NOT fix link for: {title} (old href not found in section)")
    return content, count

# Fix Oloff section: revert back to original B0DXFML6K1
content, n1 = fix_link_in_range(
    content, oloff_section_start, oloff_section_end,
    "THE PIRATE'S TREASURE",
    "https://www.amazon.com/dp/B0DW6HZFHV",  # currently wrong
    "https://www.amazon.com/dp/B0DXFML6K1"   # correct original
)

# Fix Red Ruby section: update to B0DW6HZFHV
content, n2 = fix_link_in_range(
    content, red_ruby_section_start, red_ruby_section_end,
    "THE PIRATE'S TREASURE",
    "https://www.amazon.com/dp/B0DXFML6K1",  # currently old
    "https://www.amazon.com/dp/B0DW6HZFHV"   # user wants this new link
)

with open(input_file, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print(f"Done. Fixed {n1} in Oloff, {n2} in Red Ruby")

# Verify
with open(input_file, 'r', encoding='utf-8', newline='') as f:
    content2 = f.read()
for m in re.finditer(r'<article class.*?</article>', content2, re.DOTALL):
    art = m.group()
    if "THE PIRATE" in art and "TREASURE" in art:
        h3m = re.search(r'<h3>([^<]+)</h3>', art)
        hrefm = re.search(r'href="([^"]+)"', art)
        pos = m.start()
        sec_pos = content2[:pos].rfind('<h2>')
        sec_end = content2.find('</h2>', sec_pos)
        print(f"  {content2[sec_pos+4:sec_end]}: {hrefm.group(1) if hrefm else '?'}")
