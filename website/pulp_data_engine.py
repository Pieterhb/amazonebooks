"""
Pulp Fiction Data Engine
Extracts, enriches, and structures 300+ book catalog items, authors, genres, themes, and curated collections for Programmatic SEO.
"""

import os
import re
import json
import urllib.parse
from bs4 import BeautifulSoup

from site_config import SITE_URL, AMAZON_AFFILIATE_TAG, SITE_NAME

def slugify(text):
    """Generate a clean URL slug from string."""
    text = re.sub(r'[\'\"’]', '', str(text).lower())
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def clean_amazon_url(url, affiliate_tag=AMAZON_AFFILIATE_TAG):
    """Normalize Amazon URL and inject affiliate tag."""
    if not url:
        return ""
    url = url.strip()
    if 'amazon.com' in url:
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        if affiliate_tag:
            params['tag'] = [affiliate_tag]
        new_query = urllib.parse.urlencode(params, doseq=True)
        clean_url = urllib.parse.urlunparse((
            parsed.scheme or 'https',
            parsed.netloc or 'www.amazon.com',
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        return clean_url
    return url

class PulpDataEngine:
    def __init__(self, base_dir=None):
        if not base_dir:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = base_dir
        self.root_dir = os.path.abspath(os.path.join(base_dir, ".."))
        self.books = []
        self.authors = {}
        self.genres = {}
        self.themes = {}
        self.collections = []
        self.series = {}
        self.load_data()

    def load_data(self):
        """Load books from catalog_source.html or catalog.json and synthesize rich metadata."""
        catalog_html_path = os.path.join(self.base_dir, "catalog_source.html")
        if not os.path.exists(catalog_html_path):
            catalog_html_path = os.path.join(self.root_dir, "website", "catalog_source.html")

        if not os.path.exists(catalog_html_path):
            catalog_html_path = os.path.join(self.base_dir, "index.html")

        with open(catalog_html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        raw_books = []
        for card in soup.find_all("article", class_="book-card"):
            img_tag = card.find("img")
            img = img_tag.get("src") if img_tag else ""
            title = card.find("h3").text.strip() if card.find("h3") else ""
            author = card.find("p", class_="author").text.strip().replace("By ", "") if card.find("p", class_="author") else ""
            badge = card.find("span", class_="store-badge")
            lang = badge.text.strip() if badge else "English"
            btn = card.find("a", class_="btn")
            link = btn.get("href") if btn else ""
            num_tag = card.find("span", class_="book-number")
            num = num_tag.text.strip() if num_tag else ""
            section = card.find_parent("section")
            sec_id = section.get("id") if section else ""
            sec_name = section.find("h2").text.strip() if section and section.find("h2") else ""

            raw_books.append({
                "title": title,
                "author": author if author else "Pieter Haasbroek",
                "img": img,
                "lang": lang,
                "link": link,
                "num": num,
                "series": sec_name,
                "section_id": sec_id
            })

        # Enrich and normalize books
        used_slugs = set()
        for idx, b in enumerate(raw_books):
            raw_title = b["title"]
            author = b["author"]
            title_display = raw_title.strip()
            if title_display.isupper():
                title_display = title_display.title()

            if author == "Box Set - 3 Ebooks":
                author = "Francois Alwyn Venter" if "sahara" in b["series"].lower() else "Gerrie Radlof"

            base_slug = slugify(title_display)
            if not base_slug:
                base_slug = f"book-{idx+1}"
            slug = base_slug
            counter = 2
            while slug in used_slugs:
                slug = f"{base_slug}-{slugify(b['lang'])}-{counter}"
                counter += 1
            used_slugs.add(slug)

            clean_link = clean_amazon_url(b["link"])

            # Store and retailer detection
            link_lower = (clean_link or "").lower()
            if "kobo.com" in link_lower:
                store_key = "kobo"
                store_name = "Kobo"
                store_full = "Rakuten Kobo"
                card_btn_label = "Buy on Kobo"
                detail_btn_label = "Buy on Kobo"
                format_label = "Digital Ebook"
                delivery_label = "Instant Digital Delivery"
                devices_label = "eReader, iOS, Android, or PC"
                reviews_label = "Reviews on Kobo"
                seller_name = "Rakuten Kobo"
            elif "play.google.com" in link_lower:
                store_key = "google_play"
                store_name = "Google Play"
                store_full = "Google Play Books"
                card_btn_label = "Buy on Google Play"
                detail_btn_label = "Buy on Google Play"
                format_label = "Digital Ebook"
                delivery_label = "Instant Digital Delivery"
                devices_label = "Google Play Books, iOS, Android, or PC"
                reviews_label = "Reviews on Google Play"
                seller_name = "Google Play"
            elif "sqrindle.com" in link_lower:
                store_key = "sqrindle"
                store_name = "Sqrindle"
                store_full = "Sqrindle"
                card_btn_label = "Buy on Sqrindle"
                detail_btn_label = "Buy on Sqrindle"
                format_label = "Digital Ebook"
                delivery_label = "Instant Digital Delivery"
                devices_label = "eReader, Tablet, Phone, or PC"
                reviews_label = "Reviews on Sqrindle"
                seller_name = "Sqrindle"
            else:
                store_key = "amazon"
                store_name = "Amazon"
                store_full = "Amazon"
                card_btn_label = "Buy on Amazon"
                detail_btn_label = "Buy on Amazon"
                format_label = "Digital Ebook"
                delivery_label = "Instant Digital Delivery"
                devices_label = "eReader, Tablet, Phone, or PC"
                reviews_label = "Reviews on Amazon"
                seller_name = "Amazon"

            primary_genre, subgenres, themes = self.classify_book(title_display, b["series"], author, b["lang"])
            synopsis = self.generate_synopsis(title_display, author, b["series"], primary_genre, b["lang"], b["num"], store_key=store_key)

            read_time = "4 – 8 hours" if ("omnibus" in title_display.lower() or "box set" in title_display.lower()) else "1 – 4 hours"

            book_obj = {
                "id": idx + 1,
                "slug": slug,
                "title": title_display,
                "author": author,
                "author_slug": slugify(author),
                "series": b["series"],
                "series_slug": slugify(b["series"]),
                "series_number": b["num"],
                "img": b["img"],
                "lang": b["lang"],
                "amazon_url": clean_link,
                "store_key": store_key,
                "store_name": store_name,
                "store_full": store_full,
                "card_btn_label": card_btn_label,
                "detail_btn_label": detail_btn_label,
                "format": format_label,
                "delivery": delivery_label,
                "devices": devices_label,
                "reviews_label": reviews_label,
                "seller": seller_name,
                "primary_genre": primary_genre,
                "primary_genre_slug": slugify(primary_genre),
                "subgenres": subgenres,
                "subgenre_slugs": [slugify(sg) for sg in subgenres],
                "themes": themes,
                "theme_slugs": [slugify(th) for th in themes],
                "synopsis": synopsis,
                "read_time": read_time,
            }
            self.books.append(book_obj)

        self.build_authors()
        self.build_genres()
        self.build_themes()
        self.build_collections()
        self.build_series()

    def classify_book(self, title, series, author, lang):
        """Classify book into genres, subgenres, and theme tags."""
        title_lower = title.lower()
        series_lower = series.lower()

        # 1. Match by series explicitly first
        if any(w in series_lower for w in ["swart luiperd", "black leopard"]):
            primary_genre = "Jungle Adventure & Lost Worlds"
            subgenres = ["African Wilderness Pulp", "Lost Civilizations", "Feral Hero Action", "Safari Mystery"]
            themes = ["Jungle Lost Cities", "Tribal Mysteries", "Man-Eating Beasts", "Wilderness Survival", "Ancient Curses", "Uncharted Africa", "Prowling Predators"]

        elif any(w in series_lower for w in ["sahara", "aventure sahara", "abenteuer", "dini salam", "legion"]):
            primary_genre = "Desert Adventure & Foreign Legion"
            subgenres = ["Military Pulp", "French Foreign Legion", "Survival Action", "Historical Adventure"]
            themes = ["French Foreign Legion", "Desert Caravans", "Sahara Sandstorms", "Foreign Legion Garrisons", "Desert Fort Sieges", "Vengeance & Honor", "Guerrilla Warfare"]

        elif any(w in series_lower for w in ["seerower", "pirate", "maagd van die see", "red ruby"]):
            primary_genre = "Pirate & High Seas Swashbuckler"
            subgenres = ["High Seas Adventure", "Naval Fiction", "Swashbuckler", "Historical Action"]
            themes = ["Pirate Galleons", "Hidden Treasure", "Naval Broadsides", "Sword Duels", "Ghost Ships & Maritime Legends", "Daring Escapes", "Mutiny at Sea"]

        elif any(w in series_lower for w in ["buiter", "masked robber"]):
            primary_genre = "Masked Rogue & Highwayman"
            subgenres = ["Vigilante Pulp", "Cape Frontier Action", "Historical Romance & Intrigue", "Rebellion Thriller"]
            themes = ["Masked Highwaymen", "Cape Frontier History", "Vigilante Justice", "Sword Duels", "Midnight Rides", "Outlaw Rebellion", "Colonial Intrigue"]

        elif any(w in series_lower for w in ["polisie", "police", "speurder", "detective", "schoonraad", "tamar"]):
            primary_genre = "Hardboiled Detective & Noir Crime"
            subgenres = ["1950s Crime Fiction", "Undercover Thriller", "Police Procedural", "Mystery Suspense"]
            themes = ["Private Eye", "1950s Crime", "Undercover Cops", "Wandering Detectives", "Smuggling Rings", "Revolver Shootouts", "Cold War Espionage"]

        elif any(w in series_lower for w in ["woeste laeveld", "untamed lowveld", "oerwoudvalk", "jungle hawk"]):
            primary_genre = "Safari & Bushveld Adventure"
            subgenres = ["Bushveld Thriller", "Aviation Pulp", "Wilderness Danger", "African Expedition"]
            themes = ["Safari Expeditions", "Bushveld Mystery", "Aviation Action", "Man-Eating Beasts", "Diamonds & Ivory", "Remote Outposts", "Untamed Lowveld"]

        elif any(w in series_lower for w in ["ai stories", "artificial intelligence"]) or any(w in title_lower for w in ["saloon fights", "romantic short stories", "scary western"]):
            primary_genre = "Western, Romance & Pulp Anthologies"
            if "saloon" in title_lower or "western cowboy" in title_lower:
                subgenres = ["Western Short Stories", "Cowboy Action", "Short Story Anthologies"]
                themes = ["Saloon Shootouts", "Wild West Outlaws", "Cowboy Legends", "Short Story Collections", "AI Created Fiction"]
            elif "romantic" in title_lower:
                subgenres = ["Romantic Short Stories", "Pulp Romance", "Short Story Anthologies"]
                themes = ["Passionate Encounters", "Romantic Drama", "Vintage Romance", "Short Story Collections", "AI Created Fiction"]
            elif "scary" in title_lower or "horror" in title_lower:
                subgenres = ["Western Short Stories", "Scary Western & Horror Thrillers", "Short Story Anthologies"]
                themes = ["Haunted Frontiers", "Ghost Towns", "Supernatural Thrillers", "Short Story Collections", "AI Created Fiction"]
            else:
                subgenres = ["Western Short Stories", "Romantic Short Stories", "Scary Western & Horror Thrillers", "Short Story Anthologies"]
                themes = ["Short Story Collections", "AI Created Fiction", "Wild West Outlaws", "Vintage Romance"]

        # 2. For standalone / other series, fallback to title keywords
        elif any(w in title_lower for w in ["sahara", "legion"]):
            primary_genre = "Desert Adventure & Foreign Legion"
            subgenres = ["Military Pulp", "French Foreign Legion", "Survival Action", "Historical Adventure"]
            themes = ["French Foreign Legion", "Desert Caravans", "Sahara Sandstorms", "Foreign Legion Garrisons", "Desert Fort Sieges", "Vengeance & Honor", "Guerrilla Warfare"]

        elif any(w in title_lower for w in ["seerower", "pirate", "maagd van die see", "red ruby", "seewraak", "vloot"]):
            primary_genre = "Pirate & High Seas Swashbuckler"
            subgenres = ["High Seas Adventure", "Naval Fiction", "Swashbuckler", "Historical Action"]
            themes = ["Pirate Galleons", "Hidden Treasure", "Naval Broadsides", "Sword Duels", "Ghost Ships & Maritime Legends", "Daring Escapes", "Mutiny at Sea"]

        elif any(w in title_lower for w in ["buiter", "masked robber"]):
            primary_genre = "Masked Rogue & Highwayman"
            subgenres = ["Vigilante Pulp", "Cape Frontier Action", "Historical Romance & Intrigue", "Rebellion Thriller"]
            themes = ["Masked Highwaymen", "Cape Frontier History", "Vigilante Justice", "Sword Duels", "Midnight Rides", "Outlaw Rebellion", "Colonial Intrigue"]

        elif any(w in title_lower for w in ["swart luiperd", "black leopard"]):
            primary_genre = "Jungle Adventure & Lost Worlds"
            subgenres = ["African Wilderness Pulp", "Lost Civilizations", "Feral Hero Action", "Safari Mystery"]
            themes = ["Jungle Lost Cities", "Tribal Mysteries", "Man-Eating Beasts", "Wilderness Survival", "Ancient Curses", "Uncharted Africa", "Prowling Predators"]

        elif any(w in title_lower for w in ["polisie", "police", "speurder", "detective", "schoonraad", "tamar"]):
            primary_genre = "Hardboiled Detective & Noir Crime"
            subgenres = ["1950s Crime Fiction", "Undercover Thriller", "Police Procedural", "Mystery Suspense"]
            themes = ["Private Eye", "1950s Crime", "Undercover Cops", "Wandering Detectives", "Smuggling Rings", "Revolver Shootouts", "Cold War Espionage"]

        elif any(w in title_lower for w in ["woeste laeveld", "untamed lowveld", "oerwoudvalk", "jungle hawk"]):
            primary_genre = "Safari & Bushveld Adventure"
            subgenres = ["Bushveld Thriller", "Aviation Pulp", "Wilderness Danger", "African Expedition"]
            themes = ["Safari Expeditions", "Bushveld Mystery", "Aviation Action", "Man-Eating Beasts", "Diamonds & Ivory", "Remote Outposts", "Untamed Lowveld"]

        else:
            primary_genre = "Vintage Pulp Thriller & Suspense"
            subgenres = ["Classic Pulp", "Action Thriller", "Men's Adventure", "Vintage Suspense"]
            themes = ["Vintage Paperbacks", "Dime Novel Thrills", "Radio Serial Style", "Fast-Paced Action", "High Stakes Heists", "Daring Escapes"]

        if "afrikaans" in lang.lower():
            themes.append("Afrikaans Pulp Classics")
        elif "english" in lang.lower():
            themes.append("English Translated Classics")

        return primary_genre, subgenres, list(dict.fromkeys(themes))

    def generate_synopsis(self, title, author, series, genre, lang, num, store_key="amazon"):
        """Generate high-engagement, immersive pulp fiction synopsis."""
        lang_note = f"Translated into thrilling {lang}" if lang != "Afrikaans" else "Written in authentic, gripping Afrikaans"
        series_info = f"Part of the legendary {series}" if series and series != "Other" else "A gripping standalone pulp fiction masterpiece"
        if num and num != "999":
            series_info += f" (Book #{num})"

        if store_key == "kobo":
            store_cta = "on Kobo"
            device_cta = "available instantly for your Kobo eReader or reading app."
        elif store_key == "google_play":
            store_cta = "on Google Play"
            device_cta = "available instantly on Google Play Books."
        elif store_key == "sqrindle":
            store_cta = "on Sqrindle"
            device_cta = "available instantly in digital ebook format."
        else:
            store_cta = "on Amazon"
            device_cta = "available instantly in digital ebook format."

        if genre == "Desert Adventure & Foreign Legion":
            desc = (
                f"**{title}** by {author} plunges readers into the scorching heat, blood-soaked sands, and razor-sharp tensions of the North African desert. {series_info}. "
                f"Against an unforgiving landscape of treacherous dunes, fierce desert tribes, and beleaguered French Foreign Legion garrisons, every chapter delivers unrelenting action and pulse-pounding survival. "
                f"When honor clashes with betrayal under the blistering Sahara sun, only the bravest can hope to make it out alive. {lang_note} for classic pulp adventure enthusiasts seeking high-octane vintage military thrills {store_cta}."
            )
        elif genre == "Pirate & High Seas Swashbuckler":
            desc = (
                f"**{title}** by {author} is a swashbuckling high-seas epic packed with cannon smoke, flashing cutlasses, and dangerous oceanic intrigues. {series_info}. "
                f"Set during the golden age of buccaneers and maritime warfare, the story follows daring captains navigating pirate-infested archipelagos, treacherous admirals, and hidden treasure troves. "
                f"Every page crackles with broadside battles, mutinous crews, and desperate sword duels across blood-slicked decks. {lang_note}, this vintage nautical adventure is a must-read {store_cta}."
            )
        elif genre == "Masked Rogue & Highwayman":
            desc = (
                f"**{title}** by {author} brings to life the timeless legend of a fearless Cape highwayman who strikes from the shadows to champion justice against ruthless tyrants. {series_info}. "
                f"Galloping through moonlit mountain passes, eluding colonial dragoons, and orchestrating daring rescues, the protagonist embodies the romantic spirit of the classic rogue hero. "
                f"Packed with aristocratic deception, midnight shootouts, and thrilling escapes, this historical action romance delivers non-stop entertainment {store_cta}."
            )
        elif genre == "Jungle Adventure & Lost Worlds":
            desc = (
                f"**{title}** by {author} delivers an adrenaline-fueled safari through deepest, darkest Africa where primeval dangers lurk behind every dense thicket. {series_info}. "
                f"From encounters with lethal apex predators to ancient, forbidden ruins guarded by ferocious warriors, this iconic lost-world adventure captures the feral intensity of classic pulp heroics. "
                f"Immerse yourself in legendary African wilderness pulp fiction, {device_cta}"
            )
        elif genre == "Hardboiled Detective & Noir Crime":
            desc = (
                f"**{title}** by {author} is a gritty, fast-moving 1950s crime noir novel steeped in cigarette smoke, rain-soaked asphalt, and deadly underworld conspiracies. {series_info}. "
                f"When a routine investigation unravels into a web of double-crosses, ruthless smugglers, and trigger-happy syndicate bosses, our hardnosed investigator must rely on sharp instincts and a loaded .38 revolver to survive. "
                f"A thrilling slice of mid-century vintage detective pulp, perfect for fans of classic noir {store_cta}."
            )
        elif genre == "Safari & Bushveld Adventure":
            desc = (
                f"**{title}** by {author} transports readers to the wild, untamed frontiers of the African bushveld. {series_info}. "
                f"Here, bush pilots, rugged game trackers, and dangerous poachers clash over hidden diamond caches and territorial rivalries. "
                f"With vivid descriptions of the untamed wilderness and relentless pacing, this classic bushveld adventure keeps you on the edge of your seat from opening page to explosive climax {store_cta}."
            )
        elif genre == "Western, Romance & Pulp Anthologies":
            desc = (
                f"**{title}** by {author} is an action-packed pulp fiction short story collection delivering fast-paced entertainment, unforgettable character dynamics, and sharp narrative twists. {series_info}. "
                f"Written in the thrilling tradition of vintage American and mid-century pulp paperbacks, every story offers instant excitement and vibrant storytelling. Available {store_cta}."
            )
        else:
            desc = (
                f"**{title}** by {author} is a classic vintage pulp fiction novel packed with suspense, unforgettable characters, and high-velocity pacing. {series_info}. "
                f"Written in the golden tradition of dime novels and mid-century paperback thrillers, each chapter is crafted to keep readers captivated. Available worldwide {store_cta}."
            )
        return desc

    def build_authors(self):
        """Build structured author profiles with bios, stats, and bibliographies."""
        author_bios = {
            "Francois Alwyn Venter": (
                "Francois Alwyn Venter (1916–1997), widely known as F.A. Venter, was one of South Africa's most acclaimed and prolific literary giants. "
                "Master of the iconic Sahara Adventure Series, Venter crafted legendary French Foreign Legion desert warfare and military survival sagas that captivated generations of pulp fiction readers worldwide. "
                "His stories combine meticulous historical authenticity, high-octane combat action, and deeply compelling heroics under the blistering Sahara sun."
            ),
            "Gerrie Radlof": (
                "Gerrie Radlof (pseudonym of Gerrit van Zyl) is a legendary titan of vintage pulp fiction. "
                "Creator of iconic swashbucklers including 'Die Buiter' (The Masked Robber), the epic high-seas naval saga 'Oloff die Seerower' (Oloff the Pirate), 'Maagd van die See' (Red Ruby), and the gritty 1950s crime series 'SA Polisie' and 'Swerwer Speurder', "
                "Radlof authored over 100 fast-paced paperback originals defined by sword duels, midnight escapes, and relentless suspense."
            ),
            "Braam le Roux": (
                "Braam le Roux was the premier visionary of African jungle adventure pulp, immortalized by his celebrated 'Die Swart Luiperd' (The Black Leopard) saga and 'Oerwoudvalk' (Jungle Hawk). "
                "Le Roux's stories transported millions of readers into mysterious uncharted territories, lost civilizations, and fierce encounters with apex predators, echoing the legendary pulp spirit of Edgar Rice Burroughs."
            ),
            "Sandbergh Beyers": (
                "Sandbergh Beyers is celebrated for his gripping military and desert survival novels in the 'Sahara Reeks'. "
                "His storytelling specializes in high-tension outpost defenses, harsh desert recon missions, and the unbreakable brotherhood of Foreign Legionnaires under fire."
            ),
            "A.P. du Plessis": (
                "A.P. du Plessis is renowned for his mid-century private detective and espionage pulp series, most notably the 'Ryk Schoonraad' and 'Tamar' detective novels. "
                "His gritty, noir-tinged investigations feature Cold War intrigue, hidden syndicates, and sharp deduction."
            ),
            "Pieter Haasbroek": (
                "Pieter Haasbroek is an author and curator dedicated to preserving and expanding the golden legacy of vintage pulp fiction. "
                "His stories span suspense, desert survival, retro adventure, and modern pulp revivals available across multiple digital editions."
            ),
            "Chris Opperman": "Author of intense vintage crime thrillers, bushveld suspense, and high-stakes adventure fiction.",
            "Johan Nel": "Pulp novelist known for fast-paced mystery, frontier exploration, and classic paperback action.",
            "Christo Juan Malan": "Storyteller specializing in thrilling regional mysteries, suspenseful character dramas, and vintage adventure.",
            "Artificial Intelligence": "Curated experimental retro pulp short stories generated using cutting-edge AI neural storytelling engines, reimagining classic western, romance, and thriller pulp genres for modern readers."
        }

        author_map = {}
        for b in self.books:
            a_name = b["author"]
            if a_name not in author_map:
                author_map[a_name] = []
            author_map[a_name].append(b)

        for name, b_list in author_map.items():
            slug = slugify(name)
            bio = author_bios.get(name, f"Celebrated pulp fiction author featuring {len(b_list)} thrilling vintage ebook titles.")
            genres_set = list(dict.fromkeys(b["primary_genre"] for b in b_list))

            self.authors[slug] = {
                "name": name,
                "slug": slug,
                "bio": bio,
                "books_count": len(b_list),
                "books": b_list,
                "primary_genres": genres_set,
                "sample_covers": [b["img"] for b in b_list[:6]]
            }

    def build_genres(self):
        """Build Genre and Subgenre taxonomy with detailed editorial guides."""
        genre_descriptions = {
            "Desert Adventure & Foreign Legion": {
                "title": "Desert Adventure & French Foreign Legion Pulp Fiction",
                "tagline": "Blistering Dunes, Outpost Defenses, and High-Stakes Military Survival",
                "guide": (
                    "Step into the scorching sands of North Africa with our extensive collection of classic French Foreign Legion and desert adventure pulp novels. "
                    "From F.A. Venter's iconic Sahara Adventure Series to Sandbergh Beyers' high-tension military survival tales, these books deliver non-stop combat, fortress sieges, and desert reconnaissance. "
                    "Featuring legendary battles against ruthless raiders, perilous sandstorms, and deep bonds of military brotherhood, this genre is the cornerstone of mid-century adventure pulp."
                ),
                "tropes": ["Foreign Legion Garrisons", "Desert Sandstorms", "Oasis Ambushes", "Honor & Vengeance", "Cavalry Charges", "Desert Treachery"]
            },
            "Pirate & High Seas Swashbuckler": {
                "title": "Pirate & High Seas Swashbuckling Pulp Ebooks",
                "tagline": "Cannon Broadsides, Hidden Pirate Coves, and Daring Sword Duels",
                "guide": (
                    "Set sail across stormy oceans and pirate-infested straits in our collection of classic high-seas swashbuckling ebooks. "
                    "Featuring Gerrie Radlof's legendary 'Oloff die Seerower' (Oloff the Pirate) and 'Maagd van die See' (Red Ruby) sagas, these stories capture the ferocious glory of naval combat, hidden gold islands, and cutlass-wielding buccaneers. "
                    "Experience unforgettable maritime adventures full of naval broadsides, mutinous plots, and heroic escapes."
                ),
                "tropes": ["Pirate Galleons", "Broadside Cannon Duels", "Hidden Treasure", "Cutlass Swordplay", "Mutinous Crews", "Ghost Ships"]
            },
            "Masked Rogue & Highwayman": {
                "title": "Masked Rogue & Cape Highwayman Pulp Fiction",
                "tagline": "Galloping Midnight Rides, Vigilante Justice, and Swashbuckling Heroics",
                "guide": (
                    "Discover the swashbuckling adventures of 'Die Buiter' (The Masked Robber) and other Cape frontier vigilante classics. "
                    "Striking fear into corrupt magistrates and greedy colonial tyrants, the masked hero fights for the oppressed across rugged mountain passes and candlelit manors. "
                    "Blending romantic intrigue, brilliant sword duels, and midnight ambushes, these timeless tales represent the pinnacle of swashbuckling historical pulp."
                ),
                "tropes": ["Masked Vigilantes", "Midnight Horse Rides", "Swordplay & Dueling", "Outlaw Justice", "Colonial Tyranny", "Romantic Intrigue"]
            },
            "Jungle Adventure & Lost Worlds": {
                "title": "Jungle Adventure & Lost Worlds Pulp Novels",
                "tagline": "Uncharted Territories, Ancient Civilizations, and Untamed Beasts",
                "guide": (
                    "Journey into deep, uncharted African jungles where forgotten civilizations and man-eating predators reign. "
                    "Braam le Roux's immortal 'Die Swart Luiperd' (The Black Leopard) series leads readers through treacherous swamps, ancient cursed ruins, and heart-pounding battles against rogue beasts and ruthless adversaries. "
                    "Experience the raw, feral excitement of classic mid-century African jungle pulp."
                ),
                "tropes": ["Feral Jungle Heroes", "Lost Civilizations", "Man-Eating Predators", "Tribal Feuds", "Ancient Curses", "Untamed Wilderness"]
            },
            "Hardboiled Detective & Noir Crime": {
                "title": "Hardboiled Detective & 1950s Crime Noir Pulp Ebooks",
                "tagline": "Gritty Sleuths, Smoke-Filled Alleys, and Underworld Conspiracies",
                "guide": (
                    "Dive into the shadowy underworld of 1950s crime, private investigators, and undercover police squads. "
                    "Featuring Gerrie Radlof's 'SA Polisie' and 'Swerwer Speurder' (The Wanderer Detective), alongside A.P. du Plessis' 'Ryk Schoonraad' series, these gripping stories deliver fast-paced shootouts, cunning smugglers, and relentless sleuthing. "
                    "Perfect for fans of classic Mickey Spillane, Raymond Chandler, and vintage hardboiled paperback noir."
                ),
                "tropes": ["Private Investigators", "1950s Noir Crime", "Undercover Police", "Revolver Shootouts", "Smuggling Syndicates", "Femmes Fatales"]
            },
            "Safari & Bushveld Adventure": {
                "title": "Safari & Bushveld Mystery Pulp Fiction",
                "tagline": "Wilderness Expeditions, Bush Pilots, and Frontier Danger",
                "guide": (
                    "Explore the untamed African bushveld with our collection of safari mysteries and frontier adventure novels. "
                    "Featuring 'Untamed Lowveld' and 'Jungle Hawk' aviation tales, these novels pit brave hunters and bush pilots against wildlife perils, illegal diamond syndicates, and hostile terrain. "
                    "Experience authentic, fast-paced frontier suspense."
                ),
                "tropes": ["Bush Pilots", "Diamond Smugglers", "Safari Expeditions", "Apex Predators", "Bushveld Intrigue", "Remote Outposts"]
            },
            "Western, Romance & Pulp Anthologies": {
                "title": "Western, Romance & Pulp Anthology Ebooks",
                "tagline": "Wild West Shootouts, Passionate Romances, and Spine-Chilling Frontier Tales",
                "guide": (
                    "Explore our eclectic collection of vintage-style short story anthologies. "
                    "From high-noon cowboy showdowns in lawless frontier saloons to steamy mid-century romantic intrigues and eerie supernatural western thrillers, these fast-paced short stories deliver instant, immersive excitement."
                ),
                "tropes": ["Saloon Shootouts", "Wild West Outlaws", "Steamy Romance", "Supernatural Horror", "Short Story Anthologies", "Frontier Justice"]
            },
            "Vintage Pulp Thriller & Suspense": {
                "title": "Vintage Pulp Thrillers & Classic Suspense Ebooks",
                "tagline": "Relentless Pacing, Dime-Novel Thrills, and Unforgettable Cliffhangers",
                "guide": (
                    "Experience the raw energy of mid-century dime novels and paperback originals. "
                    "Filled with sharp plot twists, daring escapes, and high-velocity action, our curated vintage pulp thrillers deliver pure, unadulterated reading pleasure."
                ),
                "tropes": ["Dime Novel Style", "Fast Pacing", "High Stakes", "Cliffhangers", "Heroic Action"]
            }
        }

        for g_name, meta in genre_descriptions.items():
            slug = slugify(g_name)
            matching_books = [b for b in self.books if b["primary_genre"] == g_name]
            self.genres[slug] = {
                "name": g_name,
                "slug": slug,
                "title": meta["title"],
                "tagline": meta["tagline"],
                "guide": meta["guide"],
                "tropes": meta["tropes"],
                "books_count": len(matching_books),
                "books": matching_books,
                "subgenres": list(dict.fromkeys([sg for b in matching_books for sg in b["subgenres"]]))
            }

        subgenre_custom_meta = {
            "Western Short Stories": {
                "title": "Western Short Stories Pulp Fiction Ebooks",
                "tagline": "Gunslingers, Saloon Showdowns, and Dusty Frontier Action",
                "guide": "Step into the dusty streets and rowdy saloons of the American frontier with our western pulp short stories. Featuring high-stakes saloon brawls, quick-draw shootouts, and rugged cowboy heroes enforcing frontier justice.",
                "tropes": ["Saloon Brawls", "Quick-Draw Shootouts", "Frontier Justice", "Cowboy Legends"]
            },
            "Romantic Short Stories": {
                "title": "Romantic Short Stories Vintage Pulp Ebooks",
                "tagline": "Passionate Encounters, Steamy Dramas, and Vintage Pulp Intrigue",
                "guide": "Indulge in steamy romantic short stories inspired by golden-era pulp romance. Featuring passionate encounters, seductive twists, and dramatic emotional rivalries crafted for quick, captivating reading.",
                "tropes": ["Steamy Encounters", "Romantic Drama", "Vintage Romance", "Dramatic Suspense"]
            },
            "Scary Western & Horror Thrillers": {
                "title": "Scary Western & Horror Thrillers Pulp Ebooks",
                "tagline": "Haunted Frontiers, Ghost Towns, and Eerie Supernatural Westerns",
                "guide": "Discover chilling weird-west stories where eerie supernatural horrors stalk desolate frontier ghost towns and lonely desert trails. A unique blend of atmospheric horror and classic western grit.",
                "tropes": ["Ghost Towns", "Haunted Trails", "Weird West", "Supernatural Thriller"]
            },
            "Short Story Anthologies": {
                "title": "Short Story Anthologies Pulp Fiction Ebooks",
                "tagline": "Bite-Sized Pulp Fiction, Multi-Story Collections, and Fast-Paced Action",
                "guide": "Browse our curated short story anthologies offering fast-moving, action-packed fiction across western adventures, steamy romances, and spine-chilling suspense.",
                "tropes": ["Anthologies", "Fast Paced", "Multi-Genre", "Short Reads"]
            }
        }

        subgenre_map = {}
        for b in self.books:
            for sg in b["subgenres"]:
                if sg not in subgenre_map:
                    subgenre_map[sg] = []
                subgenre_map[sg].append(b)

        for sg_name, sg_books in subgenre_map.items():
            sg_slug = slugify(sg_name)
            if sg_slug not in self.genres:
                custom = subgenre_custom_meta.get(sg_name, {})
                self.genres[sg_slug] = {
                    "name": sg_name,
                    "slug": sg_slug,
                    "title": custom.get("title", f"{sg_name} Vintage Pulp Fiction Ebooks"),
                    "tagline": custom.get("tagline", f"Explore the Best {sg_name} Classic Pulp Novels"),
                    "guide": custom.get("guide", f"Discover our handpicked selection of {sg_name} vintage pulp fiction ebooks. Featuring {len(sg_books)} thrilling titles by celebrated authors with fast-paced storytelling and authentic retro atmosphere."),
                    "tropes": custom.get("tropes", ["Action Packed", "Vintage Aesthetic", "Relentless Suspense"]),
                    "books_count": len(sg_books),
                    "books": sg_books,
                    "subgenres": []
                }

    def build_themes(self):
        """Build 120+ Niche Theme & Tag programmatic pages."""
        theme_map = {}
        for b in self.books:
            for th in b["themes"]:
                if th not in theme_map:
                    theme_map[th] = []
                theme_map[th].append(b)

        additional_niche_themes = [
            ("Private Eye", "Gritty gumshoes, trench coats, and high-stakes detective mysteries."),
            ("Femme Fatale", "Deadly sirens, dangerous alliances, and noir mystery."),
            ("Cold War Espionage", "Secret agents, coded messages, and iron-curtain suspense."),
            ("1950s Crime", "Mid-century mobsters, getaway cars, and hardboiled police squads."),
            ("French Foreign Legion", "Legendary legionnaires defending remote Sahara outposts."),
            ("Desert Caravans", "Camel trains, nomadic warriors, and sun-baked trade routes."),
            ("Pirate Galleons", "High-seas warships, cannon smoke, and pirate captains."),
            ("Hidden Treasure", "Sunken galleons, forgotten maps, and ancient gold hoards."),
            ("Masked Highwaymen", "Cape Robin Hood heroes striking against oppressive tyrants."),
            ("Jungle Lost Cities", "Ancient stone temples hidden deep inside untamed jungles."),
            ("Man-Eating Beasts", "Lethal lions, leopards, and apex predators prowling the dark."),
            ("Undercover Cops", "Dangerous deep-cover police stings inside criminal syndicates."),
            ("Wandering Detectives", "Drifter sleuths solving murders across desolate towns."),
            ("Smuggling Rings", "Contraband traders, coastal coves, and illegal contraband."),
            ("Daring Prison Escapes", "Fortress breakouts, midnight tunneling, and desperate flights."),
            ("Sahara Sandstorms", "Survival against lethal desert dust storms and blazing sun."),
            ("Saloon Shootouts", "Wild West tavern brawls, quick-draw showdowns, and lawless frontier action."),
            ("Wild West Outlaws", "Gunslingers, bandits, and frontier justice in the American Old West."),
            ("Passionate Encounters", "Steamy vintage romances, emotional rivalry, and dramatic love affairs."),
            ("Supernatural Thrillers", "Eerie ghost towns, haunted frontier trails, and weird west horror."),
            ("Short Story Collections", "Fast-paced short fiction anthologies delivering instant pulp entertainment."),
            ("AI Created Fiction", "Experimental fiction crafted with artificial intelligence storytelling tools."),
            ("Naval Broadsides", "Ship-to-ship artillery warfare and thunderous naval battles."),
            ("Sword Duels", "Clashing blades, rapier fencing, and honorable duels."),
            ("Radio Serial Style", "Fast-paced cliffhanger fiction inspired by vintage radio dramas."),
            ("Dime Novel Thrills", "The pure, high-voltage action of golden age pulp magazines."),
            ("Afrikaans Pulp Classics", "Original vintage Afrikaans pulp literature (snelskrif & ontspanningslees)."),
            ("English Translated Classics", "Masterpiece pulp fiction translated for worldwide ebook readers."),
            ("Bush Pilots", "Daring aviators flying over unmapped African wilderness."),
            ("Desert Outpost Sieges", "Desperate garrisons holding out against overwhelming odds."),
            ("Lost Civilizations", "Enigmatic ancient empires hidden in uncharted Africa."),
            ("Vengeance & Blood Feuds", "Uncompromising justice and relentless vendettas."),
            ("Ghost Ships & Curses", "Cursed maritime vessels, phantom crews, and supernatural dread."),
            ("Diamond Smugglers", "Illicit rough diamond syndicates in the Namib and Kalahari."),
            ("Midnight Rides", "Horseback chases across mountain passes in the dead of night."),
            ("Revolver Shootouts", "Quick-draw pistol duels in smoky backrooms and desert frontiers."),
            ("Tribal Mysteries", "Ancient rituals, lost totems, and deep African lore."),
            ("Wilderness Survival", "Man vs nature in the harshest deserts and dense jungles."),
            ("Cape Frontier Action", "Historical swashbuckling set during the Cape colony era."),
            ("Military Brotherhood", "Bonds forged under fire in Foreign Legion companies."),
            ("Underworld Syndicates", "Organized crime rings, corrupt kingpins, and vice rings."),
            ("High Stakes Heists", "Daring bank robberies, gem thefts, and intricate plans."),
            ("Aviation Action", "Aerial dogfights, emergency landings, and flying pulp heroes."),
            ("Forbidden Tombs", "Archaeological expeditions uncovering deadly secrets."),
            ("Bounty Hunters", "Relentless trackers hunting fugitives across hostile frontiers."),
            ("Namib Desert Peril", "Survival across the skeleton coast and endless sand seas."),
            ("Kalahari Vultures", "Dangerous confrontations in the parched Kalahari wilderness."),
            ("Cederberg Secrets", "Mountain hideouts and forgotten cave caches in the Cederberg."),
            ("Mutiny on the High Seas", "Rebellious sailors taking command of galleons and frigates."),
            ("Cutlass Combat", "Close-quarters sword fighting aboard rocking ship decks."),
            ("Gold of Monomotapa", "Legends of legendary African gold mines and ancient kings."),
            ("Feral Warriors", "Wild heroes living in harmony with nature and deadly beasts."),
            ("Poacher Hunters", "Game rangers battling illegal ivory and diamond cartels."),
            ("Underground Informants", "Whispered tips, secret meetups, and espionage contacts."),
            ("Dime Novel Heroes", "Fearless pulp protagonists conquering impossible odds.")
        ]

        for name, desc in additional_niche_themes:
            if name not in theme_map:
                matches = [b for b in self.books if name.lower() in b["title"].lower() or name.lower() in b["synopsis"].lower() or name.lower() in [th.lower() for th in b["themes"]] or name.lower() in [sg.lower() for sg in b["subgenres"]]]
                if not matches:
                    if any(w in name.lower() for w in ["desert", "sahara", "legion", "namib", "kalahari"]):
                        matches = [b for b in self.books if b["primary_genre"] == "Desert Adventure & Foreign Legion"][:12]
                    elif any(w in name.lower() for w in ["pirate", "sea", "treasure", "naval", "ship", "mutiny", "cutlass"]):
                        matches = [b for b in self.books if b["primary_genre"] == "Pirate & High Seas Swashbuckler"][:12]
                    elif any(w in name.lower() for w in ["detective", "crime", "noir", "cop", "sleuth", "revolver", "smuggl", "informant"]):
                        matches = [b for b in self.books if b["primary_genre"] == "Hardboiled Detective & Noir Crime"][:12]
                    elif any(w in name.lower() for w in ["jungle", "beast", "lion", "safari", "lost", "feral", "monomotapa"]):
                        matches = [b for b in self.books if b["primary_genre"] == "Jungle Adventure & Lost Worlds"][:12]
                    elif any(w in name.lower() for w in ["masked", "highway", "cape", "sword", "ride", "cederberg"]):
                        matches = [b for b in self.books if b["primary_genre"] == "Masked Rogue & Highwayman"][:12]
                    else:
                        matches = self.books[:12]
                theme_map[name] = matches

        for th_name, th_books in theme_map.items():
            th_slug = slugify(th_name)
            self.themes[th_slug] = {
                "name": th_name,
                "slug": th_slug,
                "title": f"{th_name} Pulp Fiction Ebooks",
                "tagline": f"The Ultimate Collection of {th_name} Pulp Stories",
                "guide": f"Immerse yourself in our curated selection of vintage {th_name} pulp fiction ebooks. Featuring {len(th_books)} classic novels with authentic retro action, gripping suspense, and instant digital delivery.",
                "books_count": len(th_books),
                "books": th_books
            }

    def build_collections(self):
        """Build 550+ Curated Collections & Long-Tail pSEO Intent Landing Pages."""
        collection_templates = [
            ("Best Retro Crime Fiction on Amazon", "Explore the top vintage hardboiled crime, detective noir, and mid-century mystery pulp ebooks available on Amazon.", "Hardboiled Detective & Noir Crime"),
            ("Short Pulp Stories under $3", "Fast, thrilling, budget-friendly vintage pulp novels available online at just $2.99 or less.", "All"),
            ("Top 10 Classic Foreign Legion Novels", "The definitive reading list of French Foreign Legion desert warfare and military survival pulp fiction.", "Desert Adventure & Foreign Legion"),
            ("Ultimate Pirate Pulp Adventure Ebooks", "High-seas swashbucklers featuring galleon broadsides, cutlass duels, and pirate treasure islands.", "Pirate & High Seas Swashbuckler"),
            ("Vintage African Jungle Adventure Novels", "Iconic lost world and African wilderness pulp stories featuring legendary feral heroes and jungle danger.", "Jungle Adventure & Lost Worlds"),
            ("Best Hardboiled Detective Ebooks on Amazon", "Gritty private eyes, rain-soaked streets, and 1950s undercover police investigations.", "Hardboiled Detective & Noir Crime"),
            ("Top Swashbuckling Rogue & Highwayman Stories", "Classic masked vigilantes, daring midnight escapes, and cape frontier action.", "Masked Rogue & Highwayman"),
            ("Best 1950s Vintage Mystery Novels", "Nostalgic mid-century paperback mysteries with sharp sleuths and intricate whodunits.", "Hardboiled Detective & Noir Crime"),
            ("Complete Sahara Adventure Reading Order", "The complete chronological guide and reading list for F.A. Venter's legendary Sahara Adventure Series.", "Desert Adventure & Foreign Legion"),
            ("Complete Oloff the Pirate Series Reading Order", "Read Gerrie Radlof's master swashbuckler naval series in sequence from Book 1 to 25.", "Pirate & High Seas Swashbuckler"),
            ("Complete Masked Robber Chronology", "The definitive guide to 'Die Buiter' / 'The Masked Robber' cape frontier vigilante saga.", "Masked Rogue & Highwayman"),
            ("Top 20 Afrikaans Pulp Fiction Ebooks", "The finest vintage Afrikaans action, romance, and detective novels available worldwide.", "Afrikaans"),
            ("Top 20 English Translated Pulp Fiction Masterpieces", "Classic South African and international pulp fiction translated into English for global readers.", "English"),
            ("Fast-Paced Action Ebooks for Weekend Reading", "Binge-worthy, edge-of-your-seat pulp adventure thrillers you can finish in a single weekend.", "All"),
            ("Pulp Thrillers for Fans of Conan and Tarzan", "Feral heroics, lost civilizations, and brutal wilderness action for classic pulp fantasy enthusiasts.", "Jungle Adventure & Lost Worlds"),
            ("Vintage Espionage Novels for Fans of Ian Fleming", "Cold War spy craft, undercover agents, and deadly foreign conspiracies.", "Hardboiled Detective & Noir Crime"),
            ("Binge-Worthy Pulp Fiction Box Sets and Omnibuses", "Value-packed 3-in-1 collections and omnibus editions delivering hundreds of pages of pulp thrills.", "All"),
            ("Must-Read Desert Survival Thrillers", "Outpost sieges, searing sandstorms, and military grit in the unforgiving North African desert.", "Desert Adventure & Foreign Legion"),
            ("Underground Noir Crime Paperbacks", "Cigarette smoke, femme fatales, and lethal syndicate double-crosses in 1950s crime pulp.", "Hardboiled Detective & Noir Crime"),
            ("Classic Maritime Adventure Novels on Amazon", "Broadside naval battles, ghost ships, and fearless captains battling the high seas.", "Pirate & High Seas Swashbuckler"),
        ]

        for title, desc, filter_category in collection_templates:
            slug = slugify(title)
            if filter_category == "All":
                matching = self.books[:18]
            elif filter_category == "Afrikaans":
                matching = [b for b in self.books if "afrikaans" in b["lang"].lower()][:20]
            elif filter_category == "English":
                matching = [b for b in self.books if "english" in b["lang"].lower()][:20]
            else:
                matching = [b for b in self.books if b["primary_genre"] == filter_category][:20]

            self.collections.append({
                "title": title,
                "slug": slug,
                "description": desc,
                "books_count": len(matching),
                "books": matching,
                "category": filter_category
            })

        intents = [
            ("Best {} Ebooks on Amazon", "The ultimate curated list of top-rated {} pulp novels available for instant digital download."),
            ("Top 10 {} Pulp Fiction Classics", "Our editorial ranking of the 10 most thrilling {} stories you must read today."),
            ("Must-Read {} Thrillers", "High-octane {} books packed with suspense, action, and retro paperback style."),
            ("Ultimate Guide to {} Novels", "A comprehensive buyer's and reader's guide to the best {} pulp ebooks on Amazon."),
            ("Essential {} Vintage Paperbacks", "Rediscover the golden era of mid-century {} pulp fiction available online."),
            ("Cheap {} Ebooks Under $10 on Amazon", "Affordable, top-quality {} vintage pulp ebooks for your digital library."),
            ("Action-Packed {} Stories for Fast Reading", "Fast-moving {} pulp novels delivering instant excitement from the first page."),
            ("Classic {} Ebooks with Badass Protagonists", "Follow fearless heroes navigating high stakes and deadly danger in these {} masterpieces."),
            ("Top Ranked {} Books for Pulp Fiction Fans", "Community favorite {} pulp fiction ebooks ranked by excitement and storytelling quality."),
            ("Best {} Novels for Vacation Reading", "Gripping {} stories that will keep you captivated throughout your travels.")
        ]

        topics = [
            ("French Foreign Legion", "Desert Adventure & Foreign Legion"),
            ("Sahara Military Survival", "Desert Adventure & Foreign Legion"),
            ("High Seas Pirate Action", "Pirate & High Seas Swashbuckler"),
            ("Swashbuckling Buccaneer", "Pirate & High Seas Swashbuckler"),
            ("Hardboiled Private Detective", "Hardboiled Detective & Noir Crime"),
            ("1950s Undercover Crime", "Hardboiled Detective & Noir Crime"),
            ("Cape Frontier Vigilante", "Masked Rogue & Highwayman"),
            ("African Jungle Lost World", "Jungle Adventure & Lost Worlds"),
            ("Wilderness Bushveld Safari", "Safari & Bushveld Adventure"),
            ("Pulp Short Story Anthologies", "Western, Romance & Pulp Anthologies"),
            ("Francois Alwyn Venter Adventure", "Francois Alwyn Venter"),
            ("Gerrie Radlof Swashbuckler", "Gerrie Radlof"),
            ("Braam le Roux Jungle Hero", "Braam le Roux"),
            ("Sandbergh Beyers Military", "Sandbergh Beyers"),
            ("A.P. du Plessis Noir Detective", "A.P. du Plessis"),
            ("Die Buiter Masked Robber", "Die Buiter Reeks"),
            ("Oloff the Pirate High Seas", "Oloff the Pirate Series"),
            ("The Black Leopard African", "The Black Leopard Series"),
            ("Wanderer Detective Sleuth", "Wanderer Detective Series"),
            ("SA Police Hardboiled Crime", "SA Police Series"),
            ("Red Ruby Maritime Adventure", "Red Ruby Series"),
            ("Jungle Hawk Bush Pilot", "Jungle Hawk Series"),
            ("Untamed Lowveld Safari Mystery", "Untamed Lowveld Series"),
            ("Ryk Schoonraad Private Eye", "Ryk Schoonraad Series"),
            ("Afrikaans Vintage Ebooks", "Afrikaans"),
            ("English Translated Pulp Classics", "English"),
            ("Desert Outpost Sieges", "Desert Adventure & Foreign Legion"),
            ("Galleon Cannon Battles", "Pirate & High Seas Swashbuckler"),
            ("Midnight Sword Duels", "Masked Rogue & Highwayman"),
            ("Underworld Smuggling Rings", "Hardboiled Detective & Noir Crime"),
            ("Diamond Syndicate Thrillers", "Safari & Bushveld Adventure"),
            ("Lost Civilizations in Africa", "Jungle Adventure & Lost Worlds"),
            ("Revolver Shootout Action", "Hardboiled Detective & Noir Crime"),
            ("Vintage Pulp Box Sets", "All"),
            ("Classic Dime Novel Ebooks", "All"),
            ("Fast Paced Pulp Mysteries", "Hardboiled Detective & Noir Crime"),
            ("Treasure Hunting Pulp Stories", "Pirate & High Seas Swashbuckler"),
            ("Escape & Evasion Military Thrillers", "Desert Adventure & Foreign Legion"),
            ("Men's Adventure Vintage Paperbacks", "All"),
            ("Pulp Fiction Novellas", "All"),
            ("Cold War Spy Thrillers", "Hardboiled Detective & Noir Crime"),
            ("Vintage Crime Paperbacks", "Hardboiled Detective & Noir Crime"),
            ("Desert Caravan Romances", "Desert Adventure & Foreign Legion"),
            ("High Seas Mutiny Novels", "Pirate & High Seas Swashbuckler"),
            ("Feral Hero Jungle Sagas", "Jungle Adventure & Lost Worlds"),
            ("Cape Colony Historical Swashbucklers", "Masked Rogue & Highwayman"),
            ("Man Eating Beast Thrillers", "Jungle Adventure & Lost Worlds"),
            ("Bushveld Diamond Caches", "Safari & Bushveld Adventure"),
            ("Western Romance & Horror Pulp", "Western, Romance & Pulp Anthologies"),
            ("Pulp Fiction Masterpieces", "All"),
            ("Skeleton Coast Survival Novels", "Desert Adventure & Foreign Legion"),
            ("Kalahari Desert Espionage", "Desert Adventure & Foreign Legion"),
            ("Daring Prison Break Pulp Stories", "Desert Adventure & Foreign Legion"),
            ("Classic Highwayman Romances", "Masked Rogue & Highwayman"),
            ("Bounty Hunter Drifter Pulp", "Hardboiled Detective & Noir Crime"),
            ("Ancient Relic Quest Ebooks", "Jungle Adventure & Lost Worlds"),
            ("Undercover Police Infiltration", "Hardboiled Detective & Noir Crime"),
            ("Vintage Maritime Ghost Ship Tales", "Pirate & High Seas Swashbuckler"),
            ("Radio Drama Style Cliffhangers", "All"),
            ("Golden Age Paperback Thrillers", "All")
        ]

        for topic_name, category in topics:
            for pattern, desc_pattern in intents:
                col_title = pattern.format(topic_name)
                col_desc = desc_pattern.format(topic_name)
                col_slug = slugify(col_title)

                if any(c["slug"] == col_slug for c in self.collections):
                    continue

                if category == "All":
                    h = sum(ord(c) for c in col_title) % len(self.books)
                    matching = self.books[h:h+16]
                    if len(matching) < 8:
                        matching = self.books[:16]
                elif category in ["Afrikaans", "English"]:
                    matching = [b for b in self.books if category.lower() in b["lang"].lower()][:18]
                elif category in self.genres:
                    matching = self.genres[category]["books"][:18]
                elif category in self.authors:
                    matching = self.authors[category]["books"][:18]
                elif any(a["name"] == category for a in self.authors.values()):
                    matching = [b for b in self.books if b["author"] == category][:18]
                elif any(b["series"] == category for b in self.books):
                    matching = [b for b in self.books if b["series"] == category][:18]
                else:
                    kw = topic_name.lower().split()[0]
                    matching = [b for b in self.books if kw in b["title"].lower() or kw in b["synopsis"].lower() or kw in b["primary_genre"].lower()][:18]
                    if not matching:
                        matching = self.books[:16]

                self.collections.append({
                    "title": col_title,
                    "slug": col_slug,
                    "description": col_desc,
                    "books_count": len(matching),
                    "books": matching,
                    "category": topic_name
                })

    def build_series(self):
        """Build structured series collections with story descriptions, reading order, and metadata."""
        series_dict = {}
        for b in self.books:
            s_name = b.get("series") or "Other"
            s_slug = slugify(s_name)
            if not s_slug:
                s_slug = "other"
            if s_slug not in series_dict:
                series_dict[s_slug] = {
                    "name": s_name,
                    "slug": s_slug,
                    "books": [],
                    "authors": set(),
                    "languages": set(),
                    "genres": set(),
                    "sample_covers": []
                }
            series_dict[s_slug]["books"].append(b)
            series_dict[s_slug]["authors"].add(b["author"])
            series_dict[s_slug]["languages"].add(b["lang"])
            series_dict[s_slug]["genres"].add(b["primary_genre"])
            if b["img"] and len(series_dict[s_slug]["sample_covers"]) < 4:
                series_dict[s_slug]["sample_covers"].append(b["img"])

        # Sort books inside each series by book number
        for s_slug, s_data in series_dict.items():
            def sort_key(bk):
                num_str = str(bk.get("series_number", "999"))
                try:
                    return int(num_str)
                except ValueError:
                    return 999
            s_data["books"].sort(key=sort_key)
            s_data["books_count"] = len(s_data["books"])
            s_data["authors"] = list(s_data["authors"])
            s_data["languages"] = list(s_data["languages"])
            s_data["genres"] = list(s_data["genres"])
            s_data["primary_author"] = s_data["authors"][0] if s_data["authors"] else "Various"
            s_data["primary_genre"] = s_data["genres"][0] if s_data["genres"] else "Vintage Pulp Fiction"
            s_data["description"] = self.generate_series_description(s_data["name"], s_data["primary_author"], s_data["primary_genre"], s_data["books_count"], s_data["languages"])

        self.series = series_dict

        print(f"Data Engine loaded: {len(self.books)} books, {len(self.authors)} authors, {len(self.genres)} genres, {len(self.themes)} themes, {len(self.collections)} collections, {len(self.series)} series. Total landing pages: {len(self.books) + len(self.authors) + len(self.genres) + len(self.themes) + len(self.collections) + len(self.series) + 7}")

    def generate_series_description(self, series_name, author, genre, count, languages):
        """Generate high-engagement overview synopsis for a book series."""
        lang_str = ", ".join(languages)
        name_lower = series_name.lower()
        if "sahara" in name_lower or "aventure sahara" in name_lower or "abenteuer" in name_lower:
            return (
                f"The legendary **{series_name}** by {author} is one of the most famous military adventure and desert survival sagas in classic pulp fiction. "
                f"Spanning {count} pulse-pounding volumes available in {lang_str}, the series follows French Foreign Legion outposts, fearless legionnaires, "
                f"and perilous desert reconnaissance missions across treacherous Sahara sands. Experience the complete saga in reading order."
            )
        elif "swart luiperd" in name_lower or "black leopard" in name_lower:
            return (
                f"The iconic **{series_name}** by {author} is South Africa's premier jungle adventure pulp phenomenon. "
                f"Featuring {count} adrenaline-fueled novels in {lang_str}, the saga follows Leon Marais (The Black Leopard) through uncharted African wilderness, "
                f"hidden lost cities, ferocious man-eating beasts, and ancient tribal mysteries in classic pulp tradition."
            )
        elif "buiter" in name_lower or "masked robber" in name_lower:
            return (
                f"The celebrated **{series_name}** by {author} chronicles the daring exploits of a masked Cape highwayman who champions justice against corrupt colonial forces. "
                f"Across {count} thrilling historical adventure paperbacks in {lang_str}, expect fast horseback pursuits, sword duels, moonlit rescues, and high-velocity intrigue."
            )
        elif "seerower" in name_lower or "pirate" in name_lower or "red ruby" in name_lower or "maagd van die see" in name_lower:
            return (
                f"The sweeping **{series_name}** by {author} is an epic naval and high-seas swashbuckling saga packed with cannon battles, cutlass duels, "
                f"and maritime intrigue. Discover {count} legendary ocean adventures in {lang_str}, exploring pirate galleons, lost treasure islands, and daring naval captains."
            )
        elif "polisie" in name_lower or "police" in name_lower or "speurder" in name_lower or "detective" in name_lower or "schoonraad" in name_lower or "tamar" in name_lower:
            return (
                f"The gripping **{series_name}** by {author} is a vintage 1950s crime noir and detective series. "
                f"Featuring {count} hardboiled crime novels in {lang_str}, each installment follows fearless investigators unraveling underworld syndicates, "
                f"diamond smuggling rings, and dangerous conspiracies."
            )
        elif "oerwoudvalk" in name_lower or "jungle hawk" in name_lower or "woeste laeveld" in name_lower or "lowveld" in name_lower:
            return (
                f"The thrilling **{series_name}** by {author} captures the danger, romance, and untamed beauty of the African bushveld and aviation pulp. "
                f"With {count} exciting titles in {lang_str}, follow rugged bush pilots and game trackers confronting poachers, remote outpost perils, and wilderness survival."
            )
        else:
            return (
                f"The classic **{series_name}** by {author} features {count} vintage pulp fiction novels in {lang_str}. "
                f"Discover unforgettable characters, fast-paced action, and timeless retro storytelling available in digital ebook editions."
            )

if __name__ == "__main__":
    engine = PulpDataEngine()
