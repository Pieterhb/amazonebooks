"""
Programmatic SEO (pSEO) Static Site Generator
Generates 1,000+ SEO-optimized landing pages, JSON-LD structured data,
internal linking mesh, chunked XML sitemaps, and robots.txt.
"""

import os
import shutil
import json
import re
from datetime import datetime

from site_config import (
    SITE_URL, SITE_NAME, SITE_TITLE_SUFFIX, SITE_TAGLINE,
    DEFAULT_DESCRIPTION, AMAZON_AFFILIATE_TAG, PUBLISHER_NAME,
    PUBLISHER_LOGO, DEFAULT_OG_IMAGE
)
from pulp_data_engine import PulpDataEngine, slugify, strip_markdown

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

def escape_html(text):
    """Simple HTML escaping."""
    if not text:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")

def render_sidebar(engine, active_target="home"):
    """Render consistent sidebar navigation."""
    home_link = f'<li class="nav-item-home"><a href="/" class="home-nav-link {"active" if active_target == "home" else ""}">🏠 Home</a></li>'
    nav_links = [
        f'<li><a href="/books/" class="{"active" if active_target == "books" else ""}">📚 All Books <span class="count">({len(engine.books)})</span></a></li>',
        f'<li><a href="/series/" class="{"active" if active_target == "series" else ""}">📖 Book Series <span class="count">({len(engine.series)})</span></a></li>',
        f'<li><a href="/authors/" class="{"active" if active_target == "authors" else ""}">✍️ Authors <span class="count">({len(engine.authors)})</span></a></li>',
        f'<li><a href="/genres/" class="{"active" if active_target == "genres" else ""}">🏷️ Genres <span class="count">({len(engine.genres)})</span></a></li>',
        f'<li><a href="/themes/" class="{"active" if active_target == "themes" else ""}">🎯 Niche Themes <span class="count">({len(engine.themes)})</span></a></li>',
        f'<li><a href="/collections/" class="{"active" if active_target == "collections" else ""}">⭐ Curated Lists <span class="count">({len(engine.collections)})</span></a></li>',
    ]

    # Top genres in sidebar
    genre_links = []
    for g_slug, g in list(engine.genres.items())[:8]:
        genre_links.append(f'<li><a href="/genres/{g_slug}/" class="{"active" if active_target == f"genre-{g_slug}" else ""}">{g["name"]} <span class="count">({g["books_count"]})</span></a></li>')

    # All Series in sidebar sorted by books_count
    series_links = []
    for s_slug, s in sorted(engine.series.items(), key=lambda x: -x[1]["books_count"]):
        series_links.append(f'<li><a href="/series/{s_slug}/" class="{"active" if active_target == f"series-{s_slug}" else ""}">{escape_html(s["name"])} <span class="count">({s["books_count"]})</span></a></li>')

    return f"""
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header desktop-only">
        <a href="/" class="logo">
          Pulp Fiction <span>eBooks</span>
        </a>
      </div>
      <nav class="sidebar-nav">
        <ul class="nav-list">
          {home_link}
          <li class="nav-header" style="margin-top:0.6rem;">Explore Library</li>
          {"".join(nav_links)}
          <li class="nav-header">Popular Genres</li>
          {"".join(genre_links)}
          <li class="nav-header" style="color:var(--accent-yellow); margin-top:1.25rem;">Series</li>
          {"".join(series_links)}
        </ul>
      </nav>
    </aside>
    <script>
      (function() {{
        var sb = document.getElementById('sidebar');
        if (sb) {{
          var sp = sessionStorage.getItem('sidebar_scroll_pos');
          if (sp !== null) {{
            sb.scrollTop = parseInt(sp, 10);
          }}
        }}
      }})();
    </script>
    """

def render_mobile_header():
    """Render mobile header bar with toggle button."""
    return """
    <header class="mobile-header">
      <a href="/" class="logo">
        Pulp Fiction <span>eBooks</span>
      </a>
      <button class="mobile-menu-btn" id="mobile-menu-btn" aria-label="Toggle navigation menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </button>
    </header>
    """

def render_footer(engine):
    """Render comprehensive site footer with internal mesh links."""
    return f"""
    <footer class="site-footer">
      <div class="footer-grid">
        <div class="footer-col">
          <h4>Classic Pulp Fiction Ebooks</h4>
          <p>The premier library for vintage pulp fiction ebooks. Featuring French Foreign Legion sagas, pirate swashbucklers, hardboiled 1950s detectives, and untamed African adventures.</p>
        </div>
        <div class="footer-col">
          <h4>Top Genres</h4>
          <ul class="footer-links">
            <li><a href="/genres/desert-adventure-foreign-legion/">Foreign Legion &amp; Desert</a></li>
            <li><a href="/genres/pirate-high-seas-swashbuckler/">Pirate &amp; Swashbuckler</a></li>
            <li><a href="/genres/hardboiled-detective-noir-crime/">Hardboiled Noir Detective</a></li>
            <li><a href="/genres/jungle-adventure-lost-worlds/">Jungle Adventure &amp; Lost Worlds</a></li>
            <li><a href="/genres/masked-rogue-highwayman/">Masked Rogue &amp; Highwayman</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Featured Authors</h4>
          <ul class="footer-links">
            <li><a href="/authors/francois-alwyn-venter/">Francois Alwyn Venter</a></li>
            <li><a href="/authors/gerrie-radlof/">Gerrie Radlof</a></li>
            <li><a href="/authors/braam-le-roux/">Braam le Roux</a></li>
            <li><a href="/authors/sandbergh-beyers/">Sandbergh Beyers</a></li>
            <li><a href="/authors/a-p-du-plessis/">A.P. du Plessis</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Navigation</h4>
          <ul class="footer-links">
            <li><a href="/books/">All 300+ Books</a></li>
            <li><a href="/series/">Book Series</a></li>
            <li><a href="/authors/">All Authors</a></li>
            <li><a href="/genres/">All Genres</a></li>
            <li><a href="/themes/">Niche Themes</a></li>
            <li><a href="/collections/">Curated Collections</a></li>
            <li><a href="/sitemap.xml">XML Sitemap Index</a></li>
          </ul>
        </div>
        <div class="footer-col footer-about">
          <h4>About Us</h4>
          <p><strong>Classic Pulp Fiction Ebooks</strong> is your dedicated source for discovering and enjoying vintage South African pulp fiction, now available as digital ebooks.</p>
          <p>📧 <a href="mailto:haasbroek.pieter@gmail.com">haasbroek.pieter@gmail.com</a></p>
          <p>💬 <a href="https://wa.me/27637722878" target="_blank" rel="noopener">Chat on WhatsApp</a></p>
          <p class="footer-disclaimer">As an Amazon Associate, we earn from qualifying purchases.</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; {datetime.now().year} Classic Pulp Fiction Ebooks. All rights reserved. Built for speed, discovery, and vintage pulp preservation.</p>
      </div>
    </footer>
    """

def render_book_card(book):
    """Render a single high-converting book card."""
    lang_badge = f'<span class="store-badge badge-{slugify(book["lang"])}">{book["lang"]}</span>'
    num_badge = f'<span class="book-number">{book["series_number"]}</span>' if book.get("series_number") and str(book["series_number"]) != "999" else ""

    return f"""
    <article class="book-card" data-series="{escape_html(book['series'])}">
      <div class="book-img-wrapper">
        <a href="/books/{book['slug']}/" aria-label="{escape_html(book['title'])}">
          <img src="{book['img']}" alt="{escape_html(book['title'])} cover" loading="lazy" width="220" height="330">
        </a>
        {num_badge}
        {lang_badge}
      </div>
      <div class="book-content">
        <h3><a href="/books/{book['slug']}/">{escape_html(book['title'])}</a></h3>
        <p class="author">By <a href="/authors/{book['author_slug']}/">{escape_html(book['author'])}</a></p>
        <div class="book-card-actions">
          <a href="{book['amazon_url']}" target="_blank" rel="noopener noreferrer nofollow" class="btn-amazon" aria-label="{escape_html(book['card_btn_label'])} - {escape_html(book['title'])}" data-title="{escape_html(book['title'])}" data-author="{escape_html(book['author'])}" data-genre="{escape_html(book['primary_genre'])}" data-amazon-url="{book['amazon_url']}">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/></svg>
            {escape_html(book['card_btn_label'])}
          </a>
          <a href="/books/{book['slug']}/" class="btn-secondary">Details &amp; Synopsis</a>
        </div>
      </div>
    </article>
    """

