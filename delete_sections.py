from bs4 import BeautifulSoup

targets_to_delete = [
    "jaap-zeeman-reeks",
    "ruimte-reeks",
    "henk-human-reeks",
    "simon-rand-reeks",
    "spioenasie-reeks",
    "temmers-van-die-woestyn-reeks",
    "social-media"
]

with open('c:/googleamazon/website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

removed_books_count = 0
removed_sections_count = 0

for target in targets_to_delete:
    # 1. Remove the section
    section = soup.find('section', id=target)
    if section:
        cards = section.find_all('article', class_='book-card')
        removed_books_count += len(cards)
        section.decompose()
        removed_sections_count += 1
        print(f"Removed section {target} containing {len(cards)} books.")
        
    # 2. Remove the sidebar link
    sidebar_a = soup.find('a', attrs={'data-target': target})
    if sidebar_a:
        li = sidebar_a.find_parent('li')
        if li:
            li.decompose()
            print(f"Removed sidebar link for {target}.")

# 3. Update Total Books and Categories in stats banner
stat_cards = soup.find_all('div', class_='stat-card')
for stat in stat_cards:
    label = stat.find('span', class_='stat-label')
    if label:
        if 'Total Books' in label.text:
            num_span = stat.find('span', class_='stat-number')
            if num_span and num_span.string.isdigit():
                old_total = int(num_span.string)
                new_total = old_total - removed_books_count
                num_span.string = str(new_total)
                print(f"Updated total books from {old_total} to {new_total}")
        elif 'Categories' in label.text:
            num_span = stat.find('span', class_='stat-number')
            if num_span and num_span.string.isdigit():
                old_total = int(num_span.string)
                new_total = old_total - removed_sections_count
                num_span.string = str(new_total)
                print(f"Updated categories from {old_total} to {new_total}")

with open('c:/googleamazon/website/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
