"""
Enrichment Engine for Pulp Fiction Catalog
Provides deep, unique semantic synopsis generation, story highlights,
archival collector notes, series navigation linking, and editorial guides
for books, themes, and curated collections.
"""

import re
import html

# --- Historical and Literary Author Context ---
AUTHOR_CONTEXT = {
    "Francois Alwyn Venter": {
        "style": "renowned for raw, visceral battlefield tension and meticulous military realism",
        "era": "the golden age of Afrikaans pulp fiction in the 1950s and 1960s",
        "legacy": "F.A. Venter (1916–1997) was a towering titan of South African literature whose Sahara sagas became legendary staples of bedside reading",
        "hero_archetype": "battle-hardened French Foreign Legionnaires facing brutal desert skirmishes with unshakeable fortitude"
    },
    "Gerrie Radlof": {
        "style": "celebrated for blistering narrative momentum, rapid-fire dialogue, and dashing swashbuckling heroics",
        "era": "the mid-century heyday of South African paperback serials (Keurbiblioteek and Pronkboeke)",
        "legacy": "Gerrie Radlof (Gerrit van Zyl) was the indisputable master of high-octane escapist pulp, penning over a hundred unforgettable adventure novels",
        "hero_archetype": "fearless masked highwaymen, daring high-seas pirates, and sharp 1950s undercover sleuths"
    },
    "Braam le Roux": {
        "style": "famed for untamed feral heroics, pulse-pounding lost-world mysteries, and primeval wilderness perils",
        "era": "the 1950s boom of African wilderness adventure pulp",
        "legacy": "Braam le Roux created unforgettable pulp icons including 'Die Swart Luiperd', capturing the imagination of hundreds of thousands of readers",
        "hero_archetype": "Leon Marais, the masked Black Leopard champion wandering uncharted jungles with his loyal tame leopards"
    },
    "Sandbergh Beyers": {
        "style": "distinguished by harsh desert survival realism, tactical skirmishes, and deep bonds of military brotherhood",
        "era": "the classic era of Sahara desert warfare paperbacks",
        "legacy": "Sandbergh Beyers specialized in relentless outpost defenses, desert tracking, and high-tension survival against overwhelming odds",
        "hero_archetype": "resolute legionnaire scouts and desert garrison defenders holding remote frontier lines"
    },
    "Andreas du Plessis": {
        "style": "steeped in gritty 1950s hardboiled crime noir, smoke-filled detective offices, and cold-war intrigue",
        "era": "the post-war paperback explosion of crime and espionage thrillers",
        "legacy": "Andreas du Plessis created Ryk Schoonraad, South Africa's most iconic hardboiled private investigator",
        "hero_archetype": "tough, cynical private investigators navigating syndicate conspiracies and lethal double-crosses"
    },
    "Pieter Haasbroek": {
        "style": "combining authentic retro pulp energy with contemporary digital storytelling and restoration",
        "era": "modern vintage revival and digital preservation",
        "legacy": "Pieter Haasbroek acts as curator and author, bringing forgotten mid-century gems into the digital ebook era",
        "hero_archetype": "rugged frontier trackers, desert survivors, and resourceful adventurers"
    }
}

DEFAULT_AUTHOR_CONTEXT = {
    "style": "richly atmospheric storytelling, unrelenting pacing, and classic mid-century pulp suspense",
    "era": "the golden age of mid-century adventure fiction",
    "legacy": "preserving the vibrant storytelling traditions of 20th-century popular fiction",
    "hero_archetype": "daring protagonists battling formidable adversaries across dangerous frontiers"
}

