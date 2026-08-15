import re
import unicodedata
from bs4 import BeautifulSoup

def normalize(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
    return s.lower().strip()

manual_updates = [
    ("gemaskerde moordenaars", "https://www.kobo.com/ww/en/ebook/gemaskerde-moordenaars-1?sId=ed71ca7c-7068-4b34-b58a-6cd35bfb0a21&ssId=VWSvhZde1cD8ATR1j9fx6"),
    ("die mensvreters van tsawo", "https://www.kobo.com/ww/en/ebook/die-mensvreters-van-tsawo-1?sId=a35e43e0-f14c-45c4-8508-dd5f4af5ef1d&ssId=zTuEwJDRV7sA98_QOrwOq"),
    ("die bloedboodskap", "https://www.kobo.com/ww/en/ebook/die-bloedboodskap?sId=f0d91e74-d05c-46b4-8a42-aa2189974524&ssId=xYgOvDE94IH3k-68yTJOw"),
    ("kamerade van die draak", "https://www.kobo.com/ww/en/ebook/kamerade-van-die-draak?sId=9215ebe2-875b-44ec-8688-8741ec9c6cc8&ssId=NUwWR5rDtHnW0M221vvvO"),
    ("die kruipende dood", "https://www.kobo.com/ww/en/ebook/die-kruipende-dood?sId=09083a63-4905-4cdd-8806-324fbe4160e9&ssId=WfdnawffyPvSdUMvBc4Kg"),
    ("die galg in die oerwoud", "https://www.kobo.com/ww/en/ebook/die-galg-in-die-oerwoud?sId=83d335fa-d167-4d93-a7bb-6bb4625bcbe9&ssId=25C2t3HE871H3jCSAwVcV")
]

with open('c:/googleamazon/website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

matched = set()

# Process only 'die-swart-luiperd-reeks' to be safe, though global replace is fine since these are specific names
section = soup.find('section', id='die-swart-luiperd-reeks')
if section:
    cards = section.find_all('article', class_='book-card')
    for card in cards:
        h3 = card.find('h3')
        if not h3:
            continue
            
        app_title = normalize(h3.text)
        
        best_match = None
        for update in manual_updates:
            clean_search = normalize(update[0])
            
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
                    new_span.string = "1"
                    
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
