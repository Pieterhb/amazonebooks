import re

with open(r'c:\googleamazon\website\index.html', 'r', encoding='utf-8', newline='') as f:
    content = f.read()

for m in re.finditer(r'<article class.*?</article>', content, re.DOTALL):
    art = m.group()
    if 'THE PIRATE' in art and 'TREASURE' in art:
        h3m = re.search(r'<h3>([^<]+)</h3>', art)
        hrefm = re.search(r'href="([^"]+)"', art)
        num = re.search(r'book-number[^>]*>([^<]+)</span>', art)
        section_pos = m.start()
        print('Title:', h3m.group(1) if h3m else '?')
        print('Link:', hrefm.group(1) if hrefm else '?')
        print('Number:', num.group(1) if num else '?')
        # Find what section this is in
        section_search = content[:section_pos].rfind('<h2>')
        if section_search != -1:
            h2end = content.find('</h2>', section_search)
            print('In section:', content[section_search+4:h2end])
        print()
