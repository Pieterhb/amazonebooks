import pandas as pd
import re
from bs4 import BeautifulSoup

# 1. Load Excel
df = pd.read_excel('c:/googleamazon/Book2.xlsx', header=None)
excel_books = []
for index, row in df.iterrows():
    title = str(row[0]).strip()
    url = str(row[1]).strip()
    clean_title = re.split(r'[:(]', title)[0].strip().lower()
    excel_books.append({'raw': title, 'clean': clean_title, 'url': url})

# 2. Load HTML
with open('c:/googleamazon/website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
sections = soup.find_all('section')

matched = []
unmatched = []

# Keep track of matched raw titles to find which ones were NOT matched
matched_raw = set()

# Process section by section for the missing number counter
for section in sections:
    missing_number_counter = 1
    cards = section.find_all('article', class_='book-card')
    
    for card in cards:
        h3 = card.find('h3')
        if not h3:
            continue
            
        app_title = h3.text.strip().lower()
        
        # Find matching excel book
        best_match = None
        for eb in excel_books:
            if eb['clean'] == app_title or eb['clean'] in app_title or app_title in eb['clean']:
                best_match = eb
                break
                
        if best_match:
            matched_raw.add(best_match['raw'])
            
            # 1. Update the link
            a_tag = card.find('a', href=re.compile(r'sqrindle\.com'))
            if a_tag:
                a_tag['href'] = best_match['url']
                
            # 2. Update the icon
            img_wrapper = card.find('div', class_='book-img-wrapper')
            if img_wrapper:
                book_number_span = img_wrapper.find('span', class_='book-number')
                if book_number_span:
                    book_number_span['style'] = 'background-color: #ff0000; color: #ffffff;'
                else:
                    # Create the span if missing
                    new_span = soup.new_tag('span')
                    new_span['class'] = 'book-number'
                    new_span['style'] = 'background-color: #ff0000; color: #ffffff;'
                    new_span.string = str(missing_number_counter)
                    missing_number_counter += 1
                    
                    # Insert after the img tag or at beginning
                    img_tag = img_wrapper.find('img')
                    if img_tag:
                        img_tag.insert_after(new_span)
                    else:
                        img_wrapper.insert(0, new_span)

# Write back the modified HTML
# using formatter='html5' to prevent self-closing tags expansion if possible
with open('c:/googleamazon/website/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

# Check which ones were unmatched
for eb in excel_books:
    if eb['raw'] not in matched_raw:
        unmatched.append(eb['raw'])

print(f'Matched: {len(matched_raw)}')
print(f'Unmatched: {len(unmatched)}')
print('--- UNMATCHED ---')
for u in unmatched:
    print(u)
