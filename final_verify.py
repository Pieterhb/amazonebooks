import re

with open(r'c:\googleamazon\website\index.html', 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# Check Sahara link
m = re.search(r'<h3>SAHARA AVONTUUR OMNIBUS - 3 EBOEKE</h3>.*?href="([^"]+)"', content, re.DOTALL)
if m:
    print('Sahara Omnibus link:', m.group(1))

# Count updates  
print()
has12 = '(12)</span>' in content and 'SA Polisie' in content
print('SA Polisie count 12:', has12)
has9 = '(9)</span>' in content
print('Swerwer Speurder has 9:', has9)

# Pirate Treasure links
print()
for m2 in re.finditer(r'<h3>THE PIRATE\'S TREASURE</h3>.*?href="([^"]+)"', content, re.DOTALL):
    print('Pirate Treasure link:', m2.group(1))
