import re

with open(r'c:\googleamazon\website\index_backup_before_changes.html', 'r', encoding='utf-8', newline='') as f:
    content = f.read()

for m in re.finditer(r'<article class.*?</article>', content, re.DOTALL):
    art = m.group()
    if 'THE PIRATE' in art and 'TREASURE' in art:
        h3m = re.search(r'<h3>([^<]+)</h3>', art)
        hrefm = re.search(r'href="([^"]+)"', art)
        print('Title:', h3m.group(1) if h3m else '?')
        print('Link:', hrefm.group(1) if hrefm else '?')
        print()
