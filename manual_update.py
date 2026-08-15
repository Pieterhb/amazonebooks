import re
import unicodedata
from bs4 import BeautifulSoup

def normalize(s):
    # Remove accents, punctuation, etc.
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
    return s.lower().strip()

manual_updates = [
    ("Dreunende Hoewe", "https://www.amazon.com/dp/B07MFZN38F/"),
    ("Storm oor Dini Salam", "https://www.amazon.com/dp/B0F48TXBP2/"),
    ("Vuurpeleton", "https://www.amazon.com/dp/B0FDGHW5FT/"),
    ("Sahara Avontuur Omnibus", "https://www.amazon.com/dp/B0FF57BLSC/"), # For Sahara-Adventure-Box-Set-3Ebooks which might be omnibus
    ("Terror under the Stars", "https://www.amazon.com/Terror under the Stars/dp/B0F62W9B61/"),
    ("Footprints of Betrayal", "https://www.amazon.com/Footprints-of Betrayal/dp/B0F6397K52/"),
    ("Aber-el-Mirs Secret", "https://www.amazon.com/Aber-el-Mirs Secret/dp/B0F63FDFCL/"),
    ("Signal in the Dark", "https://www.amazon.com/Signal in the Dark/dp/B0F63DBMNP/"),
    ("Under a Blazing Sky", "https://www.amazon.com/Under a Blazing Sky/dp/B0F63FKNP2/"),
    ("Die Swaardvegter", "https://www.amazon.com/dp/B0F7JQFQR6/"),
    ("Die Seewraak", "https://www.amazon.com/dp/B0F7K2WK2Z/"),
    ("Die Skuim van die see", "https://www.amazon.com/dp/B0F7K7QQ93/"),
    ("Aasvoels van die see", "https://www.amazon.com/dp/B0F7K5LPHC/"),
    ("Die vloot van verwoesting", "https://www.amazon.com/dp/B0F7K482WS/"),
    ("Riders of Death", "https://www.amazon.com/dp/B0DSJGJ5SJ"),
    ("Gold city of sheba", "https://www.amazon.com/dp/B0DSGBFRMQ/"),
    ("Nag van geen genade", "https://www.amazon.com/dp/B0FMPJPYFV/"),
    ("aasvoels van die Kalahari", "https://www.amazon.com/dp/B0FMPKD5KG/"),
    ("area zero", "https://www.amazon.com/dp/B0FBRWMQZK/"),
    ("PEREL VAN MALSIA", "https://www.amazon.com/dp/B0DWM6CL89/"),
    ("die goue draak", "https://www.amazon.com/dp/B0DPVT6BML/"),
    ("How to Fix 46 Common Household Problems", "https://www.amazon.com/dp/B0CW1NFXYP/"),
    ("scary western", "https://www.amazon.com/dp/B0FGDB7RLJ"),
    ("mooiplaas", "https://play.google.com/store/books/details?id=fRZSEAAAQBAJ&pli=1"),
    ("the masked robber", "https://www.amazon.com/dp/B0CFKB2VHW/", True),
    ("die buiter", "https://www.amazon.com/Die-Buiter-Reeks-Book-Afrikaans-ebook/dp/B09LJ4LQBQ/", True),
    ("lank lewe die buiter", "https://www.amazon.com/dp/B09LJ31W3J/"),
    ("die buiter en sy bende", "https://www.amazon.com/Buiter-Bende-Reeks-Book-Afrikaans-ebook/dp/B09LJ42LZM/"),
    ("lokval vir die buiter", "https://www.amazon.com/Lokval-Buiter-Reeks-Book-Afrikaans-ebook/dp/B09LJ3373D/"),
    ("die buiter ry snags", "https://www.amazon.com/Buiter-Snags-Reeks-Book-Afrikaans-ebook/dp/B09LJ2P1GW/"),
    ("die buiter se geheim", "https://www.amazon.com/dp/B09LRBW86T/"),
    ("boodskap vir die buiter", "https://www.amazon.com/dp/B09M9BBRJ5/"),
    ("die buiter hou wag", "https://www.amazon.com/Die-Buiter-Reeks-Book-Afrikaans-ebook/dp/B09N15D3KX/"),
    ("die buiter seevier", "https://www.amazon.com/Buiter-Se%C3%ABvier-Reeks-Book-Afrikaans-ebook/dp/B09NCJ9V2Q/"),
    ("BLOEDSPORE IN DIE SAHARA", "https://www.kobo.com/ww/en/ebook/bloedspore-in-die-sahara?sId=79a8edfe-e6f9-4710-851e-351ec4946aee&ssId=-JP9FqZNBOogbb744h1pk"),
    ("droster in algerie", "https://www.kobo.com/ww/en/ebook/droster-in-algerie?sId=7532a205-c667-4789-9ed5-5e3672256970&ssId=lupfqgco8IXyMSDJqrwGH")
]

with open('c:/googleamazon/website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
sections = soup.find_all('section')

matched = set()

for section in sections:
    # Need to find existing max number to continue counting from it? 
    # Or just start from 1 as per instruction for the new numbers?
    # Wait, the instruction said "You can number the single books in that pages from 1 onward"
    # Actually, if I already numbered them in the previous run, maybe I shouldn't duplicate? 
    # But wait, this is running on the current state.
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
            
            # Update the link (find first a tag)
            a_tag = card.find('a')
            if a_tag:
                a_tag['href'] = best_match[1]
                
            # Update the icon
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
