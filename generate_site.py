import os
import shutil
import pandas as pd
import re

EXCEL_PATH = r"c:\googleebook\temp\INFO.xlsx"
IMG_SOURCE_DIR = r"c:\googleebook\temp\Images book covers only"
PUBLIC_IMG_DIR = r"c:\googleebook\website\public\images\covers"

# Create public image dir if it doesn't exist
os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)

df = pd.read_excel(EXCEL_PATH)

# Clean up series names
df['Series'] = df['Series or Single Ebook Names'].astype(str).str.strip().str.replace('   ', ' ')
df['Language'] = df['Language'].astype(str).str.strip()

categories = [
    {"name": "Sahara Avontuur Reeks", "series": "Sahara Avontuur Reeks", "lang": "Afrikaans"},
    {"name": "Sahara Adventure Series", "series": "Sahara Adventure Series", "lang": "English"},
    {"name": "Serie Aventure Sahara (French)", "series": "Serie Aventure Sahara", "lang": "French"},
    {"name": "Serie Avventure Sahara (Italian)", "series": "Serie Avventure Sahara", "lang": "Italian"},
    {"name": "Sahara Abenteuer Reine (German)", "series": "Sahara Abenteuer Reine", "lang": "German"},
    {"name": "Serie Aventure Sahara (Spanish)", "series": "Serie Aventure Sahara", "lang": "Spanish"},
    {"name": "Die Buiter Reeks", "series": "Die Buiter Reeks", "lang": "Afrikaans"},
    {"name": "The Masked Robber Series", "series": "The Masked Robber Series", "lang": "English"},
    {"name": "Die Swart Luiperd Reeks", "series": "Die Swart Luiperd Reeks", "lang": "Afrikaans"},
    {"name": "The Black Leopard Series", "series": "The Black Leopard Series", "lang": "English"},
    {"name": "Oloff die Seerower Reeks", "series": "Oloff die Seerower Reeks", "lang": "Afrikaans"},
    {"name": "Oloff the Pirate Series", "series": "Oloff the Pirate Series", "lang": "English"},
    {"name": "Woeste Laeveld Reeks", "series": "Woeste Laeveld Reeks", "lang": "Afrikaans"},
    {"name": "Wild Lowveld Series", "series": "Wild Lowveld Series", "lang": "English"},
    {"name": "Oerwoudvalk Reeks", "series": "Oerwoudvalk Reeks", "lang": "Afrikaans"},
    {"name": "Jungle Hawk Series", "series": "Jungle Hawk Series", "lang": "English"},
    {"name": "SA Polisie Reeks", "series": "SA Polisie Reeks", "lang": "Afrikaans"},
    {"name": "SA Police Series", "series": "SA Police Series", "lang": "English"},
    {"name": "Sahara Reeks", "series": "Sahara Reeks", "lang": "Afrikaans"},
    {"name": "Sahara Series", "series": "Sahara Series", "lang": "English"},
    {"name": "Maagd van die See Reeks", "series": "Maagd van die See Reeks", "lang": "Afrikaans"},
    {"name": "Red Ruby Series", "series": "Red Ruby Series", "lang": "English"},
    {"name": "Tamar Reeks", "series": "Tamar Reeks", "lang": "Afrikaans"},
    {"name": "Tamar Series", "series": "Tamar Series", "lang": "English"},
    {"name": "Swerwer Speurder Reeks", "series": "Swerwer Speurder Reeks", "lang": "Afrikaans"},
    {"name": "Wanderer Detective Series", "series": "Wanderer Detective Series", "lang": "English"},
    {"name": "Ryk Schoonraad Reeks", "series": "Ryk Schoonraad Reeks", "lang": "Afrikaans"},
    {"name": "Ryk Schoonraad Series", "series": "Ryk Schoonraad Series", "lang": "English"},
    {"name": "Jaap Zeeman Reeks", "series": "Jaap Zeeman Reeks", "lang": "Afrikaans"},
    {"name": "Ruimte Reeks", "series": "Ruimte Reeks", "lang": "Afrikaans"},
    {"name": "Henk Human Reeks", "series": "Henk Human Reeks", "lang": "Afrikaans"},
    {"name": "Simon Rand Reeks", "series": "Simon Rand Reeks", "lang": "Afrikaans"},
    {"name": "Spioenasie Reeks", "series": "Spioenasie Reeks", "lang": "Afrikaans"},
    {"name": "Temmers van die Woestyn Reeks", "series": "Temmers van die Woestyn Reeks", "lang": "Afrikaans"},
    {"name": "AI Stories", "series": "AI Stories", "lang": "English"},
    {"name": "Enkel Stories", "series": "Enkel Stories", "lang": "Afrikaans"},
    {"name": "Single Stories", "series": "Single Stories", "lang": "English"},
    {"name": "Pieter Haasbroek Stories", "series": "Pieter Haasbroek", "lang": "Any"}, # Custom matching
    {"name": "Social Media", "series": "Social Media", "lang": "English"},
    {"name": "Other", "series": "Other", "lang": "Any"}
]

# Create a dictionary to hold books for each category
categorized_books = {cat['name']: [] for cat in categories}

missing_images = []

