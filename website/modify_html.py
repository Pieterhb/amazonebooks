import re

input_file = r'c:\googleamazon\website\index.html'
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original length:", len(content))

# Task 1: Remove the red circle from "MAAGD VAN DIE SEE OMNIBUS - 3 EBOEKE"
# The HTML looks like:
# <img alt="MAAGD VAN DIE SEE OMNIBUS - 3 EBOEKE" loading="lazy" src="/images/covers/cover_199.jpg"/><span class="book-number" style="background-color: #ff0000; color: #ffffff;">1</span>
pattern_maagd = r'(<img alt="MAAGD VAN DIE SEE OMNIBUS - 3 EBOEKE"[^>]*/>)\s*<span class="book-number"[^>]*>.*?</span>'
content = re.sub(pattern_maagd, r'\1', content)

# Task 2: Delete "JOP - LE NIE HEELDAG IN DIE BED NIE.", "NET VIER DAE OM TE LEWE!", "DIE MAN VAN VENUS"
titles_to_delete = [
    "JOP - LE NIE HEELDAG IN DIE BED NIE.",
    "NET VIER DAE OM TE LEWE!",
    "DIE MAN VAN VENUS",
    "GAMES FOR KIDS IN CARS",
    "FACTS ABOUT CATS - 25 IMPORTANT QUESTIONS ANSWERED"
]

for title in titles_to_delete:
    # Find the article that contains this title
    pattern = r'<article class="book-card">(?:(?!</article>).)*?<h3>' + re.escape(title) + r'</h3>.*?</article>'
    # Need re.DOTALL and re.IGNORECASE just in case
    content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
# Task 3: Change "DIE GOUE DRAAK" from 1 to 7, and "DROSTER IN ALGERIË" from 1 to 8
# Find article for DIE GOUE DRAAK
pattern_goue = r'(<article class="book-card">(?:(?!</article>).)*?)<span class="book-number"[^>]*>1</span>((?:(?!</article>).)*?<h3>DIE GOUE DRAAK</h3>.*?</article>)'
content = re.sub(pattern_goue, r'\1<span class="book-number" style="background-color: #ff0000; color: #ffffff;">7</span>\2', content, flags=re.DOTALL)

# Find article for DROSTER IN ALGERIË
pattern_droster = r'(<article class="book-card">(?:(?!</article>).)*?)<span class="book-number"[^>]*>1</span>((?:(?!</article>).)*?<h3>DROSTER IN ALGERIË</h3>.*?</article>)'
content = re.sub(pattern_droster, r'\1<span class="book-number" style="background-color: #ff0000; color: #ffffff;">8</span>\2', content, flags=re.DOTALL)

print("New length:", len(content))

with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML modifications done.")
