import re

input_file = r"c:\googleamazon\website\index.html"

with open(input_file, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# Add red circle to RED RUBY BOX SET
title = "RED RUBY BOX SET - 3 EBOOKS"
idx = content.find(title)
if idx != -1:
    art_start = content.rfind('<article', 0, idx)
    art_end = content.find('</article>', idx)
    article = content[art_start:art_end]
    
    # Check if there is an image without a span right after
    img_pattern = r'(<img alt="RED RUBY BOX SET - 3 EBOOKS"[^>]*/>)'
    replacement = r'\1<span class="book-number" style="background-color: #ff0000; color: #ffffff;">1</span>'
    new_article = re.sub(img_pattern, replacement, article)
    
    if new_article != article:
        content = content[:art_start] + new_article + content[art_end:]
        print("Updated RED RUBY BOX SET - 3 EBOOKS with red circle.")

with open(input_file, 'w', encoding='utf-8', newline='') as f:
    f.write(content)
