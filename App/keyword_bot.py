import os
import re
import json
import pandas as pd
import sqlite3

BASE_DIR = r"d:\Work\Hots\Product Input"
MATRIX_PATH = os.path.join(BASE_DIR, "Input", "alibaba-800-listing-matrix.xlsx")
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")
FLAGSHIP_JSON_PATH = os.path.join(BASE_DIR, "App", "flagship_40_data.json")

INDUSTRY_ANGLES = [
    'Agriculture & Farming',
    'Civil Construction',
    'Oil & Gas Refinery',
    'Mining & Quarrying',
    'Fishery & Seafood',
    'Medical & Kitchen Hygiene',
    'Motorcycle & Courier',
    'Chemical & Factory Manufacturing',
    'Wholesale OEM Supply',
    'All-Weather Rain Utility'
]

# Color translation map
COLOR_MAP = {
    r'\bhitam\b': 'Black',
    r'\bputih\b': 'White',
    r'\bhijau\b': 'Green',
    r'\bkuning\b': 'Yellow',
    r'\bcoklat\b|\bcokelat\b': 'Brown',
    r'\bmerah\b': 'Red',
    r'\babu\b|\babu-abu\b': 'Grey',
    r'\bbiru\b': 'Blue',
    r'\borange\b|\boren\b': 'Orange',
    r'\btosca\b': 'Tosca',
    r'\bcream\b|\bkrem\b': 'Cream',
    r'\blime\b': 'Lime Green',
    r'\bpink\b': 'Pink',
    r'\bnavy\b': 'Navy'
}

_CACHED_KEYWORD_DB = None
_CACHED_BASE_PRODUCTS = None
_CACHED_FLAGSHIP_LIST = None
_CACHED_FLAGSHIP_MAP = None

def translate_colors(text):
    if not text:
        return ""
    res = str(text)
    for pat, eng in COLOR_MAP.items():
        res = re.sub(pat, eng, res, flags=re.I)
    return res

def clean_model_name(raw_text):
    """Extracts clean model identifier in English from raw product titles."""
    text = translate_colors(str(raw_text or ''))
    # Remove prefix "AP Boots" or "Sepatu Boot"
    text = re.sub(r'^(ap\s*boots?|sepatu\s*boot?)\s*', '', text, flags=re.I).strip()
    # Remove Indonesian descriptive suffixes
    text = re.split(r'\s*-\s*(sepatu|pvc|boots?|shoes|karet|slip|kets)', text, flags=re.I)[0].strip()
    text = re.sub(r'\s*(sepatu|boot|boots|shoes|pvc|karet|pria|wanita|unisex|motif)\b', '', text, flags=re.I).strip()
    text = re.sub(r'\s+', ' ', text).strip()
    return text if text else "Classic"

def get_flagship_40_list():
    """Returns the list of 40 curated Flagship products from the verified cheatsheet."""
    global _CACHED_FLAGSHIP_LIST, _CACHED_FLAGSHIP_MAP
    if _CACHED_FLAGSHIP_LIST is not None:
        return _CACHED_FLAGSHIP_LIST

    if os.path.exists(FLAGSHIP_JSON_PATH):
        try:
            with open(FLAGSHIP_JSON_PATH, "r", encoding="utf-8") as f:
                _CACHED_FLAGSHIP_LIST = json.load(f)
                _CACHED_FLAGSHIP_MAP = {}
                for it in _CACHED_FLAGSHIP_LIST:
                    sku = it.get('sku', '').strip().upper()
                    if sku:
                        _CACHED_FLAGSHIP_MAP[sku] = it
                    model = it.get('model', '').strip().upper()
                    if model:
                        _CACHED_FLAGSHIP_MAP[model] = it
                return _CACHED_FLAGSHIP_LIST
        except Exception as e:
            print(f"[WARN] Error loading flagship json: {e}")

    _CACHED_FLAGSHIP_LIST = []
    _CACHED_FLAGSHIP_MAP = {}
    return _CACHED_FLAGSHIP_LIST

