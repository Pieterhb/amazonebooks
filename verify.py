import re

with open(r'c:\googleamazon\website\index.html', 'r', encoding='utf-8', newline='') as f:
    content = f.read()

print('=== VERIFICATION ===')

# 1. Sahara Omnibus
marker = 'SAHARA AVONTUUR OMNIBUS - 3 EBOEKE'
idx = content.find(marker)
if idx != -1:
    ctx = content[max(0,idx-100):idx+200]
    has_red_circle = 'background-color: #ff0000' in ctx[:100]
    has_new_link = 'B0FF56LSBW' in ctx
    print(f'1. Sahara Omnibus red circle removed: {not has_red_circle} (True=good)')
    print(f'   Sahara Omnibus new link: {has_new_link} (True=good)')

# 2. Masked Robber Box Set
marker2 = 'THE MASKED ROBBER BOX SET - 3 EBOOKS'
idx2 = content.find(marker2)
if idx2 != -1:
    ctx2 = content[max(0,idx2-100):idx2+100]
    has_red2 = 'background-color: #ff0000' in ctx2[:100]
    print(f'2. Masked Robber red circle removed: {not has_red2} (True=good)')

# 3. Oloff Omnibus
marker3 = 'OLOFF DIE SEEROWER OMNIBUS - 3 EBOEKE'
idx3 = content.find(marker3)
if idx3 != -1:
    ctx3 = content[max(0,idx3-100):idx3+100]
    has_red3 = 'background-color: #ff0000' in ctx3[:100]
    print(f'3. Oloff Omnibus red circle removed: {not has_red3} (True=good)')

# 4. SA Polisie
print(f'4. SA Polisie book 13 deleted: {("MONSTER UIT DIE MIS" not in content)} (True=good)')
print(f'   SA Polisie book 12 preserved: {"DIE BARON VAN DIE NAMIB" in content} (True=good)')

# 5. Swerwer Speurder
print(f'5. Swerwer Speurder book10 deleted: {("DRUPPEL WYN" not in content)} (True=good)')
print(f'   Swerwer Speurder book9 preserved: {"KIEM VAN DIE DOOD" in content} (True=good)')

# Link updates
print()
print('Link updates:')
checks = [
    ('DIE VERRAAIER VAN DINI-SALAM', 'B0F48T9FVN'),
    ('BLOEDIGE ROBYN', 'bloedige-robyn'),
    ('MAAGD VAN DIE SEE', 'B09LJ4W49R'),
    ('RED RUBY BOX SET - 3 EBOOKS', 'B0FFK5WPJJ'),
    ('EMERALD OF THE HIGH SEAS', 'B0DW6BX4SH'),
    ('VONNIS VAN DIE BERGE', 'vonnis-van-die-berge'),
    ('1. OERWOUDVALK OMNIBUS - 3 EBOEKE', 'oerwoudvalk-omnibus'),
]
for title, url_part in checks:
    h3 = f'<h3>{title}</h3>'
    idx = content.find(h3)
    if idx != -1:
        ctx = content[idx:idx+300]
        found = url_part in ctx
        print(f'  {title}: link updated={found}')
    else:
        print(f'  {title}: NOT FOUND IN HTML')

# Oerwoudvalk red circle
idx_oe = content.find('1. OERWOUDVALK OMNIBUS - 3 EBOEKE')
if idx_oe != -1:
    ctx_oe = content[max(0,idx_oe-100):idx_oe+200]
    has_red_oe = '#ff0000' in ctx_oe
    print(f'  Oerwoudvalk Omnibus has red circle: {has_red_oe} (True=good)')