# --- Title Semantic Concepts & Deep Narrative Frameworks ---
# Each tuple: (regex_pattern, hook, conflict_p1, narrative_p2, literary_focus_p3)
TITLE_THEME_RULES = [
    # 1. Triumph, Victory, Climax
    (
        r"(se[eë]vier|triumph|oorwinning|victor|victory|erfgenaam)",
        "The climactic resolution and long-awaited triumph of justice",
        "The long-simmering battle for justice reaches an explosive, triumphant crescendo where lingering vendettas, corrupt conspiracies, and ruthless adversaries must be decisively confronted in a high-stakes final showdown.",
        "As the oppressive net tightens around our hero, every ally's loyalty is tested to its absolute limit. Infiltrating high-security colonial bastions, deciphering intercepted dispatches, and coordinating a decisive counter-offensive require split-second precision. Rather than relying on brute force alone, victory demands psychological acumen, audacious misdirection, and selfless gallantry.",
        "This volume serves as a celebratory benchmark in the saga, demonstrating how classic mid-century pulp heroes overcame impossible odds with wit, courage, and moral clarity."
    ),
    # 2. Vengeance, Retribution
    (
        r"(wraak|vengeance|revenge|vergelding|bloedwraak)",
        "A relentless quest for retribution across hostile frontiers",
        "Driven by an uncompromising code of honor, the protagonist embarks on a grueling expedition to avenge fallen comrades and settle a deadly score that corrupt authorities failed to resolve.",
        "Tracking across harsh, waterless expanses tests the limits of physical and mental resilience. Haunted by the memories of fallen comrades, the protagonist presses forward where lesser men would turn back, facing venomous vipers, sun blindness, and ambush at solitary desert oases. The trail of retribution demands sacrifices, forcing the hero to choose between cold vengeance and the rescue of innocent captives.",
        "A quintessential frontier vendetta novel that captures the raw emotional stakes and moral complexities of personal retribution in untamed territories."
    ),
    # 3. Fortresses, Sieges, Strongholds, Outposts
    (
        r"(fort|stronghold|vesting|citadel|outpost|bouvalle|ruins|kasteel)",
        "A desperate siege and defense of a fortified frontier bastion",
        "A heavily fortified redoubt becomes the focal point of intense military strategy, where besieged defenders face overwhelming numerical odds and cutting-edge tactical assaults.",
        "Surrounded by hostile forces and cut off from reinforcement, the garrison must maintain morale as ammunition dwindles and heat exhaustion sets in. Breached palisades, midnight skirmishes beneath flare-lit skies, and desperate counter-charges characterize the defense of this remote outpost. Every soldier must rise above fear to hold the line against overwhelming numbers.",
        "A masterclass in siege warfare and defensive tactics, this gripping installment delivers claustrophobic tension and explosive frontline combat."
    ),
    # 4. Bloodshed, Lethal Combat, Massacre
    (
        r"(bloodbath|bloed|blood|dood\s+met|death\s+at|dodelik|lethal|slagting)",
        "A high-stakes, life-or-death confrontation against staggering odds",
        "The narrative plunges into raw, uncompromising combat where survival hinges on split-second decisions, raw nerve, and fierce hand-to-hand engagements.",
        "The confrontation escalates with terrifying ferocity as combatants clash in close-quarters warfare. Amidst cannon blast, rifle fire, and flashing steel, survival depends on instant reflexes and brotherhood under fire. The narrative captures the grim reality of frontier warfare with breathless immediacy, delivering relentless cliffhangers with every turning page.",
        "Delivering the visceral battlefield realism that defined mid-century military paperbacks, this story stands as an unforgettable highlight of heroic courage."
    ),
    # 5. Death, Skeletons, Skulls
    (
        r"(dood|death|skull|doodskop|geraamte|skeleton|graf|tomb)",
        "A brush with mortality amidst treacherous hidden perils",
        "Danger stalks every step as the characters confront lethal traps, ruthless killers, and haunting symbols of past catastrophes that warningly mark the trail ahead.",
        "Traversing forgotten canyons littered with bleached bones and crumbling stone markers, our heroes must decipher cryptic warnings left by previous expeditions that vanished without a trace. Every shadow conceals a potential sniper, and every narrow pass threatens a sudden rockslide or poisoned dart, keeping adrenaline levels at peak intensity.",
        "Rich in eerie atmosphere and gothic pulp suspense, this novel expertly blends high adventure with spine-chilling frontier dread."
    ),
    # 6. Tracking, Spoor, Footsteps
    (
        r"(spoor|spore|footsteps|track|tracker|jag|hunt|jaag|pursuit)",
        "A deadly manhunt tracking footsteps across punishing terrain",
        "A razor-sharp game of cat and mouse unfolds where every footprint in the dust and broken twig reveals the proximity of a cunning quarry who may well be laying an ambush.",
        "Reading subtle disturbances in the dust, crushed desert scrub, and abandoned camp debris, the tracker pieces together the adversary's desperate flight. Yet as the quarry realizes he is being stalked, the hunter risks becoming the hunted. Deadly ambushes, false trails, and sudden skirmishes in narrow rock defiles keep readers guessing until the explosive confrontation.",
        "Showcasing the meticulous art of bushcraft and frontier tracking, this novel is an authentic, tension-fueled pursuit story."
    ),
    # 7. Night, Midnight, Shadows, Darkness
    (
        r"(nag|snags|night|midnight|shadow|skadu|skemer|donker|dark)",
        "Nocturnal operations, midnight rides, and shadow warfare",
        "Cloaked by darkness, the hero navigates moonlit trails and hostile cordons to strike secretly and vanish before the enemy garrison can mount an organized pursuit.",
        "Under the shroud of night, stealth and surveillance take center stage as the protagonist monitors hostile troop movements across dark mountain passes. With only moonlight reflecting off drawn blades and muffled hoofbeats breaking the nocturnal silence, every second spent behind enemy lines carries the threat of instant capture.",
        "A quintessential nocturnal pulp thriller, celebrated for its atmospheric darkness, galloping horseback chases, and silent infiltration."
    ),
    # 8. Traps, Deception, Betrayal, Ambush
    (
        r"(lokval|trap|hinderlaag|ambush|verraad|betrayal|verraaier|traitor|agterdog)",
        "Deceptive colonial traps, false allies, and deadly ambushes",
        "The protagonist walks into a meticulously prepared snare engineered by calculating conspirators, forcing an audacious escape through quick thinking and sheer daring.",
        "A counterfeit summons and a compromised route deliver our hero directly into the crosshairs of enemy forces. Trapped in a rocky ravine with escape cut off, survival demands audacious misdirection, utilizing every natural obstacle and lightning-fast reactions to turn the ambushers' trap completely against them.",
        "Packed with psychological intrigue and tactical reversals, this tale exemplifies the thrilling cat-and-mouse plotting of classic pulp literature."
    ),
    # 9. Sorcery, Witches, Mysticism, Curses
    (
        r"(heks|witch|tower|curse|vloek|geheimsinnig|mystic|professie)",
        "Enigmatic desert legends, tribal mysticism, and eerie prophecies",
        "Folk superstition and desert lore intertwine with raw physical adventure as whispers of a shadowy mystic draw soldiers and nomads into unpredictable peril.",
        "Nomadic oral traditions and eerie desert folklore shroud the central mystery, blurring the line between tribal superstition and calculated psychological warfare. The protagonist must separate fact from myth to untangle a web of deception that has paralyzed frontier garrisons with dread.",
        "An exotic, spellbinding blend of folklore intrigue, psychological tension, and gritty frontier combat that transports readers to another era."
    ),
    # 10. Sea, Pirates, Ships, Cannons, Ocean
    (
        r"(seerower|pirate|see|sea|skip|ship|galleon|cannon|kanon|vloot|fleet|boord|ocean|swart\s+seile|black\s+sails)",
        "Swashbuckling naval warfare, broadsides, and high-seas daring",
        "Tall-masted frigates clash amidst cannon smoke, splintering timbers, and flashing cutlasses as buccaneers battle rival captains and imperial navies for maritime supremacy.",
        "Heeling over under full sail in treacherous crosswinds, the vessel maneuvers for the weather gauge to unleash devastating broadsides. Grappling hooks fly and cutlasses clash as boarding parties surge across blood-slicked decks. The salty spray, creaking timbers, and thunderous ordnance bring the golden age of buccaneer warfare to vivid life.",
        "A stirring naval swashbuckler brimming with authentic seamanship, explosive broadside artillery, and daring high-seas heroics."
    ),
    # 11. Jewels, Diamonds, Gold, Treasure
    (
        r"(robyn|ruby|skat|treasure|diamant|diamond|goud|gold|silwer|silver|ivory|ivoor)",
        "A perilous quest for fabled gems and contested fortunes",
        "Lured by rumors of an invaluable treasure cache, rival expeditions clash ruthlessly in remote frontiers where human greed proves just as lethal as hostile wildlife.",
        "Lured by the legend of an ancient gemstone hoard, rival expeditions race through unforgiving terrain where human treachery proves deadlier than wild beasts. Secret maps, deciphered ciphers, and treacherous guides lead ever deeper into forbidden territory where gold and blood have historically mingled.",
        "A high-stakes treasure quest packed with deadly double-crosses, archaeological intrigue, and unrelenting frontier danger."
    ),
    # 12. Vigilance, Watch, Secret Identity
    (
        r"(hou\s+wag|keeps\s+watch|watch|geheim|secret|mantel|mantle|mask|vermom)",
        "A tense nocturnal vigil guarding imperiled innocents and secret identities",
        "Under the cover of night, our protagonist keeps watch over vulnerable allies, balancing the preservation of a guarded double life against the immediate threat of military discovery.",
        "Silence and shadows become the protagonist's most vital weapons as the night unfolds. Perched above treacherous ravines, monitoring the flickering campfires of advancing patrols, Armand de la Harpe must anticipate enemy traps before they can be sprung. Tension builds steadily as unexpected complications threaten to expose his vantage point, transforming a quiet reconnaissance mission into a desperate tactical duel.",
        "Masterfully illustrating the tactical stealth and chivalric vigilance of the masked rogue, this installment highlights the selfless courage that forged a folk legend."
    ),
    # 13. Crime, Police, Undercover, Mob
    (
        r"(polisie|police|speurder|detective|bende|gang|smokkel|smuggl|misdaad|crime|moord|murder|dief|thief)",
        "Undercover police operations, syndicate raids, and hardboiled noir intrigue",
        "Detectives infiltrate dangerous underground smuggling rings and mob syndicates where one false step can lead to a shallow grave on the city outskirts.",
        "Operating deep beneath cover, the investigator moves through a labyrinth of smoke-filled speakeasies, dockside warehouses, and corrupt officialdom. With danger mounting on both sides of the law, every contact could be an undercover agent or an assassin waiting in the shadows with a snub-nosed revolver.",
        "A razor-sharp mid-century crime procedural featuring gritty dialogue, urban menace, and authentic police detective tradecraft."
    ),
    # 14. Wild Beasts, Jungle, Leopards, Predators
    (
        r"(luiperd|leopard|valk|hawk|leeu|lion|tier|tiger|wolf|oerwoud|jungle|roofdier|predator|beast)",
        "Feral heroics and apex predator encounters in uncharted jungles",
        "Navigating primeval forests and untamed wilderness, the hero battles rogue beasts, hostile poachers, and ancient tribal hazards in harmony with loyal feline companions.",
        "Deep within the primeval canopy where daylight barely filters through the leaves, primeval dangers await. Guided by the uncanny instincts of his tame leopards, Leon Marais uncovers ancient Monomotapa stone ruins, defies poisoned arrows, and battles ruthless poachers intent on ravaging the sanctuary.",
        "An exhilarating wilderness adventure that captures the untamed spirit of Edgar Rice Burroughs and golden-era African jungle pulp."
    ),
    # 15. Desert, Dunes, Blistering Sun
    (
        r"(woestyn|desert|sahara|dunes|duine|son|sun|hitte|heat|sand|kalahari|namib)",
        "A punishing struggle for survival against the scorching Sahara sands",
        "Blistering heatwaves, blinding sandstorms, and treacherous dunes test human endurance to the absolute limit as rival factions clash around life-saving desert wells.",
        "The Sahara itself is a formidable antagonist—an ocean of shifting red dunes where water is more precious than gold and sandstorms can swallow an entire patrol in minutes. Tactical desert maneuvers, camel charges, and oasis skirmishes are rendered with vivid sensory detail that puts readers directly into the scorching heat.",
        "A tour-de-force of desert survival literature, celebrated for its punishing authenticity, military camaraderie, and raw emotional intensity."
    )
]