def get_keyword_matrix():
    """Loads the 810 Alibaba listing matrix keywords from SQLite."""
    global _CACHED_KEYWORD_DB, _CACHED_BASE_PRODUCTS
    if _CACHED_KEYWORD_DB is not None:
        return _CACHED_KEYWORD_DB, _CACHED_BASE_PRODUCTS

    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alibaba_keywords'")
            if cur.fetchone():
                df = pd.read_sql_query("SELECT * FROM alibaba_keywords", conn)
                conn.close()
                if len(df) >= 800:
                    _CACHED_KEYWORD_DB = df
                    _CACHED_BASE_PRODUCTS = sorted(df['Base_Product_Name'].dropna().unique().tolist(), key=len, reverse=True)
                    return _CACHED_KEYWORD_DB, _CACHED_BASE_PRODUCTS
            conn.close()
        except Exception:
            pass

    if os.path.exists(MATRIX_PATH):
        df = pd.read_excel(MATRIX_PATH, sheet_name='Keyword_Manager_Database')
        _CACHED_KEYWORD_DB = df
        _CACHED_BASE_PRODUCTS = sorted(df['Base_Product_Name'].dropna().unique().tolist(), key=len, reverse=True)
        return _CACHED_KEYWORD_DB, _CACHED_BASE_PRODUCTS

    return pd.DataFrame(), []

def generate_b2b_english_title(model_name, category="", angle="Agriculture & Farming", original_title=""):
    """
    Generates professional English Alibaba B2B title matching Alibaba standard formula:
    [Brand] [Model/Color] [Material/Core Feature] [Product Type] [Target Application / Industry] [B2B Wholesale Intent]
    Strictly <= 128 characters!
    """
    clean_model = clean_model_name(model_name or original_title or "AP Boots")
    
    # Ensure brand prefix
    if not clean_model.upper().startswith("AP"):
        brand_model = f"AP Boots {clean_model}"
    else:
        brand_model = clean_model if "BOOTS" in clean_model.upper() else f"AP Boots {clean_model.replace('AP ', '').strip()}"

    combined_lower = f"{brand_model.lower()} {str(category).lower()} {str(original_title).lower()}"
    angle_l = (angle or "").lower()

    # Product Type specific title generators
    if "clogs" in combined_lower or "sandal" in combined_lower or "selop" in combined_lower:
        if "medic" in combined_lower or "hospital" in combined_lower:
            title = f"{brand_model} Cleanroom Medical Protective Clogs Anti-Slip Autoclave Hospital Shoes Wholesale"
        elif "chef" in combined_lower or "koki" in combined_lower or "kitchen" in combined_lower:
            title = f"{brand_model} RubberTech Slip Resistant Kitchen Work Clogs Waterproof Anti-Fatigue Wholesale"
        elif "pink" in combined_lower or "ladies" in combined_lower:
            title = f"{brand_model} Waterproof PVC Slip-On Garden Clogs Lightweight Healthcare Footwear Wholesale"
        else:
            title = f"{brand_model} Waterproof PVC Slip-On Work Clogs Anti-Slip Lightweight Garden Mules Wholesale"

    elif "kets" in combined_lower or "star" in combined_lower or "sneaker" in combined_lower:
        title = f"{brand_model} Waterproof PVC Casual Sneakers Slip-On Walking Shoes Everyday Footwear Wholesale"

    elif "963" in combined_lower or "bola" in combined_lower or "cleat" in combined_lower or "soccer" in combined_lower:
        title = f"{brand_model} Cleated Rubber Football Soccer Shoes Waterproof Anti-Slip Turf Footwear Wholesale"

    elif "medic" in combined_lower:
        title = f"{brand_model} Medical Cleanroom Protective Footwear Anti-Slip Hospital Laboratory Shoes Bulk"

    elif "chef" in combined_lower:
        title = f"{brand_model} Oil Resistant Kitchen Chef Work Shoes Slip-On Waterproof Food Service Wholesale"

    elif "allbike" in combined_lower or "all bike" in combined_lower or "moto" in combined_lower or "biker" in combined_lower or "courier" in angle_l:
        title = f"{brand_model} Waterproof Mid-Calf PVC Motorcycle Riding Boots Slip-On Outdoor Footwear Wholesale"

    elif "orca" in combined_lower or "fishery" in combined_lower or "seafood" in angle_l:
        title = f"{brand_model} Heavy Duty High PVC Rain Boots Waterproof Anti-Slip for Fishery Seafood Supply"

    elif "s5" in combined_lower or "metaguard" in combined_lower or "safety s4" in combined_lower or "steel toe" in combined_lower or "puncture" in combined_lower:
        title = f"{brand_model} Steel Toe Industrial Safety Boots Waterproof PVC Rubber for Mining Construction Bulk"

    elif "white" in combined_lower or "putih" in combined_lower or "hygiene" in angle_l:
        title = f"{brand_model} Waterproof PVC Hygiene Rain Boots Mid-Calf for Food Processing Cleanroom Wholesale"

    elif "kids" in combined_lower or "anak" in combined_lower:
        title = f"{brand_model} Waterproof Anti-Slip Children Rain Boots Durable PVC Cute Outerwear Wholesale"

    elif "terra" in combined_lower or "2003" in combined_lower or "2005" in combined_lower or "2006" in combined_lower or "2015" in combined_lower or "2017" in combined_lower or "2018" in combined_lower or "agriculture" in angle_l:
        title = f"{brand_model} Heavy Duty Waterproof PVC Rain Boots Mid-Calf for Agriculture Plantation Wholesale"

    elif "construction" in angle_l or "civil" in angle_l or "9905" in combined_lower or "9506" in combined_lower:
        title = f"{brand_model} Heavy Duty PVC Safety Boots Mid-Calf Waterproof Anti-Slip for Construction Bulk"

    elif "oil" in angle_l or "gas" in angle_l or "max" in combined_lower:
        title = f"{brand_model} Chemical Proof Industrial Rubber Safety Boots Waterproof for Oil Gas Refinery Bulk"

    elif "mining" in angle_l or "quarry" in angle_l:
        title = f"{brand_model} Heavy Duty Abrasion Resistant Mining Rubber Boots Waterproof for Industrial Site"

    else:
        title = f"{brand_model} High Durability Waterproof PVC Work Rain Boots Mid-Calf Factory Export Supply"

    # Enforce strictly <= 128 characters
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > 128:
        title = title[:125].rstrip() + "..."
    return title

