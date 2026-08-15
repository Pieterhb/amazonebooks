from bs4 import BeautifulSoup
import re

with open('c:/googleamazon/website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

section = soup.find('section', id='die-swart-luiperd-reeks')
if section:
    cards = section.find_all('article', class_='book-card')
    print(f"Found {len(cards)} cards in Die Swart Luiperd Reeks section.")
    
    # Remove cards from index 6 onwards (i.e. keep 0 to 5, which are 1 to 6)
    removed_count = 0
    for card in cards[6:]:
        card.decompose()
        removed_count += 1
        
    print(f"Removed {removed_count} cards.")
    
    # Update sidebar count
    # <a data-target="die-swart-luiperd-reeks" href="#">Die Swart Luiperd Reeks <span class="count">(71)</span></a>
    sidebar_a = soup.find('a', attrs={'data-target': 'die-swart-luiperd-reeks'})
    if sidebar_a:
        count_span = sidebar_a.find('span', class_='count')
        if count_span:
            old_val = count_span.string
            count_span.string = f"({len(cards) - removed_count})"
            print(f"Updated sidebar count from {old_val} to {count_span.string}")

    # Update hero section description if needed
    # <p>Explore the complete collection of 71 books in this series.</p>
    p_tags = section.find_all('p')
    for p in p_tags:
        if 'Explore the complete collection of ' in p.text:
            p.string = p.text.replace(str(len(cards)), str(len(cards) - removed_count))
            print(f"Updated section description to: {p.string}")

    # Update total books count in stats-banner
    # <div class="stat-card">
    #   <span class="stat-number">513</span>
    #   <span class="stat-label">Total Books</span>
    # </div>
    # It might be 513 or some other number. 
    # Let's count all article book-card in the body to get exact total? Wait, some are in home view.
    # It's better to calculate the exact difference.
    stat_cards = soup.find_all('div', class_='stat-card')
    for stat in stat_cards:
        label = stat.find('span', class_='stat-label')
        if label and 'Total Books' in label.text:
            num_span = stat.find('span', class_='stat-number')
            if num_span and num_span.string.isdigit():
                old_total = int(num_span.string)
                new_total = old_total - removed_count
                num_span.string = str(new_total)
                print(f"Updated total books from {old_total} to {new_total}")

with open('c:/googleamazon/website/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