def render_base_html(title, meta_desc, canonical_url, json_ld, content_html, active_target="home", og_img=DEFAULT_OG_IMAGE, engine=None, lang="en", is_404=False):
    """Base HTML wrapper with complete technical SEO meta tags, OpenGraph, Twitter, Schema.org, and scripts."""
    if not engine:
        return ""
    sidebar_html = render_sidebar(engine, active_target)
    mobile_header = render_mobile_header()
    footer_html = render_footer(engine)

    robots_directive = "noindex, follow" if is_404 else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    og_locale = "af_ZA" if lang == "af" else "en_US"
    clean_meta_desc = strip_markdown(meta_desc)
    clean_title = strip_markdown(title)
    og_img_url = og_img if og_img.startswith('http') else SITE_URL + og_img

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape_html(clean_title)}</title>
  <meta name="description" content="{escape_html(clean_meta_desc)}" />
  <meta name="robots" content="{robots_directive}" />
  <link rel="canonical" href="{canonical_url}" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  
  <!-- OpenGraph Meta Tags -->
  <meta property="og:site_name" content="{SITE_NAME}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{escape_html(clean_title)}" />
  <meta property="og:description" content="{escape_html(clean_meta_desc)}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:image" content="{og_img_url}" />
  <meta property="og:image:width" content="340" />
  <meta property="og:image:height" content="510" />
  <meta property="og:image:alt" content="{escape_html(clean_title)}" />
  <meta property="og:locale" content="{og_locale}" />
  
  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{escape_html(clean_title)}" />
  <meta name="twitter:description" content="{escape_html(clean_meta_desc)}" />
  <meta name="twitter:image" content="{og_img_url}" />

  <!-- Preconnect and Stylesheet -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="/style.css" />

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
{json.dumps(json_ld, indent=2, ensure_ascii=False)}
  </script>

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-T4XB5JKQYT"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-T4XB5JKQYT');
  </script>
</head>
<body>
  {mobile_header}
  <div class="app-layout">
    {sidebar_html}
    <main class="main-content">
      {content_html}
      {footer_html}
    </main>
  </div>
  <script type="module" src="/main.js"></script>
