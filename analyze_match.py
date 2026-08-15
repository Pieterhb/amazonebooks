import pandas as pd
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    import sys
    print("BeautifulSoup not found")
    sys.exit(1)

df = pd.read_excel('c:/googleamazon/Book2.xlsx', header=None)
excel_books = []
for index, row in df.iterrows():
    title = str(row[0]).strip()
    url = str(row[1]).strip()
    clean_title = re.split(r'[:(]', title)[0].strip().lower()
    excel_books.append({'raw': title, 'clean': clean_title, 'url': url})

with open('c:/googleamazon/website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
cards = soup.find_all('article', class_='book-card')
app_titles = []
for card in cards:
    h3 = card.find('h3')
    if h3:
        app_titles.append(h3.text.strip().lower())

matched = []
unmatched = []

for eb in excel_books:
    found = False
    for at in app_titles:
        if eb['clean'] == at or eb['clean'] in at or at in eb['clean']:
            matched.append(eb['raw'])
            found = True
            break
    if not found:
        unmatched.append(eb['raw'])

print(f'Total excel books: {len(excel_books)}')
print(f'Matched: {len(matched)}')
print(f'Unmatched: {len(unmatched)}')
if unmatched:
    print('Unmatched examples:')
    for u in unmatched[:10]:
        print(" -", u)
