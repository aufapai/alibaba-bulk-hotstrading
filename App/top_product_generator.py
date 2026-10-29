import sqlite3
import random
import os
import sys

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from currency_calculator import calculate_packaging_and_carton, get_live_usd_idr_rate
from accio_keyword_generator import generate_accio_listing
from market_intelligence import CONTINENTAL_MARKET_RULES, get_current_quarter

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Contextual scene descriptions tailored to destination country/continent & season
COUNTRY_SCENE_MAP = {
    "Europe": {
        "countries": ["Germany", "United Kingdom", "Netherlands", "France", "Poland"],
        "scenes": {
            "Safety": "a European industrial construction site in Germany on a wet cold autumn morning with steel beams and yellow safety tape",
            "Chef": "a busy European restaurant kitchen in Berlin with clean wet anti-slip commercial floor tiles",
            "Terra": "a damp European countryside farm pathway after rain with autumn leaves and light mist",
            "General": "a modern European commercial warehouse loading dock on a cool rainy day"
        }
    },
    "North America": {
        "countries": ["United States", "Canada", "Mexico"],
        "scenes": {
            "Safety": "a North American civil engineering worksite in Texas with concrete structures and heavy machinery in outdoor daylight",
            "Chef": "a fast-paced American commercial food prep facility with stainless steel counters and wet tile floor",
            "Terra": "a North American muddy agricultural farmstead during rainy harvesting season",
            "General": "an industrial logistics distribution center concrete floor with OSHA safety guidelines"
        }
    },
    "Southeast Asia": {
        "countries": ["Malaysia", "Thailand", "Philippines", "Vietnam", "Singapore"],
        "scenes": {
            "Safety": "a Southeast Asian manufacturing plant and construction project during tropical monsoon conditions",
            "Chef": "a Southeast Asian hotel catering kitchen with wet anti-slip safety flooring",
            "Terra": "a tropical oil palm plantation in Malaysia with muddy terrain and puddles during monsoon rain",
            "General": "a wet city asphalt street during heavy tropical monsoon rain with puddle reflections"
        }
    },
    "Middle East": {
        "countries": ["United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait"],
        "scenes": {
            "Safety": "a high-profile infrastructure construction foundation project in Dubai with concrete structures and desert daylight",
            "Chef": "a modern luxury hotel culinary preparation center in Abu Dhabi with slip-resistant hygienic flooring",
            "Terra": "an agricultural greenhouse and irrigation facility in Saudi Arabia",
            "General": "an industrial petrochemical refinery maintenance yard in the Gulf region"
        }
    },
    "Oceania": {
        "countries": ["Australia", "New Zealand"],
        "scenes": {
            "Safety": "an Australian civil construction worksite and mining facility under clear outdoor daylight",
            "Chef": "an Australian food processing and dairy packaging plant with wet hygienic floor",
            "Terra": "a lush New Zealand dairy farm pasture and agricultural paddock in morning dew",
            "General": "a commercial fishery harbor wet deck and seafood processing wharf in Australia"
        }
    }
}

def pick_top_products(category_filter=None, continent_filter=None, count=5, mode="top_sellers"):
    """
    Picks top products based on category or target destination country/continent.
    Modes:
      - 'top_sellers': Highest sold_count and rating_score
      - 'flagship': From Flagship 40 list
      - 'random_sample': Random sample among top 50 products
    """
    conn = get_db()
    cur = conn.cursor()

    conditions = ["image_1 LIKE 'http%'"]
    params = []

    if category_filter and category_filter not in ["", "all", "All Footwear Categories"]:
        conditions.append("category_group = ?")
        params.append(category_filter)

    where_clause = " WHERE " + " AND ".join(conditions)

    if mode == "flagship":
        sql = f"SELECT * FROM products {where_clause} AND is_flagship = 1 ORDER BY flagship_rank ASC LIMIT 50"
    elif mode == "top_sellers":
        sql = f"SELECT * FROM products {where_clause} ORDER BY sold_count DESC, rating_score DESC LIMIT 50"
    else: # random among qualified
        sql = f"SELECT * FROM products {where_clause} ORDER BY is_flagship DESC, sold_count DESC LIMIT 60"

    cur.execute(sql, params)
    candidates = [dict(r) for r in cur.fetchall()]
    conn.close()

    if not candidates:
        return []

    count = min(int(count), len(candidates))
    if mode == "random_sample":
        selected = random.sample(candidates, count)
    else:
        selected = candidates[:count]

    return selected

