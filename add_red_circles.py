import re

input_file = r"c:\googleamazon\website\index.html"

with open(input_file, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

titles_to_check = [
    "DIE VERRAAIER VAN DINI-SALAM",
    "THE TRAITOR OF DINI SALAM",
    "DIE VERRAAIER",
    "VLAM VAN DIE LAEVELD",
    "DIE POORT VAN TRANE",
    "BEMINDE VERRAAIER",
    "SPORE IN DIE DOU",
    "GEEN VERGIFFENIS",
    "HOEFSLAE TEEN MIDDERNAG",
    "RUITERS VAN DIE DOOD",
    "1. OERWOUDVALK OMNIBUS - 3 EBOEKE",
    "GOUDSTAD VAN SKEBA",
    "DIE SEEKAT",
    "OERVALLEI",
    "JAGTERS VAN ZARSJATA",
    "DIE LUIPERDBENDE",
    "REWOLUSIE IN DIE OERWOUD",
    "LAND VAN DIE VAMPIERE",
    "BLOEDSPORE IN DIE SAHARA",
    "BLOEDHOND IN DIE SAHARA",
    "SKADUWEE OOR DIE SAHARA",
    "WRAAK TREK OOR DIE SAHARA",
    "MAKKERS VAN DIE DOOD",
    "BLOEDIGE ROBYN",
    "GEBIED ZERO",
    "DIE MUITERS",
    "SO DONKER DIE WRAAK",
    "SO SOET DIE WRAAK",
    "TEMPEL VAN GEWELD",
    "STRAF EKSPEDISIE",
    "GIL IN DIE NAG",
    "MAAGD VAN DIE SEE",
    "RED RUBY BOX SET - 3 EBOOKS",
    "THE PIRATE'S TREASURE",
    "EMERALD OF THE HIGH SEAS",
    "VONNIS VAN DIE BERGE"
]

def add_red_circle(content, title):
    # Find the article containing this title
    # First, find the exact h3
    h3_str = f'<h3>{title}</h3>'
    idx = content.find(h3_str)
    
    if idx == -1:
        # Fallback to case insensitive or partial
        print(f"Title not found: {title}")
        return content, False
        
    # Find the start of this article
    art_start = content.rfind('<article', 0, idx)
    art_end = content.find('</article>', idx)
    if art_start == -1 or art_end == -1:
        return content, False
        
    article = content[art_start:art_end]
    
    # Check if there is a book number span
    span_match = re.search(r'<span class="book-number"[^>]*>([^<]+)</span>', article)
    if not span_match:
        # Add it if missing
        print(f"No book-number span found for {title}")
        return content, False
        
    span_full = span_match.group(0)
    num = span_match.group(1)
    
    if '#ff0000' in span_full.lower():
        # Already red
        return content, False
        
    new_span = f'<span class="book-number" style="background-color: #ff0000; color: #ffffff;">{num}</span>'
    new_article = article.replace(span_full, new_span)
    
    # Replace in content
    new_content = content[:art_start] + new_article + content[art_end:]
    print(f"Updated red circle for {title}")
    return new_content, True

updated_count = 0
for title in titles_to_check:
    content, updated = add_red_circle(content, title)
    if updated:
        updated_count += 1

print(f"Total titles updated with red circles: {updated_count}")

# Write back
with open(input_file, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