def analyze_title_semantics(title, series, genre, author, lang):
    """Analyze title and metadata to extract unique plot hook and narrative themes."""
    title_clean = title.strip()
    title_lower = title_clean.lower()
    
    # Check matched rules
    matched_themes = []
    for pattern, hook, conflict_p1, narrative_p2, literary_p3 in TITLE_THEME_RULES:
        if re.search(pattern, title_lower):
            matched_themes.append((hook, conflict_p1, narrative_p2, literary_p3))
    
    # Fallback if no regex matched
    if not matched_themes:
        hook = f"A thrilling standalone adventure in the saga of {title_clean}"
        conflict_p1 = (
            f"Set against the vibrant backdrop of {genre.lower()}, the narrative thrusts our protagonist "
            f"into an unexpected crisis where razor-sharp reflexes and moral courage become the sole defense against mounting danger."
        )
        narrative_p2 = (
            "Facing overwhelming odds and a rapidly closing window of opportunity, the hero must navigate "
            "unforgiving terrain, deceptive alliances, and armed adversaries determined to eliminate all resistance. "
            "Every chapter escalates the suspense, delivering unrelenting momentum from the opening scene to the climax."
        )
        literary_p3 = (
            "Crafted in the finest traditions of mid-century paperback pulp, this novel offers unforgettable characters, "
            "relentless cliffhangers, and pure escapist excitement."
        )
        matched_themes.append((hook, conflict_p1, narrative_p2, literary_p3))
        
    primary_theme = matched_themes[0]
    secondary_theme = matched_themes[1] if len(matched_themes) > 1 else None
    
    return primary_theme, secondary_theme

