import re
import unicodedata
from bs4 import BeautifulSoup

def normalize(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
    return s.lower().strip()

manual_updates = [
    ("La Sorciere du Sahara", "https://www.amazon.com/dp/B0GPXJ42MT/"),
    ("Storm oor Dini-Salam", "https://www.amazon.com/dp/B0F48TXBP2/")
]

with open('c:/googleamazon/website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
sections = soup.find_all('section')

matched = set()

for section in sections:
    missing_number_counter = 1
    cards = section.find_all('article', class_='book-card')
    
    for card in cards:
        h3 = card.find('h3')
        if not h3:
            continue
            
        app_title = normalize(h3.text)
        
        best_match = None
        for update in manual_updates:
            clean_search = normalize(update[0])
            url = update[1]
            exact_only = len(update) > 2 and update[2]
            
            if exact_only:
                if clean_search == app_title:
                    best_match = update
                    break
            else:
                if clean_search in app_title:
                    best_match = update
                    break
                    
        if best_match:
            matched.add(best_match[0])
            
            a_tag = card.find('a')
            if a_tag:
                a_tag['href'] = best_match[1]
                
            img_wrapper = card.find('div', class_='book-img-wrapper')
            if img_wrapper:
                book_number_span = img_wrapper.find('span', class_='book-number')
                if book_number_span:
                    book_number_span['style'] = 'background-color: #ff0000; color: #ffffff;'
                else:
                    new_span = soup.new_tag('span')
                    new_span['class'] = 'book-number'
                    new_span['style'] = 'background-color: #ff0000; color: #ffffff;'
                    new_span.string = str(missing_number_counter)
                    missing_number_counter += 1
                    
                    img_tag = img_wrapper.find('img')
                    if img_tag:
                        img_tag.insert_after(new_span)
                    else:
                        img_wrapper.insert(0, new_span)

with open('c:/googleamazon/website/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print(f"Matched {len(matched)} of {len(manual_updates)}")
for update in manual_updates:
    if update[0] not in matched:
        print(f"UNMATCHED: {update[0]}")