def infer_default_angle(model_or_title=""):
    t_low = (model_or_title or "").lower()
    if "medic" in t_low or "hospital" in t_low or "chef" in t_low or "kitchen" in t_low:
        return 'Medical & Kitchen Hygiene'
    elif "orca" in t_low or "fishery" in t_low or "white" in t_low or "seafood" in t_low:
        return 'Fishery & Seafood'
    elif "all bike" in t_low or "allbike" in t_low or "moto" in t_low or "riding" in t_low or "biker" in t_low:
        return 'Motorcycle & Courier'
    elif "terra" in t_low or "2003" in t_low or "2005" in t_low or "2006" in t_low or "2015" in t_low or "2017" in t_low or "2018" in t_low:
        return 'Agriculture & Farming'
    elif "s5" in t_low or "metaguard" in t_low or "safety" in t_low or "9905" in t_low or "9506" in t_low:
        return 'Civil Construction'
    elif "max" in t_low or "oil" in t_low:
        return 'Oil & Gas Refinery'
    elif "clogs" in t_low or "star" in t_low or "sneaker" in t_low or "sandal" in t_low or "963" in t_low or "kids" in t_low:
        return 'All-Weather Rain Utility'
    else:
        return 'Agriculture & Farming'

def match_product_keywords(title, category="", preferred_angle=None, sku=""):
    """
    Main matching engine:
    1. Checks Flagship 40 Cheatsheet first for exact verified title & keywords.
    2. Otherwise matches against 810 matrix models by model name and industry angle.
    3. Falls back to product-specific B2B English title generator and keyword suite.
    """
    clean_sku = (sku or "").strip().upper()
    get_flagship_40_list()
    global _CACHED_FLAGSHIP_MAP

    # 1. Check Flagship 40 by SKU
    if clean_sku and _CACHED_FLAGSHIP_MAP and clean_sku in _CACHED_FLAGSHIP_MAP:
        f = _CACHED_FLAGSHIP_MAP[clean_sku]
        kws = f['keywords'].split(',')
        p1 = kws[0].strip() if len(kws) > 0 else 'waterproof rain boots'
        p2 = kws[1].strip() if len(kws) > 1 else 'pvc safety boots'
        p3 = kws[2].strip() if len(kws) > 2 else 'wholesale work boots'
        return {
            "matched_base_product": f.get('model', clean_sku),
            "target_industry_angle": preferred_angle or f.get('angle', 'Agriculture & Farming'),
            "primary_keyword_1": p1,
            "primary_keyword_2": p2,
            "primary_keyword_3": p3,
            "longtail_keywords": f['keywords'],
            "keywords": f['keywords'],
            "alibaba_product_title": f['title'],
            "is_flagship": True,
            "flagship_rank": f.get('rank', 1),
            "fixed_price_usd": f.get('price_usd', 5.50),
            "images": f.get('images', [])
        }

    # 2. Extract clean model identifier
    model_name = clean_model_name(title)
    target_angle = preferred_angle or infer_default_angle(f"{model_name} {title}")

    # Check Flagship 40 by Model Name
    if _CACHED_FLAGSHIP_MAP and model_name.upper() in _CACHED_FLAGSHIP_MAP:
        f = _CACHED_FLAGSHIP_MAP[model_name.upper()]
        kws = f['keywords'].split(',')
        return {
            "matched_base_product": f.get('model', model_name),
            "target_industry_angle": preferred_angle or f.get('angle', target_angle),
            "primary_keyword_1": kws[0].strip() if len(kws) > 0 else 'waterproof rain boots',
            "primary_keyword_2": kws[1].strip() if len(kws) > 1 else 'pvc safety boots',
            "primary_keyword_3": kws[2].strip() if len(kws) > 2 else 'wholesale work boots',
            "longtail_keywords": f['keywords'],
            "keywords": f['keywords'],
            "alibaba_product_title": f['title'],
            "is_flagship": True,
            "flagship_rank": f.get('rank', 1),
            "fixed_price_usd": f.get('price_usd', 5.50),
            "images": f.get('images', [])
        }

    # 3. Match against 810 Alibaba Keyword Matrix
    df, base_products = get_keyword_matrix()
    matched_row = None

    if not df.empty:
        # Find closest base product match among the 81 matrix models
        best_bp = None
        for bp in base_products:
            bp_clean = bp.lower().replace('series', '').replace('ap ', '').strip()
            if len(bp_clean) >= 3 and (bp_clean in model_name.lower() or bp_clean in title.lower()):
                best_bp = bp
                break

        if best_bp:
            mask = (df['Base_Product_Name'].str.lower() == best_bp.lower()) & (df['Target_Industry_Angle'].str.lower() == target_angle.lower())
            sub = df[mask]
            if not sub.empty:
                matched_row = sub.iloc[0]
            else:
                mask2 = df['Base_Product_Name'].str.lower() == best_bp.lower()
                sub2 = df[mask2]
                if not sub2.empty:
                    matched_row = sub2.iloc[0]

    # Generate English Alibaba Title tailored to THIS product
    ali_title = generate_b2b_english_title(model_name, category, target_angle, title)

    if matched_row is not None:
        p1 = str(matched_row.get('Primary_Keyword_1', '')).strip()
        p2 = str(matched_row.get('Primary_Keyword_2', '')).strip()
        p3 = str(matched_row.get('Primary_Keyword_3', '')).strip()
        lt = str(matched_row.get('Longtail_Keywords', '')).strip()
        kw_list = [k for k in [p1, p2, p3] if k and k != 'nan']
        combined_kw = ", ".join(kw_list)

        return {
            "matched_base_product": model_name,
            "target_industry_angle": target_angle,
            "primary_keyword_1": p1,
            "primary_keyword_2": p2,
            "primary_keyword_3": p3,
            "longtail_keywords": lt,
            "keywords": combined_kw,
            "alibaba_product_title": ali_title,
            "is_flagship": False,
            "flagship_rank": None
        }

    # 4. Fallback Keyword Suite
    angle_kw_map = {
        'Agriculture & Farming': ("agriculture plantation boots", "farm rubber wellingtons", "waterproof pvc rain boots"),
        'Civil Construction': ("construction safety boots", "heavy duty work wellies", "waterproof site boots"),
        'Oil & Gas Refinery': ("oil gas safety boots", "refinery protective wellingtons", "chemical resistant boots"),
        'Mining & Quarrying': ("mining safety boots", "quarry rubber wellingtons", "heavy duty mining boots"),
        'Fishery & Seafood': ("fishery waterproof boots", "seafood processing boots", "anti slip wet wellingtons"),
        'Medical & Kitchen Hygiene': ("medical cleanroom clogs", "slip resistant chef shoes", "hospital work shoes"),
        'Motorcycle & Courier': ("motorcycle riding boots", "waterproof biker shoes", "courier rain footwear"),
        'Chemical & Factory Manufacturing': ("chemical resistant boots", "acid proof rubber boots", "industrial wellingtons"),
        'Wholesale OEM Supply': ("wholesale pvc rain boots", "factory direct safety shoes", "custom oem boots"),
        'All-Weather Rain Utility': ("all weather rubber boots", "waterproof outdoor clogs", "daily casual rain shoes")
    }
    p1, p2, p3 = angle_kw_map.get(target_angle, ("waterproof rain boots", "pvc safety boots", "wholesale footwear"))

    return {
        "matched_base_product": model_name,
        "target_industry_angle": target_angle,
        "primary_keyword_1": p1,
        "primary_keyword_2": p2,
        "primary_keyword_3": p3,
        "longtail_keywords": f"indonesia factory supply {p1}, durable {p2}, export quality {p3}",
        "keywords": f"{p1}, {p2}, {p3}",
        "alibaba_product_title": ali_title,
        "is_flagship": False,
        "flagship_rank": None
    }