def generate_rich_book_synopsis(title, author, series, genre, lang, num, store_key="amazon"):
    """
    Generate a 3-paragraph, deeply differentiated, engaging literary synopsis.
    Each paragraph addresses:
    1. Title-specific premise, inciting incident, and hook.
    2. Conflict dynamics, adversarial forces, setting, and stakes.
    3. Pulp style, author context, pacing, and collector appeal.
    """
    auth_ctx = AUTHOR_CONTEXT.get(author, DEFAULT_AUTHOR_CONTEXT)
    primary_theme, _ = analyze_title_semantics(title, series, genre, author, lang)
    hook_desc, conflict_p1, narrative_p2, literary_p3 = primary_theme
    
    # Series & Volume Context
    num_str = str(num).strip() if num and str(num) not in ("", "None", "999") else ""
    if num_str and series and series != "Other":
        vol_ctx = f"Serving as Book #{num_str} in the renowned {series}"
        continuity_note = f"While delivering a vital chapter in the broader narrative arc of {series}, this novel is engineered to function equally well as a thrilling standalone adventure."
    elif series and series != "Other":
        vol_ctx = f"An integral volume in the acclaimed {series}"
        continuity_note = f"Presented as part of {series}, this installment enriches the expansive lore and character journeys of the saga."
    else:
        vol_ctx = "A self-contained vintage pulp masterpiece"
        continuity_note = "Crafted as a complete standalone story, it offers readers an uninhibited, immersive adventure from start to finish."

    # Language and Retailer Note
    if "afrikaans" in lang.lower():
        lang_note = "written in authentic, evocative Afrikaans capturing the rich idiom and colloquial flair of the era"
    elif "english" in lang.lower():
        lang_note = "translated into crisp, dynamic English that preserves the raw storytelling momentum of the original"
    else:
        lang_note = f"presented in an engaging {lang} digital edition for international pulp enthusiasts"

    store_cta = "Amazon Kindle" if store_key == "amazon" else store_key.capitalize()

    # Paragraph 1: Title-Specific Premise & Hook
    p1 = (
        f"**{title}** by {author} plunges readers into a masterclass of vintage action and narrative suspense. "
        f"{vol_ctx}, the story centers around {hook_desc.lower()}. "
        f"{conflict_p1} "
        f"From the arresting opening scene to the high-voltage revelations that follow, {author} establishes a world where every decision carries life-or-death consequences."
    )

    # Paragraph 2: Central Conflict, Setting & Adversary Dynamics (Theme-Specific)
    p2 = (
        f"{narrative_p2} "
        f"{continuity_note}"
    )

    # Paragraph 3: Pulp Atmosphere, Pacing & Literary Style (Author & Theme Specific)
    p3 = (
        f"{literary_p3} "
        f"Celebrated as a prime example of {auth_ctx['era']}, this work highlights why {author} is {auth_ctx['style']}. "
        f"Carefully digitized and preserved from original mid-century physical paperbacks, this edition is {lang_note}, "
        f"available instantly on {store_cta} for eReaders, tablets, and smartphones."
    )

    return f"{p1}\n\n{p2}\n\n{p3}"

