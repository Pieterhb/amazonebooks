input_file = r'c:\googleamazon\website\index.html'
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Update counts
content = content.replace('Enkel Stories <span class="count">(11)</span>', 'Enkel Stories <span class="count">(8)</span>')
content = content.replace('Explore the complete collection of 11 books in this series.', 'Explore the complete collection of 8 books in this series.')

content = content.replace('Pieter Haasbroek Stories <span class="count">(7)</span>', 'Pieter Haasbroek Stories <span class="count">(5)</span>')
content = content.replace('Explore the complete collection of 7 books in this series.', 'Explore the complete collection of 5 books in this series.')

with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)
