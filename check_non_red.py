import re

with open(r'c:\googleamazon\website\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for spans with class="book-number" but don't strictly require quotes to match
spans = re.findall(r'<span class="book-number"[^>]*>.*?</span>', content)
non_red = []
for span in spans:
    if '#ff0000' not in span.lower():
        non_red.append(span)

# Look for spans with class="book-number" where class is the only attribute
spans_simple = re.findall(r'<span class="book-number">.*?</span>', content)
for span in spans_simple:
    if '#ff0000' not in span.lower():
        non_red.append(span)

# Eliminate duplicates
non_red = list(set(non_red))

if non_red:
    print(f'Found {len(non_red)} non-red book number spans.')
    for s in non_red:
        print(s)
else:
    print('All book-number spans are red!')
