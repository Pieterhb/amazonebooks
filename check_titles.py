import re

with open(r'c:\googleamazon\website\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find each book card with its title and link
book_pattern = r'<article class="book-card">(.*?)</article>'
books = re.findall(book_pattern, content, re.DOTALL)

targets = ['MAAGD VAN DIE SEE', 'RED RUBY', 'OERWOUDVALK OMNIBUS', 'EMERALD OF THE HIGH SEAS', "PIRATE'S TREASURE", 'VONNIS VAN DIE BERGE', 'VONNIS VAN DIE BERGE']
for book in books:
    title_match = re.search(r'<h3>([^<]+)</h3>', book)
    href_match = re.search(r'href="([^"]+)"', book)
    if title_match:
        title = title_match.group(1)
        href = href_match.group(1) if href_match else 'NO_LINK'
        if any(t in title for t in targets):
            print(f'TITLE: {title}')
            print(f'HREF: {href}')
            print()