def generate_story_highlights(title, author, series, genre, lang, num):
    """Generate 4 structured, unique story highlight cards for the book detail page."""
    primary_theme, _ = analyze_title_semantics(title, series, genre, author, lang)
    hook_desc, _, _, _ = primary_theme
    
    num_str = str(num).strip() if num and str(num) not in ("", "None", "999") else ""
    series_text = f"Book #{num_str} in {series}" if num_str and series else (series if series and series != "Other" else "Standalone Pulp Novel")
    
    # Setting determination
    genre_lower = genre.lower()
    if "desert" in genre_lower or "sahara" in title.lower():
        setting = "North African Sahara Desert, remote Foreign Legion garrison outposts, and sun-baked dune expanses."
    elif "pirate" in genre_lower or "see" in title.lower() or "ocean" in title.lower():
        setting = "The high seas, Caribbean archipelagos, pirate coves, and storm-battered wooden galleons."
    elif "masked" in genre_lower or "buiter" in title.lower():
        setting = "18th-century Cape Colony, rugged Drakenstein mountain passes, and candlelit frontier homesteads."
    elif "detective" in genre_lower or "noir" in genre_lower or "polisie" in title.lower():
        setting = "1950s urban South Africa, smoky detective offices, mining syndicates, and rain-slicked city streets."
    elif "jungle" in genre_lower or "luiperd" in title.lower():
        setting = "Uncharted African wilderness, forgotten ancient temple ruins, and dense primeval forests."
    elif "safari" in genre_lower or "lowveld" in genre_lower or "laeveld" in title.lower():
        setting = "The untamed Lowveld bushveld frontier, remote cattle stations, and wild game trails."
    else:
        setting = "Classic mid-century pulp frontier settings evoking the golden age of paperback action."

    highlights = [
        {
            "icon": "⚔️",
            "label": "Core Conflict",
            "text": hook_desc
        },
        {
            "icon": "🗺️",
            "label": "Atmospheric Setting",
            "text": setting
        },
        {
            "icon": "⚡",
            "label": "Pacing & Narrative Tone",
            "text": "Rapid-fire cliffhangers, high-velocity dialogue, and pulse-pounding action tailored for a 2–4 hour immersive read."
        },
        {
            "icon": "📖",
            "label": "Series Continuum",
            "text": series_text
        }
    ]
    return highlights