</body>
</html>"""

class PSEOBuilder:
    def __init__(self, engine, out_dir):
        self.engine = engine
        self.out_dir = out_dir
        self.sitemap_urls = {
            "pages": [],
            "books": [],
            "series": [],
            "authors": [],
            "genres": [],
            "themes": [],
            "collections": []
        }

    def write_page(self, rel_path, html_content):
        """Write HTML content to output directory."""
        full_path = os.path.join(self.out_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def build_all(self):
        """Run complete static programmatic generation."""
        print("Starting Programmatic SEO Generation...")
        self.build_search_index()
        self.build_book_pages()
        self.build_series_pages()
        self.build_author_pages()
        self.build_genre_pages()
        self.build_theme_pages()
        self.build_collection_pages()
        self.build_directory_hubs()
        self.build_homepage()
        self.build_404_page()
        self.build_sitemaps()
        self.build_robots_txt()
        self.build_redirects()
        print(f"PSEO generation finished successfully! Generated {sum(len(v) for v in self.sitemap_urls.values()) + 1} static pages.")

    def build_search_index(self):
        """Generate search-index.json for client-side live autocomplete."""
        print("Generating search-index.json...")
        index_data = {
            "books": [
                {
                    "title": b["title"],
                    "slug": b["slug"],
                    "author": b["author"],
                    "author_slug": b["author_slug"],
                    "series": b["series"],
                    "series_slug": b["series_slug"],
                    "primary_genre": b["primary_genre"],
                    "primary_genre_slug": b["primary_genre_slug"],
                    "lang": b["lang"],
                    "img": b["img"]
                }
                for b in self.engine.books
            ],
            "series": [
                {"name": s["name"], "slug": slug, "count": s["books_count"]}
                for slug, s in self.engine.series.items()
            ],
            "authors": [
                {"name": a["name"], "slug": slug, "count": a["books_count"]}
                for slug, a in self.engine.authors.items()
            ],
            "genres": [
                {"name": g["name"], "slug": slug, "count": g["books_count"]}
                for slug, g in self.engine.genres.items()
            ]
        }
        json_str = json.dumps(index_data, ensure_ascii=False)
        self.write_page("search-index.json", json_str)
        self.write_page("public/search-index.json", json_str)

    def build_book_pages(self):
        """Generate 326 Book Detail Pages (/books/[slug]/index.html)."""
        print(f"Generating {len(self.engine.books)} Book Detail Pages...")
        for book in self.engine.books:
            url = f"{SITE_URL}/books/{book['slug']}/"
            self.sitemap_urls["books"].append({
                "loc": url,
                "lastmod": CURRENT_DATE,
                "changefreq": "monthly",
                "priority": "0.9"
            })

            # Meta tags & language detection
            book_lang = "af" if "afrikaans" in book.get("lang", "").lower() else "en"
            if book.get("store_key") == "kobo":
                title = f"{book['title']} by {book['author']} | Kobo Pulp Ebook"
                meta_desc = f"Read {book['title']} by {book['author']}. Discover vintage {book['primary_genre']} pulp fiction available on Kobo. Instant digital download."
            else:
                title = f"{book['title']} by {book['author']} | Vintage Pulp Ebook"
                meta_desc = f"Read {book['title']} by {book['author']}. Discover vintage {book['primary_genre']} pulp fiction available on Amazon. Instant digital download."
            
            # Related books: More from author
            author_books = [b for b in self.engine.books if b['author'] == book['author'] and b['id'] != book['id']][:4]
            # Similar genre books
            genre_books = [b for b in self.engine.books if b['primary_genre'] == book['primary_genre'] and b['id'] != book['id'] and b['author'] != book['author']][:4]
            if len(genre_books) < 4:
                genre_books = [b for b in self.engine.books if b['id'] != book['id'] and b['id'] not in [ab['id'] for ab in author_books]][:4]

            # Breadcrumbs
            breadcrumbs_html = f"""
            <nav class="breadcrumbs" aria-label="Breadcrumbs">
              <a href="/">Home</a>
              <span class="separator">›</span>
              <a href="/genres/{book['primary_genre_slug']}/">{book['primary_genre']}</a>
              <span class="separator">›</span>
              <span class="current">{escape_html(book['title'])}</span>
            </nav>
            """

            # Tag pills
            tag_pills = [f'<a href="/genres/{book["primary_genre_slug"]}/" class="tag-pill tag-pill-genre">🏷️ {book["primary_genre"]}</a>']
            for th in book["themes"][:4]:
                tag_pills.append(f'<a href="/themes/{slugify(th)}/" class="tag-pill">🎯 {th}</a>')

            content_html = f"""
            {breadcrumbs_html}
            
            <section class="book-detail-hero">
              <div class="book-detail-cover-wrapper">
                <img src="{book['img']}" alt="{escape_html(book['title'])} - Book Cover" width="340" height="510" fetchpriority="high">
              </div>
              <div class="book-detail-info">
                <div class="tags-row" style="margin-top:0;">
                  <span class="store-badge badge-{slugify(book['lang'])}" style="position:static; margin-right:0.5rem;">{book['lang']} Edition</span>
                  {f'<span class="tag-pill" style="color:#fff; background:var(--accent-red); border-color:var(--accent-red);">Book #{book["series_number"]}</span>' if book.get("series_number") and str(book["series_number"]) != "999" else ""}
                </div>
                <h1>{escape_html(book['title'])}</h1>
                <div class="book-detail-meta-bar">
                  <span>Author: <a href="/authors/{book['author_slug']}/" class="author-link">{escape_html(book['author'])}</a></span>
                  {f'<span>Series: <a href="/series/{book["series_slug"]}/" style="font-weight:700; color:var(--accent-yellow);">{escape_html(book["series"])}</a></span>' if book.get("series") and book["series"] != "Other" else ""}
                  <span>Format: <strong>{book['format']}</strong></span>
                  <span>⭐ <a href="{book['amazon_url']}" target="_blank" rel="noopener noreferrer nofollow" class="reviews-link">{book['reviews_label']} &rarr;</a></span>
                </div>

                <div class="tags-row">
                  {"".join(tag_pills)}
                </div>

                <div class="book-synopsis">
                  <h2 style="font-size:1.3rem; margin-bottom:0.75rem; color:var(--text-main);">Book Synopsis &amp; Story Overview</h2>
                  <p>{book['synopsis'].replace(chr(10), '<br><br>')}</p>
                </div>

                <div class="book-specs-grid">
                  <div class="spec-item">
                    <span class="spec-label">Language</span>
                    <span class="spec-val">{book['lang']}</span>
                  </div>
                  <div class="spec-item">
                    <span class="spec-label">Read Time</span>
                    <span class="spec-val">{book['read_time']}</span>
                  </div>
                  <div class="spec-item">
                    <span class="spec-label">Publisher</span>
                    <span class="spec-val">Softcover Books</span>
                  </div>
                  <div class="spec-item">
                    <span class="spec-label">Availability</span>
                    <span class="spec-val" style="color:#00e676;">{book['delivery']}</span>
                  </div>
                  <div class="spec-item">
                    <span class="spec-label">Price</span>
                    <span class="spec-val" style="color:var(--accent-yellow);"><a href="{book['amazon_url']}" target="_blank" rel="noopener noreferrer nofollow" style="color:var(--accent-yellow); text-decoration:none;">Check on {book['store_name']} &rarr;</a></span>
                  </div>
                </div>

                <div style="margin-top:1rem; display:flex; flex-wrap:wrap; gap:1rem; align-items:center;">
                  <a href="{book['amazon_url']}" target="_blank" rel="noopener noreferrer nofollow" class="btn-amazon btn-amazon-lg" data-title="{escape_html(book['title'])}" data-author="{escape_html(book['author'])}" data-genre="{escape_html(book['primary_genre'])}" data-amazon-url="{book['amazon_url']}">
                    <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/></svg>
                    {book['detail_btn_label']}
                  </a>
                  <span style="font-size:0.85rem; color:var(--text-dim);">Read instantly on {book['devices']}.</span>
                </div>
              </div>
            </section>

            <!-- More From Author -->
            {f'''
            <section style="margin-bottom:3.5rem;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
                <h2>More Vintage Pulp by {escape_html(book['author'])}</h2>
                <a href="/authors/{book['author_slug']}/" style="font-weight:700; font-size:0.9rem;">View All ({len(self.engine.authors[book['author_slug']]['books'])}) &rarr;</a>
              </div>
              <div class="product-grid">
                {"".join([render_book_card(ab) for ab in author_books])}
              </div>
            </section>
            ''' if author_books else ''}

            <!-- Similar Genre Ebooks -->
            <section style="margin-bottom:3.5rem;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
                <h2>Similar {escape_html(book['primary_genre'])} Ebooks</h2>
                <a href="/genres/{book['primary_genre_slug']}/" style="font-weight:700; font-size:0.9rem;">Explore Genre ({self.engine.genres[book['primary_genre_slug']]['books_count']}) &rarr;</a>
              </div>
              <div class="product-grid">
                {"".join([render_book_card(gb) for gb in genre_books])}
              </div>
            </section>
            """

            # JSON-LD Structured Data
            clean_synopsis = strip_markdown(book["synopsis"])
            json_ld = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "Book",
                        "@id": f"{url}#book",
                        "mainEntityOfPage": url,
                        "url": url,
                        "sameAs": book["amazon_url"],
                        "name": book["title"],
                        "author": {
                            "@type": "Person",
                            "name": book["author"],
                            "url": f"{SITE_URL}/authors/{book['author_slug']}/"
                        },
                        "image": f"{SITE_URL}{book['img']}",
                        "description": clean_synopsis,
                        "inLanguage": book["lang"],
                        "genre": book["primary_genre"],
                        "bookFormat": "https://schema.org/EBook",
                        "publisher": {
                            "@type": "Organization",
                            "name": PUBLISHER_NAME,
                            "logo": {"@type": "ImageObject", "url": PUBLISHER_LOGO}
                        }
                    },
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                            {"@type": "ListItem", "position": 2, "name": book["primary_genre"], "item": f"{SITE_URL}/genres/{book['primary_genre_slug']}/"},
                            {"@type": "ListItem", "position": 3, "name": book["title"], "item": url}
                        ]
                    }
                ]
            }

            html = render_base_html(
                title=title,
                meta_desc=meta_desc,
                canonical_url=url,
                json_ld=json_ld,
                content_html=content_html,
                active_target="books",
                og_img=book["img"],
                engine=self.engine,
                lang=book_lang
            )
            self.write_page(f"books/{book['slug']}/index.html", html)

    def build_series_pages(self):
        """Generate Series Pages (/series/[slug]/index.html)."""
        print(f"Generating {len(self.engine.series)} Series Pages...")
        for slug, series in self.engine.series.items():
            url = f"{SITE_URL}/series/{slug}/"
            self.sitemap_urls["series"].append({
                "loc": url,
                "lastmod": CURRENT_DATE,
                "changefreq": "weekly",
                "priority": "0.85"
            })

            series_lang = "af" if any("afrikaans" in l.lower() for l in series["languages"]) and not any("english" in l.lower() for l in series["languages"]) else "en"
            title = f"{series['name']} - Complete Pulp Series Reading Order | Softcover Books"
            meta_desc = f"Discover all {series['books_count']} books in {series['name']}. Read story synopses, browse cover art, and buy digital editions in chronological order."

            breadcrumbs_html = f"""
            <nav class="breadcrumbs" aria-label="Breadcrumbs">
              <a href="/">Home</a>
              <span class="separator">›</span>
              <a href="/series/">Series</a>
              <span class="separator">›</span>
              <span class="current">{escape_html(series['name'])}</span>
            </nav>
            """

            genre_pills = [f'<a href="/genres/{slugify(g)}/" class="tag-pill tag-pill-genre">🏷️ {g}</a>' for g in series["genres"]]
            lang_pills = [f'<span class="store-badge badge-{slugify(l)}" style="position:static; margin-right:0.4rem;">{l}</span>' for l in series["languages"]]

            content_html = f"""
            {breadcrumbs_html}
            
            <section class="hub-hero">
              <div class="hero-badge">📖 Complete Book Series</div>
              <h1>{escape_html(series['name'])}</h1>
              <p class="hub-tagline">{series['books_count']} Thrilling Books in Chronological Reading Order</p>
              <div class="tags-row" style="margin-bottom:1rem;">
                <span style="font-size:0.9rem; color:var(--text-dim); margin-right:0.5rem;">Languages:</span>
                {"".join(lang_pills)}
              </div>
              <div class="tags-row" style="margin-bottom:1.5rem;">
                {"".join(genre_pills)}
              </div>
              <p class="hub-description">{escape_html(series['description'])}</p>
            </section>

            <section style="margin-bottom:3rem;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
                <h2>All {series['books_count']} Books in {escape_html(series['name'])} (Reading Order)</h2>
              </div>
              <div class="product-grid">
                {"".join([render_book_card(b) for b in series['books']])}
              </div>
            </section>
            """

            clean_series_desc = strip_markdown(series["description"])
            json_ld = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "CollectionPage",
                        "@id": url,
                        "name": f"{series['name']} - Book Series",
                        "description": clean_series_desc
                    },
                    {
                        "@type": "ItemList",
                        "name": f"Books in {series['name']}",
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": idx + 1,
                                "name": b["title"],
                                "url": f"{SITE_URL}/books/{b['slug']}/"
                            }
                            for idx, b in enumerate(series["books"])
                        ]
                    },
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                            {"@type": "ListItem", "position": 2, "name": "Series", "item": f"{SITE_URL}/series/"},
                            {"@type": "ListItem", "position": 3, "name": series["name"], "item": url}
                        ]
                    }
                ]
            }

            html = render_base_html(
                title=title,
                meta_desc=meta_desc,
                canonical_url=url,
                json_ld=json_ld,
                content_html=content_html,
                active_target=f"series-{slug}",
                og_img=series["sample_covers"][0] if series["sample_covers"] else DEFAULT_OG_IMAGE,
                engine=self.engine,
                lang=series_lang
            )
            self.write_page(f"series/{slug}/index.html", html)

    def build_author_pages(self):
        """Generate Author Hub Pages (/authors/[slug]/index.html)."""
        print(f"Generating {len(self.engine.authors)} Author Hub Pages...")
        for slug, author in self.engine.authors.items():
            url = f"{SITE_URL}/authors/{slug}/"
            self.sitemap_urls["authors"].append({
                "loc": url,
                "lastmod": CURRENT_DATE,
                "changefreq": "weekly",
                "priority": "0.8"
            })

            title = f"{author['name']} - Vintage Pulp Fiction Bibliography | Softcover Books"
            meta_desc = f"Explore classic vintage pulp fiction ebooks by {author['name']}. Browse {author['books_count']} legendary paperback novels in digital editions."

            breadcrumbs_html = f"""
            <nav class="breadcrumbs" aria-label="Breadcrumbs">
              <a href="/">Home</a>
              <span class="separator">›</span>
              <a href="/authors/">Authors</a>
              <span class="separator">›</span>
              <span class="current">{escape_html(author['name'])}</span>
            </nav>
            """

            genre_pills = [f'<a href="/genres/{slugify(g)}/" class="tag-pill tag-pill-genre">🏷️ {g}</a>' for g in author["primary_genres"]]

            content_html = f"""
            {breadcrumbs_html}
            
            <section class="hub-hero">
              <div class="hero-badge">✍️ Author Spotlight</div>
              <h1>{escape_html(author['name'])}</h1>
              <p class="hub-tagline">{author['books_count']} Classic Pulp Fiction Ebooks in Complete Bibliography</p>
              <div class="tags-row" style="margin-bottom:1.5rem;">
                {"".join(genre_pills)}
              </div>
              <p class="hub-description">{escape_html(author['bio'])}</p>
            </section>

            <section style="margin-bottom:3rem;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
                <h2>Complete Bibliography by {escape_html(author['name'])} ({author['books_count']} Titles)</h2>
              </div>
              <div class="product-grid">
                {"".join([render_book_card(b) for b in author['books']])}
              </div>
            </section>
            """

            clean_bio = strip_markdown(author["bio"])
            json_ld = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "ProfilePage",
                        "@id": url,
                        "name": f"{author['name']} - Author Bibliography",
                        "mainEntity": {
                            "@type": "Person",
                            "name": author["name"],
                            "description": clean_bio
                        }
                    },
                    {
                        "@type": "ItemList",
                        "name": f"Pulp Fiction Ebooks by {author['name']}",
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": idx + 1,
                                "name": b["title"],
                                "url": f"{SITE_URL}/books/{b['slug']}/"
                            }
                            for idx, b in enumerate(author["books"])
                        ]
                    },
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                            {"@type": "ListItem", "position": 2, "name": "Authors", "item": f"{SITE_URL}/authors/"},
                            {"@type": "ListItem", "position": 3, "name": author["name"], "item": url}
                        ]
                    }
                ]
            }

            html = render_base_html(
                title=title,
                meta_desc=meta_desc,
                canonical_url=url,
                json_ld=json_ld,
                content_html=content_html,
                active_target="authors",
                og_img=author["sample_covers"][0] if author["sample_covers"] else DEFAULT_OG_IMAGE,
                engine=self.engine
            )
            self.write_page(f"authors/{slug}/index.html", html)

    def build_genre_pages(self):
        """Generate Genre Hub & Subgenre Pages (/genres/[slug]/index.html)."""
        print(f"Generating {len(self.engine.genres)} Genre Hub Pages...")
        # Clean up obsolete genre directories
        genres_dir = os.path.join(self.out_dir, "genres")
        if os.path.exists(genres_dir):
            valid_slugs = set(self.engine.genres.keys())
            for item in os.listdir(genres_dir):
                item_path = os.path.join(genres_dir, item)
                if os.path.isdir(item_path) and item not in valid_slugs:
                    shutil.rmtree(item_path, ignore_errors=True)

        for slug, genre in self.engine.genres.items():
            url = f"{SITE_URL}/genres/{slug}/"
            self.sitemap_urls["genres"].append({
                "loc": url,
                "lastmod": CURRENT_DATE,
                "changefreq": "weekly",
                "priority": "0.85"
            })

            title = f"{genre['title']} | Softcover Books"
            meta_desc = f"Discover {genre['books_count']}+ classic {genre['name']} vintage pulp fiction novels available online. {genre['tagline']}."

            breadcrumbs_html = f"""
            <nav class="breadcrumbs" aria-label="Breadcrumbs">
              <a href="/">Home</a>
              <span class="separator">›</span>
              <a href="/genres/">Genres</a>
              <span class="separator">›</span>
              <span class="current">{escape_html(genre['name'])}</span>
            </nav>
            """

            trope_pills = [f'<span class="tag-pill">🔥 {t}</span>' for t in genre.get("tropes", [])]
            subgenre_pills = [f'<a href="/genres/{slugify(sg)}/" class="tag-pill tag-pill-genre">🏷️ {sg}</a>' for sg in genre.get("subgenres", [])]

            content_html = f"""
            {breadcrumbs_html}
            
            <section class="hub-hero">
              <div class="hero-badge">🏷️ Pulp Fiction Genre Guide</div>
              <h1>{escape_html(genre['title'])}</h1>
              <p class="hub-tagline">{escape_html(genre['tagline'])}</p>
              
              {f'<div class="tags-row" style="margin-bottom:1rem;"><strong>Key Tropes:</strong> {"".join(trope_pills)}</div>' if trope_pills else ''}
              {f'<div class="tags-row" style="margin-bottom:1.5rem;"><strong>Subgenres:</strong> {"".join(subgenre_pills)}</div>' if subgenre_pills else ''}

              <p class="hub-description">{escape_html(genre['guide'])}</p>
            </section>

            <section style="margin-bottom:3rem;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
                <h2>Explore All {genre['books_count']} {escape_html(genre['name'])} Ebooks</h2>
              </div>
              <div class="product-grid">
                {"".join([render_book_card(b) for b in genre['books']])}
              </div>
            </section>
            """

            clean_guide = strip_markdown(genre["guide"])
            json_ld = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "CollectionPage",
                        "@id": url,
                        "name": genre["title"],
                        "description": clean_guide
                    },
                    {
                        "@type": "ItemList",
                        "name": f"Pulp Fiction Ebooks in {genre['name']}",
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": idx + 1,
                                "name": b["title"],
                                "url": f"{SITE_URL}/books/{b['slug']}/"
                            }
                            for idx, b in enumerate(genre["books"])
                        ]
                    },
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                            {"@type": "ListItem", "position": 2, "name": "Genres", "item": f"{SITE_URL}/genres/"},
                            {"@type": "ListItem", "position": 3, "name": genre["name"], "item": url}
                        ]
                    }
                ]
            }

            html = render_base_html(
                title=title,
                meta_desc=meta_desc,
                canonical_url=url,
                json_ld=json_ld,
                content_html=content_html,
                active_target=f"genre-{slug}",
                og_img=genre["books"][0]["img"] if genre["books"] else DEFAULT_OG_IMAGE,
                engine=self.engine
            )
            self.write_page(f"genres/{slug}/index.html", html)

    def build_theme_pages(self):
        """Generate Niche Theme/Tag Landing Pages (/themes/[slug]/index.html)."""
        print(f"Generating {len(self.engine.themes)} Niche Theme Pages...")
        # Clean up obsolete theme directories
        themes_dir = os.path.join(self.out_dir, "themes")
        if os.path.exists(themes_dir):
            valid_slugs = set(self.engine.themes.keys())
            for item in os.listdir(themes_dir):
                item_path = os.path.join(themes_dir, item)
                if os.path.isdir(item_path) and item not in valid_slugs:
                    shutil.rmtree(item_path, ignore_errors=True)

        for slug, theme in self.engine.themes.items():
            url = f"{SITE_URL}/themes/{slug}/"
            self.sitemap_urls["themes"].append({
                "loc": url,
                "lastmod": CURRENT_DATE,
                "changefreq": "monthly",
                "priority": "0.75"
            })

            title = f"{theme['title']} | Softcover Books"
            meta_desc = f"Browse vintage {theme['name']} pulp fiction ebooks. Discover {theme['books_count']} exciting retro paperback novels."

            breadcrumbs_html = f"""
            <nav class="breadcrumbs" aria-label="Breadcrumbs">
              <a href="/">Home</a>
              <span class="separator">›</span>
              <a href="/themes/">Themes</a>
              <span class="separator">›</span>
              <span class="current">{escape_html(theme['name'])}</span>
            </nav>
            """

            # Related themes
            all_other_themes = [t for t_slug, t in self.engine.themes.items() if t_slug != slug]
            h = sum(ord(c) for c in slug) % (len(all_other_themes) - 6 if len(all_other_themes) > 6 else 1)
            related_themes = all_other_themes[h:h+6]
            related_themes_html = "".join([f'<a href="/themes/{t["slug"]}/" class="tag-pill" style="padding:0.4rem 0.8rem; font-size:0.85rem;">🎯 {t["name"]} ({t["books_count"]})</a>' for t in related_themes])

            content_html = f"""
            {breadcrumbs_html}
            
            <section class="hub-hero">
              <div class="hero-badge">🎯 Niche Pulp Theme</div>
              <h1>{escape_html(theme['name'])} Pulp Fiction Ebooks</h1>
              <p class="hub-tagline">{escape_html(theme['tagline'])}</p>
              <p class="hub-description">{escape_html(theme['guide'])}</p>
            </section>

            <section style="margin-bottom:3rem;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
                <h2>Featured {escape_html(theme['name'])} Titles ({theme['books_count']})</h2>
              </div>
              <div class="product-grid">
                {"".join([render_book_card(b) for b in theme['books']])}
              </div>
            </section>

            <section style="margin-top:2.5rem; margin-bottom:3rem; border-top:1px solid var(--border); padding-top:1.5rem;">
              <h3 style="font-size:1.2rem; margin-bottom:1rem; color:var(--text-main);">Explore Related Pulp Themes</h3>
              <div class="tags-row" style="margin-top:0.5rem;">
                {related_themes_html}
              </div>
            </section>
            """

            clean_theme_guide = strip_markdown(theme["guide"])
            json_ld = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "CollectionPage",
                        "@id": url,
                        "name": theme["title"],
                        "description": clean_theme_guide
                    },
                    {
                        "@type": "ItemList",
                        "name": f"Pulp Fiction Novels featuring {theme['name']}",
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": idx + 1,
                                "name": b["title"],
                                "url": f"{SITE_URL}/books/{b['slug']}/"
                            }
                            for idx, b in enumerate(theme["books"])
                        ]
                    },
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                            {"@type": "ListItem", "position": 2, "name": "Themes", "item": f"{SITE_URL}/themes/"},
                            {"@type": "ListItem", "position": 3, "name": theme["name"], "item": url}
                        ]
                    }
                ]
            }

            html = render_base_html(
                title=title,
                meta_desc=meta_desc,
                canonical_url=url,
                json_ld=json_ld,
                content_html=content_html,
                active_target="themes",
                og_img=theme["books"][0]["img"] if theme["books"] else DEFAULT_OG_IMAGE,
                engine=self.engine
            )
            self.write_page(f"themes/{slug}/index.html", html)

    def build_collection_pages(self):
        """Generate 550+ Curated Collection Landing Pages (/collections/[slug]/index.html)."""
        print(f"Generating {len(self.engine.collections)} Curated Collection Pages...")
        # Clean up obsolete collection directories
        col_dir = os.path.join(self.out_dir, "collections")
        if os.path.exists(col_dir):
            valid_slugs = set(col["slug"] for col in self.engine.collections)
            for item in os.listdir(col_dir):
                item_path = os.path.join(col_dir, item)
                if os.path.isdir(item_path) and item not in valid_slugs:
                    shutil.rmtree(item_path, ignore_errors=True)

        for col in self.engine.collections:
            url = f"{SITE_URL}/collections/{col['slug']}/"
            self.sitemap_urls["collections"].append({
                "loc": url,
                "lastmod": CURRENT_DATE,
                "changefreq": "monthly",
                "priority": "0.8"
            })

            title = f"{col['title']} - Curated Pulp Ebooks | Softcover Books"
            meta_desc = f"{col['description']} Read top-rated vintage pulp fiction books in digital editions today."

            breadcrumbs_html = f"""
            <nav class="breadcrumbs" aria-label="Breadcrumbs">
              <a href="/">Home</a>
              <span class="separator">›</span>
              <a href="/collections/">Collections</a>
              <span class="separator">›</span>
              <span class="current">{escape_html(col['title'])}</span>
            </nav>
            """

            # Related collections (same category or nearby)
            same_cat = [c for c in self.engine.collections if c['slug'] != col['slug'] and c.get('category') == col.get('category')]
            if len(same_cat) >= 4:
                related_cols = same_cat[:4]
            else:
                h = sum(ord(c) for c in col['slug']) % (len(self.engine.collections) - 5)
                related_cols = [c for c in self.engine.collections[h:h+6] if c['slug'] != col['slug']][:4]

            related_cols_html = "".join([
                f'<a href="/collections/{rc["slug"]}/" style="display:block; padding:1rem; background:var(--bg-surface); border:1px solid var(--border); border-radius:8px; text-decoration:none; color:inherit; transition:border-color 0.2s, transform 0.2s;">'
                f'<strong style="color:var(--accent-yellow); display:block; margin-bottom:0.25rem; font-size:0.95rem;">⭐ {escape_html(rc["title"])}</strong>'
                f'<span style="font-size:0.8rem; color:var(--text-dim); line-height:1.4; display:block;">{escape_html(rc["description"][:110])}...</span>'
                f'</a>'
                for rc in related_cols
            ])

            content_html = f"""
            {breadcrumbs_html}
            
            <section class="hub-hero">
              <div class="hero-badge">⭐ Curated Reading List</div>
              <h1>{escape_html(col['title'])}</h1>
              <p class="hub-tagline">Handpicked selection of {col['books_count']} thrilling pulp fiction ebooks</p>
              <p class="hub-description">{escape_html(col['description'])} Discover high-velocity plots, unforgettable vintage characters, and instant digital reading.</p>
            </section>

            <section style="margin-bottom:3rem;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
                <h2>Ranked Book Recommendations ({col['books_count']} Ebooks)</h2>
              </div>
              <div class="product-grid">
                {"".join([render_book_card(b) for b in col['books']])}
              </div>
            </section>

            <section style="margin-top:2.5rem; margin-bottom:3rem; border-top:1px solid var(--border); padding-top:1.5rem;">
              <h3 style="font-size:1.2rem; margin-bottom:1rem; color:var(--text-main);">Related Curated Lists &amp; Reading Guides</h3>
              <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:1rem;">
                {related_cols_html}
              </div>
            </section>
            """

            clean_col_desc = strip_markdown(col["description"])
            json_ld = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "CollectionPage",
                        "@id": url,
                        "name": col["title"],
                        "description": clean_col_desc
                    },
                    {
                        "@type": "ItemList",
                        "name": col["title"],
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": idx + 1,
                                "name": b["title"],
                                "url": f"{SITE_URL}/books/{b['slug']}/"
                            }
                            for idx, b in enumerate(col["books"])
                        ]
                    },
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                            {"@type": "ListItem", "position": 2, "name": "Collections", "item": f"{SITE_URL}/collections/"},
                            {"@type": "ListItem", "position": 3, "name": col["title"], "item": url}
                        ]
                    }
                ]
            }

            html = render_base_html(
                title=title,
                meta_desc=meta_desc,
                canonical_url=url,
                json_ld=json_ld,
                content_html=content_html,
                active_target="collections",
                og_img=col["books"][0]["img"] if col["books"] else DEFAULT_OG_IMAGE,
                engine=self.engine
            )
            self.write_page(f"collections/{col['slug']}/index.html", html)

    def build_directory_hubs(self):
        """Generate Directory Hub Index Pages: /books/, /authors/, /genres/, /themes/, /collections/, /series/."""
        print("Generating Directory Hub Index Pages...")

        # 1. /books/index.html
        books_url = f"{SITE_URL}/books/"
        self.sitemap_urls["pages"].append({"loc": books_url, "lastmod": CURRENT_DATE, "changefreq": "daily", "priority": "1.0"})
        books_content = f"""
        <section class="hero">
          <div class="hero-badge">📚 Complete Library Catalog</div>
          <h1>All {len(self.engine.books)} Vintage Pulp Fiction Ebooks</h1>
          <p>Search, filter, and discover classic French Foreign Legion adventures, swashbuckling pirates, hardboiled crime sleuths, and lost jungle worlds.</p>
        </section>

        <form action="/books/" method="get" class="pseo-search-container" role="search" onsubmit="return false;">
          <svg class="pseo-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="search" name="q" id="pseo-search" class="pseo-search-input" placeholder="Search by title, author, or series keyword..." autocomplete="off">
          <div id="search-results-count" style="margin-top:0.5rem; font-size:0.85rem; color:var(--accent-yellow);"></div>
        </form>

        <div id="no-results-msg" class="no-results-card" style="display:none;">
          <h3>No matching books found</h3>
          <p>We couldn't find any books matching your search. Try searching for an author, series, or keyword.</p>
          <button type="button" class="btn btn-primary" id="clear-search-btn" style="margin-top:1rem; cursor:pointer;">Show All Books</button>
        </div>

        <div class="product-grid">
          {"".join([render_book_card(b) for b in self.engine.books])}
        </div>
        """
        books_json_ld = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": f"All {len(self.engine.books)} Vintage Pulp Fiction Ebooks",
            "url": books_url,
            "description": "Complete library catalog of vintage pulp fiction ebooks available in digital editions."
        }
        self.write_page("books/index.html", render_base_html(
            title=f"All {len(self.engine.books)} Vintage Pulp Fiction Ebooks | Softcover Books",
            meta_desc=f"Browse our complete catalog of {len(self.engine.books)} vintage pulp fiction ebooks. Search desert adventures, pirate sagas, noir mysteries, and jungle pulp.",
            canonical_url=books_url,
            json_ld=books_json_ld,
            content_html=books_content,
            active_target="books",
            engine=self.engine
        ))

        # 2. /authors/index.html
        authors_url = f"{SITE_URL}/authors/"
        self.sitemap_urls["pages"].append({"loc": authors_url, "lastmod": CURRENT_DATE, "changefreq": "weekly", "priority": "0.9"})
        authors_cards = []
        for slug, a in self.engine.authors.items():
            authors_cards.append(f"""
            <a href="/authors/{slug}/" class="directory-card">
              <h3>{escape_html(a['name'])}</h3>
              <p>{escape_html(a['bio'][:140])}...</p>
              <div class="card-footer">
                <span>{a['books_count']} Ebooks Available</span>
                <span>View Bibliography &rarr;</span>
              </div>
            </a>
            """)
        authors_content = f"""
        <section class="hero">
          <div class="hero-badge">✍️ Master Pulp Storytellers</div>
          <h1>Pulp Fiction Authors Directory</h1>
          <p>Explore the celebrated literary giants and vintage paperback authors behind our classic pulp fiction catalog.</p>
        </section>
        <div class="directory-grid">
          {"".join(authors_cards)}
        </div>
        """
        self.write_page("authors/index.html", render_base_html(
            title="Pulp Fiction Authors Directory | Softcover Books",
            meta_desc="Discover the legendary pulp fiction authors behind our vintage catalog, including F.A. Venter, Gerrie Radlof, Braam le Roux, and Sandbergh Beyers.",
            canonical_url=authors_url,
            json_ld={"@context": "https://schema.org", "@type": "CollectionPage", "name": "Pulp Fiction Authors", "url": authors_url},
            content_html=authors_content,
            active_target="authors",
            engine=self.engine
        ))

        # 3. /genres/index.html
        genres_url = f"{SITE_URL}/genres/"
        self.sitemap_urls["pages"].append({"loc": genres_url, "lastmod": CURRENT_DATE, "changefreq": "weekly", "priority": "0.9"})
        genres_cards = []
        for slug, g in self.engine.genres.items():
            genres_cards.append(f"""
            <a href="/genres/{slug}/" class="directory-card">
              <h3>{escape_html(g['name'])}</h3>
              <p>{escape_html(g['tagline'])}</p>
              <div class="card-footer">
                <span>{g['books_count']} Titles</span>
                <span>Explore Genre &rarr;</span>
              </div>
            </a>
            """)
        genres_content = f"""
        <section class="hero">
          <div class="hero-badge">🏷️ Categorized Taxonomy</div>
          <h1>Pulp Fiction Genres &amp; Subgenres</h1>
          <p>Browse by genre: French Foreign Legion military action, pirate swashbucklers, hardboiled 1950s crime noir, safari mysteries, and retro sci-fi space operas.</p>
        </section>
        <div class="directory-grid">
          {"".join(genres_cards)}
        </div>
        """
        self.write_page("genres/index.html", render_base_html(
            title="Pulp Fiction Genres & Categories | Softcover Books",
            meta_desc="Browse our complete directory of classic pulp fiction genres and subgenres. Foreign Legion, pirates, detectives, jungle action, and space opera.",
            canonical_url=genres_url,
            json_ld={"@context": "https://schema.org", "@type": "CollectionPage", "name": "Pulp Fiction Genres", "url": genres_url},
            content_html=genres_content,
            active_target="genres",
            engine=self.engine
        ))

        # 4. /themes/index.html
        themes_url = f"{SITE_URL}/themes/"
        self.sitemap_urls["pages"].append({"loc": themes_url, "lastmod": CURRENT_DATE, "changefreq": "weekly", "priority": "0.85"})
        themes_cards = []
        for slug, th in self.engine.themes.items():
            themes_cards.append(f"""
            <a href="/themes/{slug}/" class="directory-card">
              <h3>🎯 {escape_html(th['name'])}</h3>
              <p>{escape_html(th['tagline'])}</p>
              <div class="card-footer">
                <span>{th['books_count']} Ebooks</span>
                <span>Browse Theme &rarr;</span>
              </div>
            </a>
            """)
        themes_content = f"""
        <section class="hero">
          <div class="hero-badge">🎯 Niche Tropes &amp; Keywords</div>
          <h1>Pulp Fiction Niche Themes Directory</h1>
          <p>Explore specialized long-tail pulp themes: Private Eyes, Desert Caravans, Cannon Broadsides, Masked Jungle Adventurers, and Radio Drama Cliffhangers.</p>
        </section>
        <div class="directory-grid">
          {"".join(themes_cards)}
        </div>
        """
        self.write_page("themes/index.html", render_base_html(
            title="Pulp Fiction Niche Themes & Tropes | Softcover Books",
            meta_desc="Explore over 75+ niche pulp fiction themes and long-tail tropes. Private eyes, space opera, foreign legion, and lost cities.",
            canonical_url=themes_url,
            json_ld={"@context": "https://schema.org", "@type": "CollectionPage", "name": "Pulp Fiction Themes", "url": themes_url},
            content_html=themes_content,
            active_target="themes",
            engine=self.engine
        ))

        # 5. /collections/index.html
        collections_url = f"{SITE_URL}/collections/"
        self.sitemap_urls["pages"].append({"loc": collections_url, "lastmod": CURRENT_DATE, "changefreq": "daily", "priority": "0.95"})
        col_cards = []
        for col in self.engine.collections[:60]:
            col_cards.append(f"""
            <a href="/collections/{col['slug']}/" class="directory-card">
              <h3>⭐ {escape_html(col['title'])}</h3>
              <p>{escape_html(col['description'][:140])}...</p>
              <div class="card-footer">
                <span>{col['books_count']} Curated Titles</span>
                <span>View List &rarr;</span>
              </div>
            </a>
            """)
        col_content = f"""
        <section class="hero">
          <div class="hero-badge">⭐ Curated Reading Guides</div>
          <h1>Curated Thematic Pulp Fiction Collections</h1>
          <p>Browse our editorial reading lists, top-10 rankings, and buyer guides for vintage pulp fiction ebooks.</p>
        </section>
        <div class="directory-grid">
          {"".join(col_cards)}
        </div>
        """
        self.write_page("collections/index.html", render_base_html(
            title="Curated Pulp Fiction Collections & Reading Guides | Softcover Books",
            meta_desc="Discover over 500+ curated thematic pulp fiction lists, rankings, and reading guides. Find your next favorite retro adventure.",
            canonical_url=collections_url,
            json_ld={"@context": "https://schema.org", "@type": "CollectionPage", "name": "Curated Collections", "url": collections_url},
            content_html=col_content,
            active_target="collections",
            engine=self.engine
        ))

        # 6. /series/index.html
        series_url = f"{SITE_URL}/series/"
        self.sitemap_urls["pages"].append({"loc": series_url, "lastmod": CURRENT_DATE, "changefreq": "weekly", "priority": "0.95"})
        series_cards = []
        for slug, s in sorted(self.engine.series.items(), key=lambda x: -x[1]["books_count"]):
            series_cards.append(f"""
            <a href="/series/{slug}/" class="directory-card">
              <h3>📖 {escape_html(s['name'])}</h3>
              <p>{escape_html(s['description'][:140])}...</p>
              <div class="card-footer">
                <span>{s['books_count']} Books in Series</span>
                <span>View Reading Order &rarr;</span>
              </div>
            </a>
            """)
        series_content = f"""
        <section class="hero">
          <div class="hero-badge">📖 Complete Series Archive</div>
          <h1>Pulp Fiction Book Series Directory</h1>
          <p>Explore all {len(self.engine.series)} classic pulp fiction book series in complete chronological reading order. Desert foreign legion sagas, pirate epics, jungle adventures, and detective thrillers.</p>
        </section>
        <div class="directory-grid">
          {"".join(series_cards)}
        </div>
        """
        self.write_page("series/index.html", render_base_html(
            title="Pulp Fiction Book Series Directory & Reading Lists | Softcover Books",
            meta_desc=f"Explore all {len(self.engine.series)} classic vintage pulp fiction book series. Browse complete reading orders, cover art, and digital editions.",
            canonical_url=series_url,
            json_ld={"@context": "https://schema.org", "@type": "CollectionPage", "name": "Pulp Fiction Book Series", "url": series_url},
            content_html=series_content,
            active_target="series",
            engine=self.engine
        ))

    def build_homepage(self):
        """Generate high-converting, premium Homepage (/index.html)."""
        print("Generating Main Homepage...")
        home_url = f"{SITE_URL}/"
        # Add Homepage to primary pages sitemap with top priority
        self.sitemap_urls["pages"].insert(0, {"loc": home_url, "lastmod": CURRENT_DATE, "changefreq": "daily", "priority": "1.0"})

        featured_books = self.engine.books[:12]
        top_collections = self.engine.collections[:8]
        top_series = sorted(self.engine.series.values(), key=lambda x: -x["books_count"])[:6]

        content_html = f"""
        <section class="hero">
          <div class="hero-badge">🐆 Vintage Pulp Fiction Ebook Library</div>
          <h1>Classic Pulp Fiction Ebooks</h1>
          <p>Welcome to the ultimate digital archive of vintage pulp fiction. Discover over 300+ action-packed novels across French Foreign Legion warfare, pirate swashbucklers, hardboiled noir crime, and untamed jungle adventures.</p>
          
          <form action="/books/" method="get" class="pseo-search-container" role="search" style="margin-top:2rem;">
            <svg class="pseo-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input type="search" name="q" id="pseo-search" class="pseo-search-input" placeholder="Search 300+ titles, authors, or genres..." autocomplete="off">
            <div id="search-dropdown" class="search-dropdown" style="display:none;" aria-expanded="false"></div>
          </form>
          <div style="margin-top:1.25rem; text-align:center;">
            <a href="https://amzn.to/4qiRkFR" target="_blank" rel="noopener noreferrer nofollow" id="amazon-author-page-btn" style="display:inline-flex; align-items:center; gap:0.6rem; background:#FF9900; color:#111; font-weight:700; font-size:0.95rem; letter-spacing:0.01em; padding:0.75rem 1.6rem; border-radius:8px; text-decoration:none; box-shadow:0 2px 8px rgba(255,153,0,0.25);">
              &#128218; Amazon Author Page &#8211; 277 Pulp Fiction Ebooks
            </a>
          </div>
        </section>

        <div class="stats-banner">
          <div class="stat-card">
            <span class="stat-number">{len(self.engine.books)}</span>
            <span class="stat-label">Pulp Ebooks</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{len(self.engine.series)}</span>
            <span class="stat-label">Book Series</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{len(self.engine.authors)}</span>
            <span class="stat-label">Pulp Authors</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{len(self.engine.genres)}</span>
            <span class="stat-label">Genres &amp; Subgenres</span>
          </div>
        </div>

        <!-- Featured Book Series -->
        <section style="margin-bottom:3.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
            <h2>Popular Pulp Fiction Book Series</h2>
            <a href="/series/" style="font-weight:700; font-size:0.9rem;">All {len(self.engine.series)} Series &rarr;</a>
          </div>
          <div class="directory-grid">
            {"".join([f'''
            <a href="/series/{s["slug"]}/" class="directory-card">
              <h3>📖 {escape_html(s["name"])}</h3>
              <p>{escape_html(s["description"][:130])}...</p>
              <div class="card-footer">
                <span>{s["books_count"]} Books in Series</span>
                <span>View Reading Order &rarr;</span>
              </div>
            </a>
            ''' for s in top_series])}
          </div>
        </section>

        <!-- Featured Collections -->
        <section style="margin-bottom:3.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
            <h2>Curated Reading Lists &amp; Buyer Guides</h2>
            <a href="/collections/" style="font-weight:700; font-size:0.9rem;">All Guides &rarr;</a>
          </div>
          <div class="directory-grid">
            {"".join([f'''
            <a href="/collections/{c["slug"]}/" class="directory-card">
              <h3>⭐ {escape_html(c["title"])}</h3>
              <p>{escape_html(c["description"][:130])}...</p>
              <div class="card-footer">
                <span>{c["books_count"]} Titles</span>
                <span>Read Guide &rarr;</span>
              </div>
            </a>
            ''' for c in top_collections])}
          </div>
        </section>

        <!-- Featured Books Grid -->
        <section style="margin-bottom:3.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
            <h2>Popular Pulp Fiction Ebooks</h2>
            <a href="/books/" style="font-weight:700; font-size:0.9rem;">Browse All {len(self.engine.books)} &rarr;</a>
          </div>
          <div class="product-grid">
            {"".join([render_book_card(b) for b in featured_books])}
          </div>
        </section>

        <!-- Top Authors Section -->
        <section style="margin-bottom:3.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
            <h2>Featured Master Authors</h2>
            <a href="/authors/" style="font-weight:700; font-size:0.9rem;">All Authors &rarr;</a>
          </div>
          <div class="directory-grid">
            {"".join([f'''
            <a href="/authors/{a["slug"]}/" class="directory-card">
              <h3>{escape_html(a["name"])}</h3>
              <p>{escape_html(a["bio"][:140])}...</p>
              <div class="card-footer">
                <span>{a["books_count"]} Ebooks</span>
                <span>Explore Author &rarr;</span>
              </div>
            </a>
            ''' for a in list(self.engine.authors.values())[:4]])}
          </div>
        </section>
        """

        json_ld = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": f"{home_url}#website",
                    "url": home_url,
                    "name": SITE_NAME,
                    "description": DEFAULT_DESCRIPTION,
                    "publisher": {
                        "@type": "Organization",
                        "name": PUBLISHER_NAME,
                        "logo": {"@type": "ImageObject", "url": PUBLISHER_LOGO}
                    },
                    "potentialAction": {
                        "@type": "SearchAction",
                        "target": f"{SITE_URL}/books/?q={{search_term_string}}",
                        "query-input": "required name=search_term_string"
                    }
                },
                {
                    "@type": "Organization",
                    "@id": f"{home_url}#organization",
                    "name": PUBLISHER_NAME,
                    "url": home_url,
                    "logo": PUBLISHER_LOGO
                }
            ]
        }

        html = render_base_html(
            title="Vintage Pulp Fiction Ebooks | Softcover Books",
            meta_desc=DEFAULT_DESCRIPTION,
            canonical_url=home_url,
            json_ld=json_ld,
            content_html=content_html,
            active_target="home",
            engine=self.engine
        )
        self.write_page("index.html", html)

    def build_404_page(self):
        """Generate branded, SEO-friendly 404 error page."""
        print("Generating 404.html...")
        url = f"{SITE_URL}/404.html"
        content_html = f"""
        <section class="hero" style="text-align:center; padding:4rem 1.5rem;">
          <div class="hero-badge">⚠️ 404 - Page Not Found</div>
          <h1>Vintage Pulp Page Not Found</h1>
          <p style="max-width:600px; margin:0 auto 2rem auto;">
            The vintage pulp novel or reading guide you are looking for may have moved, been renamed, or is currently out of catalog. Explore over 300+ classic pulp ebooks below.
          </p>
          <form action="/books/" method="get" class="pseo-search-container" role="search" style="margin:0 auto 2rem auto; max-width:600px;">
            <svg class="pseo-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input type="search" name="q" id="pseo-search" class="pseo-search-input" placeholder="Search 300+ titles, authors, or genres..." autocomplete="off">
          </form>
          <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap; margin-top:1.5rem;">
            <a href="/" class="btn btn-primary" style="display:inline-flex; align-items:center; gap:0.5rem; background:var(--accent-red); color:#fff; padding:0.75rem 1.5rem; border-radius:6px; font-weight:700; text-decoration:none;">🏠 Back to Homepage</a>
            <a href="/books/" class="btn btn-secondary" style="display:inline-flex; align-items:center; gap:0.5rem; background:var(--bg-surface); border:1px solid var(--border-strong); color:var(--text-main); padding:0.75rem 1.5rem; border-radius:6px; font-weight:700; text-decoration:none;">📚 Browse All Books</a>
            <a href="/series/" class="btn btn-secondary" style="display:inline-flex; align-items:center; gap:0.5rem; background:var(--bg-surface); border:1px solid var(--border-strong); color:var(--text-main); padding:0.75rem 1.5rem; border-radius:6px; font-weight:700; text-decoration:none;">📖 Book Series</a>
          </div>
        </section>
        """
        html = render_base_html(
            title="Page Not Found | Softcover Books",
            meta_desc="The requested page could not be found. Search over 300+ classic vintage pulp fiction ebooks on Softcover Books.",
            canonical_url=url,
            json_ld={"@context": "https://schema.org", "@type": "WebPage", "name": "Page Not Found", "url": url},
            content_html=content_html,
            active_target="home",
            engine=self.engine,
            is_404=True
        )
        self.write_page("404.html", html)
        self.write_page("public/404.html", html)

    def build_sitemaps(self):
        """Generate Chunked XML Sitemaps (/sitemap.xml index + sub-sitemaps)."""
        print("Generating Chunked XML Sitemaps...")

        # Sub-sitemaps
        sub_sitemaps = [
            ("sitemap-pages.xml", self.sitemap_urls["pages"]),
            ("sitemap-books.xml", self.sitemap_urls["books"]),
            ("sitemap-series.xml", self.sitemap_urls["series"]),
            ("sitemap-authors.xml", self.sitemap_urls["authors"]),
            ("sitemap-genres.xml", self.sitemap_urls["genres"]),
            ("sitemap-themes.xml", self.sitemap_urls["themes"]),
            ("sitemap-collections.xml", self.sitemap_urls["collections"]),
        ]

        for fname, urls in sub_sitemaps:
            xml_lines = [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            ]
            for u in urls:
                xml_lines.append("  <url>")
                xml_lines.append(f"    <loc>{escape_html(u['loc'])}</loc>")
                xml_lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
                xml_lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
                xml_lines.append(f"    <priority>{u['priority']}</priority>")
                xml_lines.append("  </url>")
            xml_lines.append("</urlset>")
            xml_content = "\n".join(xml_lines)

            # Write to both root and public/
            self.write_page(fname, xml_content)
            self.write_page(f"public/{fname}", xml_content)

        # Sitemap Index
        index_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        for fname, _ in sub_sitemaps:
            index_lines.append("  <sitemap>")
            index_lines.append(f"    <loc>{SITE_URL}/{fname}</loc>")
            index_lines.append(f"    <lastmod>{CURRENT_DATE}</lastmod>")
            index_lines.append("  </sitemap>")
        index_lines.append("</sitemapindex>")
        index_content = "\n".join(index_lines)

        self.write_page("sitemap.xml", index_content)
        self.write_page("public/sitemap.xml", index_content)

    def build_robots_txt(self):
        """Generate search-engine-ready robots.txt."""
        print("Generating robots.txt...")
        robots_content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
        self.write_page("robots.txt", robots_content)
        self.write_page("public/robots.txt", robots_content)

    def build_redirects(self):
        """Generate Cloudflare Pages _redirects file for canonicalization and legacy slugs."""
        print("Generating _redirects...")
        collection_slugs = {c["slug"]: c for c in self.engine.collections}
        redirects = []

        # 1. Author redirects
        redirects.append(("/authors/ap-du-plessis/", "/authors/a-p-du-plessis/"))

        # 2. Legacy book redirects
        legacy_books = [
            ("/books/aasvo-ls-van-die-kalahari/", "/books/aasvoels-van-die-kalahari/"),
            ("/books/aasvo-ls-van-die-see/", "/books/aasvoels-van-die-see/"),
            ("/books/die-p-rel-van-malsia/", "/books/die-perel-van-malsia/"),
            ("/books/droster-in-algeri/", "/books/droster-in-algerie/"),
        ]
        redirects.extend(legacy_books)

        # 3. Legacy theme redirects
        legacy_themes = [
            ("/themes/namib/", "/themes/sahara-desert-peril/"),
            ("/themes/namib-desert-peril/", "/themes/sahara-desert-peril/"),
            ("/themes/kalahari/", "/themes/sahara-vultures/"),
            ("/themes/kalahari-vultures/", "/themes/sahara-vultures/"),
            ("/themes/gold-of-monomotapa/", "/themes/jungle-leopard-companions/"),
            ("/themes/bush-pilots/", "/themes/south-african-westerns/"),
            ("/themes/underworld-syndicates/", "/themes/sahara-western-action/"),
            ("/themes/man-eating-beasts/", "/themes/masked-jungle-adventurer/"),
            ("/themes/aviation/", "/themes/lowveld-westerns/"),
            ("/themes/aviation-action/", "/themes/lowveld-westerns/"),
            ("/themes/ai-rebellion/", "/themes/ai-created-fiction/"),
            ("/themes/cybernetic-intrigue/", "/themes/ai-created-fiction/"),
            ("/themes/high-tech-warfare/", "/themes/ai-created-fiction/"),
            ("/themes/futuristic-dystopia/", "/themes/ai-created-fiction/"),
            ("/themes/cosmic-mystery/", "/themes/ai-created-fiction/"),
            ("/themes/distant-galaxies/", "/themes/ai-created-fiction/"),
            ("/themes/space-opera/", "/themes/ai-created-fiction/"),
        ]
        redirects.extend(legacy_themes)

        # 4. Old static collections
        old_static = [
            ("Best Retro Crime Fiction on Amazon Kindle", "best-retro-crime-fiction-on-amazon"),
            ("Short Pulp Stories under $3", "short-pulp-stories-under-10"),
            ("Short Pulp Stories under $5", "short-pulp-stories-under-10"),
            ("Top 10 Classic Foreign Legion Novels on Kindle", "top-10-classic-foreign-legion-novels"),
            ("Ultimate Pirate Pulp Adventure Ebooks on Kindle", "ultimate-pirate-pulp-adventure-ebooks"),
            ("Vintage African Jungle Adventure Novels on Kindle", "vintage-african-jungle-adventure-novels"),
            ("Top Swashbuckling Rogue & Highwayman Stories on Amazon Kindle", "top-swashbuckling-rogue-highwayman-stories"),
            ("Best 1950s Vintage Mystery Novels for Kindle", "best-1950s-vintage-mystery-novels"),
            ("Top 20 Afrikaans Pulp Fiction Ebooks on Kindle", "top-20-afrikaans-pulp-fiction-ebooks"),
            ("Top 20 English Translated Pulp Fiction Masterpieces on Kindle", "top-20-english-translated-pulp-fiction-masterpieces"),
            ("Vintage Espionage Novels for Fans of Ian Fleming on Amazon Kindle", "vintage-espionage-novels-for-fans-of-ian-fleming"),
            ("Underground Noir Crime Paperbacks on Kindle", "underground-noir-crime-paperbacks"),
        ]
        for old_t, target_slug in old_static:
            old_slug = slugify(old_t)
            if target_slug in collection_slugs:
                redirects.append((f"/collections/{old_slug}/", f"/collections/{target_slug}/"))

        # 5. Programmatic historical variations
        old_intents_patterns = [
            ("Best {} Ebooks on Amazon Kindle", "best-{}-ebooks-on-amazon"),
            ("Must-Read {} Thrillers for Kindle", "must-read-{}-thrillers"),
            ("Ultimate Guide to {} Novels on Kindle", "ultimate-guide-to-{}-novels"),
            ("Ultimate Guide to {} Novels", "ultimate-guide-to-{}-novels"),
            ("Essential {} Vintage Paperbacks on Amazon Kindle", "essential-{}-vintage-paperbacks"),
            ("Essential {} Vintage Paperbacks", "essential-{}-vintage-paperbacks"),
            ("Cheap {} Ebooks Under $5 on Amazon", "cheap-{}-ebooks-under-10-on-amazon"),
            ("Cheap {} Ebooks Under $3 on Amazon", "cheap-{}-ebooks-under-10-on-amazon"),
            ("Action-Packed {} Stories for Fast Reading", "action-packed-{}-stories-for-fast-reading"),
            ("Classic {} Ebooks with Badass Protagonists", "classic-{}-ebooks-with-badass-protagonists"),
            ("Top Ranked {} Books for Pulp Fiction Fans", "top-ranked-{}-books-for-pulp-fiction-fans"),
            ("Best {} Novels for Vacation Reading", "best-{}-novels-for-vacation-reading"),
            ("Top 10 {} Novels on Kindle", "top-10-{}-pulp-fiction-classics"),
            ("Top 10 {} Pulp Fiction Classics on Kindle", "top-10-{}-pulp-fiction-classics"),
            ("Top 10 {} Pulp Fiction Classics", "top-10-{}-pulp-fiction-classics"),
        ]

        old_topics = [
            "French Foreign Legion", "Sahara Military Survival", "High Seas Pirate Action", "Swashbuckling Buccaneer",
            "Hardboiled Private Detective", "1950s Undercover Crime", "Cape Frontier Vigilante", "African Jungle Lost World",
            "Wilderness Bushveld Safari", "Retro Sci-Fi Space Opera", "Francois Alwyn Venter Adventure", "Gerrie Radlof Swashbuckler",
            "Braam le Roux Jungle Hero", "Sandbergh Beyers Military", "A.P. du Plessis Noir Detective", "Die Buiter Masked Robber",
            "Oloff the Pirate High Seas", "The Black Leopard African", "Wanderer Detective Sleuth", "SA Police Hardboiled Crime",
            "Red Ruby Maritime Adventure", "Jungle Hawk Bush Pilot", "Jungle Hawk Frontier Western", "Untamed Lowveld Safari Mystery",
            "Ryk Schoonraad Private Eye", "Afrikaans Vintage Ebooks", "English Translated Pulp Classics", "Desert Outpost Sieges",
            "Galleon Cannon Battles", "Midnight Sword Duels", "Underworld Smuggling Rings", "Diamond Syndicate Thrillers",
            "Lost Civilizations in Africa", "Revolver Shootout Action", "Vintage Pulp Box Sets", "Classic Dime Novel Ebooks",
            "Fast Paced Pulp Mysteries", "Treasure Hunting Pulp Stories", "Escape & Evasion Military Thrillers", "Escape Evasion Military Thrillers",
            "Men's Adventure Vintage Paperbacks", "Pulp Fiction Novellas for Kindle", "Pulp Fiction Novellas", "Cold War Spy Thrillers",
            "Vintage Crime Paperbacks", "Desert Caravan Romances", "High Seas Mutiny Novels", "Feral Hero Jungle Sagas",
            "Cape Colony Historical Swashbucklers", "Man Eating Beast Thrillers", "Bushveld Diamond Caches", "Retro AI and Cyber Thrillers",
            "Pulp Fiction Masterpieces on Kindle", "Pulp Fiction Masterpieces", "Skeleton Coast Survival Novels", "Kalahari Desert Espionage",
            "Daring Prison Break Pulp Stories", "Classic Highwayman Romances", "Bounty Hunter Drifter Pulp", "Ancient Relic Quest Ebooks",
            "Undercover Police Infiltration", "Vintage Maritime Ghost Ship Tales", "Radio Drama Style Cliffhangers", "Golden Age Paperback Thrillers"
        ]

        topic_mapping = {
            "Retro Sci-Fi Space Opera": "ai-stories",
            "Retro AI and Cyber Thrillers": "ai-stories",
            "Man Eating Beast Thrillers": "masked-jungle-adventurer",
            "Kalahari Desert Espionage": "sahara-vultures",
            "Pulp Fiction Novellas for Kindle": "pulp-fiction-novellas",
            "Pulp Fiction Masterpieces on Kindle": "pulp-fiction-masterpieces",
            "Jungle Hawk Bush Pilot": "jungle-hawk-frontier-western",
            "Escape Evasion Military Thrillers": "escape-evasion-military-thrillers",
        }

        for top in old_topics:
            for old_pat, target_pat in old_intents_patterns:
                old_title = old_pat.format(top)
                old_slug = slugify(old_title)
                
                mapped_topic = topic_mapping.get(top, top)
                if mapped_topic in ["ai-stories", "masked-jungle-adventurer", "sahara-vultures"]:
                    target_slug = slugify(target_pat.format("Pulp Fiction Masterpieces"))
                else:
                    target_slug = slugify(target_pat.format(mapped_topic))
                    
                if old_slug != target_slug:
                    if target_slug in collection_slugs:
                        redirects.append((f"/collections/{old_slug}/", f"/collections/{target_slug}/"))
                    elif old_slug in collection_slugs:
                        pass
                    else:
                        clean_target = old_slug.replace("-for-kindle", "").replace("-on-amazon-kindle", "-on-amazon").replace("-on-kindle", "").replace("-under-5-on-amazon", "-under-10-on-amazon")
                        if clean_target in collection_slugs:
                            redirects.append((f"/collections/{old_slug}/", f"/collections/{clean_target}/"))

        # Explicit overrides for remaining sci-fi collections
        redirects.append(("/collections/action-packed-retro-sci-fi-space-opera-stories-for-fast-reading/", "/collections/action-packed-pulp-fiction-masterpieces-stories-for-fast-reading/"))
        redirects.append(("/collections/ultimate-guide-to-retro-sci-fi-space-opera-novels/", "/collections/ultimate-guide-to-pulp-fiction-masterpieces-novels/"))
        redirects.append(("/collections/best-retro-sci-fi-space-opera-novels-for-vacation-reading/", "/collections/best-pulp-fiction-masterpieces-novels-for-vacation-reading/"))
        redirects.append(("/collections/best-retro-ai-and-cyber-thrillers-ebooks-on-amazon-kindle/", "/collections/best-pulp-fiction-masterpieces-ebooks-on-amazon/"))

        # Deduplicate and format rules
        seen_sources = set()
        redirect_rules = [
            "# Cloudflare Pages Redirect Rules",
            "# 301 Permanent Redirects for legacy routes, collections, themes, and authors"
        ]
        for src, dst in redirects:
            if src not in seen_sources and src != dst:
                seen_sources.add(src)
                redirect_rules.append(f"{src} {dst} 301")

        redirect_content = "\n".join(redirect_rules) + "\n"
        self.write_page("_redirects", redirect_content)
        self.write_page("public/_redirects", redirect_content)

if __name__ == "__main__":
    website_dir = os.path.dirname(os.path.abspath(__file__))
    engine = PulpDataEngine(website_dir)
    builder = PSEOBuilder(engine, website_dir)
    builder.build_all()