for index, row in df.iterrows():
    title = str(row['Title']).strip()
    link = str(row['Book_Link']).strip()
    author = str(row['Author']).strip()
    img_num = str(row['Image Number']).strip()
    series = str(row['Series']).strip()
    lang = str(row['Language']).strip()
    
    if pd.isna(row['Title']) or title == 'nan':
        continue
        
    # Find matching category
    matched_cat = "Other"
    
    if "Pieter Haasbroek" in series:
        matched_cat = "Pieter Haasbroek Stories"
    else:
        for cat in categories:
            if cat['series'] == series:
                # If language is ANY or it matches
                if cat['lang'] == 'Any' or cat['lang'].lower() in lang.lower():
                    matched_cat = cat['name']
                    break
    
    # Check if image exists and copy it
    img_name = img_num
    if not img_name.endswith('.jpg'):
        img_name += '.jpg'
        
    src_img_path = os.path.join(IMG_SOURCE_DIR, img_name)
    dst_img_path = os.path.join(PUBLIC_IMG_DIR, img_name)
    
    if os.path.exists(src_img_path):
        if not os.path.exists(dst_img_path):
            shutil.copy2(src_img_path, dst_img_path)
    else:
        missing_images.append(img_name)
        
    book_obj = {
        "title": title,
        "link": link,
        "author": author,
        "img": f"/images/covers/{img_name}",
        "series": series,
        "lang": lang
    }
    categorized_books[matched_cat].append(book_obj)

print(f"Missing images: {len(missing_images)}")
for cat, books in categorized_books.items():
    print(f"{cat}: {len(books)} books")

# Generate HTML
html_sections = []
sidebar_links = []

for i, cat in enumerate(categories):
    name = cat['name']
    books = categorized_books[name]
    if len(books) == 0:
        continue
        
    section_id = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    
    sidebar_links.append(f'<li><a href="#" data-target="{section_id}">{name} <span class="count">({len(books)})</span></a></li>')
    
    cards_html = []
    for b in books:
        badge_class = "badge-panther"
        if "afrikaans" in b['lang'].lower(): badge_class = "badge-afrikaans"
        elif "english" in b['lang'].lower(): badge_class = "badge-english"
        
        cards_html.append(f'''
        <article class="book-card">
          <div class="book-img-wrapper">
            <img src="{b['img']}" alt="{b['title']}" loading="lazy">
            <span class="store-badge {badge_class}">{b['lang']}</span>
          </div>
          <div class="book-content">
            <h3>{b['title']}</h3>
            <p class="author">By {b['author']}</p>
            <a href="{b['link']}" target="_blank" rel="noopener" class="btn btn-primary">View Book</a>
          </div>
        </article>
        ''')
        
    html_sections.append(f'''
    <section id="{section_id}" class="view">
      <div class="section-hero">
        <h2>{name}</h2>
        <p>Explore the complete collection of {len(books)} books in this series.</p>
      </div>
      <div class="product-grid">
        {"".join(cards_html)}
      </div>
    </section>
    ''')

index_html = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Discover hundreds of unique Afrikaans & English eBooks from Pieter Haasbroek." />
    <title>Pulp Fiction eBooks | Complete Collection</title>
    <link rel="stylesheet" href="/style.css" />
  </head>
  <body>
    <!-- Mobile Header -->
    <header class="mobile-header">
      <a href="#" class="logo" data-target="home">
        Pulp Fiction <span>eBooks</span>
      </a>
      <button class="mobile-menu-btn" id="mobile-menu-btn" aria-label="Toggle menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </button>
    </header>

    <div class="app-layout">
      <!-- Sidebar Navigation -->
      <aside class="sidebar" id="sidebar">
        <div class="sidebar-header desktop-only">
          <a href="#" class="logo" data-target="home">
            Pulp Fiction<br><span>eBooks</span>
          </a>
        </div>
        <nav class="sidebar-nav">
          <ul class="nav-list">
            <li><a href="#" data-target="home" class="active">🏠 Home</a></li>
            <li class="nav-header">Library Collection</li>
            {"".join(sidebar_links)}
          </ul>
        </nav>
      </aside>

      <!-- Main Content Area -->
      <main class="main-content">
        <!-- Home View -->
        <section id="home" class="view active">
          <div class="hero">
            <div class="hero-badge">🐆 Your One-Stop eBook Store</div>
            <h1>The Complete Collection</h1>
            <p>Welcome to the ultimate library of Pieter Haasbroek's classic pulp fiction eBooks. Use the sidebar to browse through 39 unique series across 6 languages.</p>
          </div>
          <div class="stats-banner">
            <div class="stat-card">
              <span class="stat-number">{sum(len(b) for b in categorized_books.values())}</span>
              <span class="stat-label">Total Books</span>
            </div>
            <div class="stat-card">
              <span class="stat-number">{len([c for c in categorized_books.values() if len(c)>0])}</span>
              <span class="stat-label">Categories</span>
            </div>
          </div>
        </section>

        <!-- Dynamic Sections -->
        {"".join(html_sections)}
      </main>
    </div>

    <script type="module" src="/main.js"></script>
  </body>
</html>
'''

with open(r'c:\googleebook\website\index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Generated index.html successfully.")