def generate_preservation_note(author, title, digital_edition_year="2024"):
    """Generate an authoritative archival preservation statement."""
    auth_ctx = AUTHOR_CONTEXT.get(author, DEFAULT_AUTHOR_CONTEXT)
    return (
        f"**Archival Digital Preservation:** *{title}* has been digitally remastered and preserved by Softcover Books "
        f"from scarce mid-century physical paperbacks. As part of our cultural pulp preservation project, original cover artwork "
        f"and unabridged prose are curated to honor {auth_ctx['legacy']}, making these rare classics permanently accessible to readers worldwide."
    )

def generate_unique_meta_description(title, author, series, num, genre, lang):
    """Generate a high-CTR, strictly under 155 characters meta description."""
    num_str = f" #{num}" if num and str(num) not in ("", "None", "999") else ""
    series_str = f" ({series}{num_str})" if series and series != "Other" else ""
    lang_str = f" in {lang}" if lang and lang != "English" else ""
    
    # Generate concise, punchy description
    meta = f"Read {title} by {author}{series_str}. Vintage {genre.lower()} pulp novel{lang_str}. Fast-paced action & instant digital download."
    if len(meta) > 155:
        meta = f"Read {title} by {author}{series_str}. Vintage {genre.lower()} pulp ebook. Instant digital download."
    if len(meta) > 155:
        meta = f"Read {title} by {author}. Vintage {genre.lower()} ebook. Instant digital download."
    return meta