def generate_tailored_product_package(product, destination_country=None, target_continent="Europe", preferred_angle=None):
    """
    For a given product and target destination:
    1. Generates 4-slot AI Image Prompts tailored to destination country/continent
    2. Generates Accio Title & SEO Keywords
    3. Calculates carton packaging, FOB USD, IDR, CBM, and shipping metrics
    """
    p_title = product.get("product_title", "")
    p_sku = product.get("sku", "")
    p_cat = product.get("category_group", "AP Boots")
    p_color = product.get("color", "Black").split(";")[0].strip()
    p_usd = float(product.get("price_usd") or 5.50)
    p_img = product.get("image_1") or ""

    clean_name = p_title.split(" - ")[0].strip() if " - " in p_title else p_title.strip()

    # 1. Destination Country Resolution
    if not destination_country or destination_country == "auto":
        c_info = COUNTRY_SCENE_MAP.get(target_continent, COUNTRY_SCENE_MAP["Europe"])
        destination_country = c_info["countries"][0]

    # Find continent from country if continent not directly matched
    detected_continent = target_continent
    for cont, data in COUNTRY_SCENE_MAP.items():
        if destination_country in data["countries"]:
            detected_continent = cont
            break

    scene_data = COUNTRY_SCENE_MAP.get(detected_continent, COUNTRY_SCENE_MAP["Europe"])["scenes"]
    
    # Pick contextual usage scene
    cat_l = p_cat.lower()
    if "safety" in cat_l or "s5" in cat_l or "orca" in cat_l:
        ctx_scene = scene_data["Safety"]
        pairs_ctn = 12
    elif "chef" in cat_l:
        ctx_scene = scene_data["Chef"]
        pairs_ctn = 18
    elif "terra" in cat_l:
        ctx_scene = scene_data["Terra"]
        pairs_ctn = 12
    elif "medic" in cat_l:
        ctx_scene = scene_data["Chef"].replace("kitchen", "medical clinic / cleanroom")
        pairs_ctn = 18
    elif "clogs" in cat_l or "kids" in cat_l:
        ctx_scene = scene_data["General"].replace("warehouse", "garden / light outdoor area")
        pairs_ctn = 24
    else:
        ctx_scene = scene_data["General"]
        pairs_ctn = 12

    # 2. 4-Slot Prompts (Alibaba Photo Guide SOP)
    p1_hero = (
        f"Using the attached reference photos, create a professional e-commerce product photo "
        f"of the exact same {p_color} {clean_name} (SKU: {p_sku}). Keep the product exactly identical to the "
        f"reference: same silhouette, material texture, sole cleats, and brand marking. "
        f"Single product, 3/4 front view standing upright, centered, occupying 85% of frame. "
        f"Pure white seamless background (RGB 255,255,255), crisp studio lighting with subtle natural contact shadow only. "
        f"Square 1:1, sharp focus, 1600x1600. No promotional overlays, no text, no props."
    )

    p2_side = (
        f"Using the attached reference photos, create a product photograph of the exact same "
        f"{p_color} {clean_name} from a clean 90-degree side profile view. Maintain exact proportions, "
        f"shaft height, and heel curve. Pure white seamless background (RGB 255,255,255), even studio lighting, "
        f"centered, occupying 85% of frame, subtle natural ground shadow. Square 1:1, sharp focus, zero text or logos."
    )

    p3_tread = (
        f"Using the attached reference photos, create a product photograph of the exact same "
        f"{p_color} {clean_name} showing the bottom outsole tread pattern and anti-slip cleat structure. "
        f"Show high detail of deep mud-release grooves and slip-resistant rubber texture. "
        f"Pure white background (RGB 255,255,255), professional product studio lighting. Square 1:1, sharp focus."
    )

    p4_context = (
        f"Using the attached reference photos, create a realistic commercial contextual in-use photograph "
        f"of the exact same {p_color} {clean_name} worn by an adult worker in {ctx_scene}. "
        f"Ground-level camera angle focusing on the boots in authentic working conditions. "
        f"Natural realistic lighting, believable environmental texture, true-to-life colors. "
        f"Square 1:1, cinematic high resolution. No artificial text or platform badges."
    )

    # 3. Accio Listing Title & Keywords Generator
    accio_res = generate_accio_listing(
        sku=p_sku,
        product_title=p_title,
        category_group=p_cat,
        preferred_angle=preferred_angle,
        destination_country=destination_country
    )

    # 4. Packaging, Carton & Currency Calculations
    calc_res = calculate_packaging_and_carton(
        price_usd=p_usd,
        pairs_per_carton=pairs_ctn,
        category_group=p_cat
    )

    return {
        "sku": p_sku,
        "product_name": clean_name,
        "category_group": p_cat,
        "color": p_color,
        "source_image": p_img,
        "target_continent": detected_continent,
        "destination_country": destination_country,
        "target_industry_angle": accio_res.get("target_industry_angle", "All-Weather Rain Utility"),
        "optimized_title": accio_res.get("alibaba_product_title", p_title),
        "primary_keywords": [
            accio_res.get("primary_keyword_1", ""),
            accio_res.get("primary_keyword_2", ""),
            accio_res.get("primary_keyword_3", "")
        ],
        "image_prompts": {
            "slot_1_hero": p1_hero,
            "slot_2_side": p2_side,
            "slot_3_tread": p3_tread,
            "slot_4_contextual": p4_context,
            "contextual_scene_description": ctx_scene
        },
        "packaging_and_pricing": calc_res
    }

def run_smart_top_pick_generator(category_filter=None, continent_filter="Europe", destination_country=None, count=3, mode="top_sellers"):
    """
    End-to-end generator:
    1. Picks top products based on category/continent
    2. Builds custom AI image prompts & packaging metrics for each
    3. Returns consolidated batch ready for AI image generator or export
    """
    prods = pick_top_products(
        category_filter=category_filter,
        continent_filter=continent_filter,
        count=count,
        mode=mode
    )

    packages = []
    for p in prods:
        pkg = generate_tailored_product_package(
            product=p,
            destination_country=destination_country,
            target_continent=continent_filter or "Europe"
        )
        packages.append(pkg)

    rate, src, ut = get_live_usd_idr_rate()

    return {
        "success": True,
        "total_picked": len(packages),
        "target_continent": continent_filter,
        "destination_country": destination_country or "Auto (Selected Continent Top Country)",
        "live_exchange_rate": rate,
        "exchange_source": src,
        "rate_updated_at": ut,
        "products": packages
    }
