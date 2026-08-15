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

missing_red_circle = []
missing_from_html = []

for title in titles_to_check:
    # Find all articles with this title
    # We use a non-greedy match to grab the article tags
    pattern = r'(<article class="book-card">.*?<h3>' + re.escape(title) + r'</h3>.*?</article>)'
    matches = re.finditer(pattern, content, flags=re.DOTALL)
    
    found = False
    for m in matches:
        found = True
        art = m.group(1)
        if '#ff0000' not in art:
            missing_red_circle.append(title)
            # Only record the first missing per title for simplicity, or we can check the section
            
    if not found:
        missing_from_html.append(title)

print("Titles missing from HTML:", missing_from_html)
print("Titles missing red circle:", set(missing_red_circle))