def get_theme_editorial_guide(theme_name, books_count):
    """Generate a rich, multi-paragraph editorial guide for a theme hub page."""
    name_clean = theme_name.strip()
    return (
        f"Explore our definitive collection of vintage **{name_clean}** pulp fiction ebooks. "
        f"In the golden age of mid-century paperbacks, the {name_clean.lower()} trope stood out as a reader-favorite motif, "
        f"delivering high-voltage suspense, larger-than-life heroics, and evocative atmosphere. "
        f"Featuring {books_count} carefully curated titles from celebrated authors, this selection captures the timeless "
        f"storytelling energy that defined vintage adventure literature. Each title has been restored and optimized for modern e-readers, "
        f"offering instant digital access to unforgettable retro fiction."
    )

def get_collection_editorial_guide(col_title, topic_name, books_count, sample_books):
    """Generate a high-value, bespoke 3-paragraph editorial guide for a curated collection."""
    featured_str = ", ".join(f'"{b["title"]}"' for b in sample_books[:3]) if sample_books else "classic titles"
    authors_str = ", ".join(list(dict.fromkeys(b["author"] for b in sample_books[:4]))) if sample_books else "celebrated authors"
    
    p1 = (
        f"Welcome to our premier reading list for **{col_title}**. "
        f"Curated specifically for connoisseurs of vintage pulp fiction and retro adventure, this collection showcases {books_count} "
        f"outstanding titles that best embody the spirit of {topic_name.lower()}. "
        f"Key highlights in this collection include {featured_str}, each offering unmatched narrative drive and memorable characters."
    )
    p2 = (
        f"Every title featured here has been hand-selected based on narrative authenticity, character depth, and thematic excellence. "
        f"Showcasing the work of masters such as {authors_str}, these novels represent the pinnacle of mid-20th century popular literature. "
        f"Whether you are seeking nail-biting outpost sieges, thrilling cutlass duels, nocturnal highwayman raids, or gritty 1950s detective investigations, "
        f"each book in this guide delivers authentic, unadulterated escapism."
    )
    p3 = (
        f"All titles are fully digitized and available instantly for Amazon Kindle and compatible reading apps, many priced under $5. "
        f"Whether you are building a comprehensive digital library or simply picking your next thrilling weekend read, "
        f"this curated list provides the ideal starting point. Dive into any volume today and rediscover the lost art of the great pulp adventure."
    )
    return p1, p2, p3
