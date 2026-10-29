"""
AP Boots Alibaba.com Accio Keyword Generator & Listing Optimizer
Based strictly on: Input/AP_Boots_Alibaba_Keyword_Generator_and_SKU_Testing_Guide.md
PT Indo Sukses Semesta (HOTS Trading)
"""

import os
import re
import json
import sqlite3

BASE_DIR = r"d:\Work\Hots\Product Input"
GUIDE_MD_PATH = os.path.join(BASE_DIR, "Input", "AP_Boots_Alibaba_Keyword_Generator_and_SKU_Testing_Guide (1).md")
if not os.path.exists(GUIDE_MD_PATH):
    GUIDE_MD_PATH = os.path.join(BASE_DIR, "Input", "AP_Boots_Alibaba_Keyword_Generator_and_SKU_Testing_Guide.md")

# Standard Accio 10 Industry Angles (Section 6 & 8)
ACCIO_INDUSTRY_ANGLES = [
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

# Section 7: Country-Based Keyword Strategy Markets
ACCIO_DESTINATION_COUNTRIES = [
    {
        "id": "global",
        "name": "Global / General Export",
        "country": "International Markets",
        "buyer_type": "International B2B Importers & Regional Wholesalers",
        "application": "General Commercial & Industrial Footwear Supply",
        "market_note": "Direct container dispatch from Tanjung Priok Seaport, Jakarta, Indonesia."
    },
    {
        "id": "malaysia",
        "name": "Malaysia (Plantation & Agriculture)",
        "country": "Malaysia",
        "buyer_type": "Plantation Estate Procurement & Agrochemical Contractors",
        "application": "Oil Palm Plantation, Estate Agriculture, Drainage Work",
        "market_note": "FOB/CIF port shipment to Port Klang / Penang / Pasir Gudang."
    },
    {
        "id": "australia",
        "name": "Australia (Mining & Civil Construction)",
        "country": "Australia",
        "buyer_type": "Mining Site Contractors & Industrial PPE Distributors",
        "application": "Mining Exploration, Heavy Excavation, Civil Earthworks",
        "market_note": "FOB/CIF sea freight to Fremantle / Brisbane / Sydney. AS/NZS compliance test confirmation pending per contract."
    },
    {
        "id": "philippines",
        "name": "Philippines (Aquaculture, Hardware & Marine)",
        "country": "the Philippines",
        "buyer_type": "Provincial Hardware Importers & Seafood Aquaculture Supply",
        "application": "Commercial Fishery, Seafood Processing, Monsoon Rain Utility",
        "market_note": "Direct container sea freight to Manila / Cebu / Davao ports."
    },
    {
        "id": "vietnam",
        "name": "Vietnam (Commercial Agriculture & Manufacturing)",
        "country": "Vietnam",
        "buyer_type": "Factory Manufacturing Procurement & Agricultural Co-ops",
        "application": "Paddy Agriculture, Food Processing, Light Industrial Assembly",
        "market_note": "Direct sea freight dispatch to Hai Phong / Ho Chi Minh City ports."
    },
    {
        "id": "uae",
        "name": "United Arab Emirates (Construction & Infrastructure)",
        "country": "the United Arab Emirates",
        "buyer_type": "Civil Engineering Contractors & Infrastructure Supply Agencies",
        "application": "Infrastructure Concrete Works, Industrial Utility, Refinery Maintenance",
        "market_note": "Direct container shipping to Jebel Ali Port, Dubai. Local municipality approval confirmation pending."
    }
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

def translate_colors(text):
    if not text:
        return ""
    res = str(text)
    for pat, eng in COLOR_MAP.items():
        res = re.sub(pat, eng, res, flags=re.I)
    return res

def clean_model_name(raw_text):
    text = translate_colors(str(raw_text or ''))
    text = re.sub(r'^(sepatu\s*boots?\s*(tinggi\s*)?(safety\s*)?|petrova\s*-\s*|petrova\s+|ap\s*boots?\s*)', '', text, flags=re.I).strip()
    text = re.split(r'\s*-\s*(sepatu|pvc|boots?|shoes|karet|slip|kets|steel\s*toe|boots\s*air)', text, flags=re.I)[0].strip()
    text = re.split(r'\s+(lentur|lokal|anti\s*slip)', text, flags=re.I)[0].strip()
    text = re.sub(r'\s*(sepatu|boot|boots|shoes|pvc|karet|pria|wanita|unisex|motif|tinggi)\b', '', text, flags=re.I).strip()
    text = re.sub(r'^(petrova|ap)\s*', '', text, flags=re.I).strip()
    text = re.sub(r'\s+', ' ', text).strip()
    return text if text else "Classic"

def classify_accio_sku(sku="", model="", title="", category=""):
    """
    Classifies SKU into strict Accio product category and determines verified facts vs prohibited claims.
    Follows GPSR Batch Compliance PT Waru Gunung (Anti-Overclaim & Geo-Block Prevention).
    """
    comb = f"{sku} {model} {title} {category}".lower()
    is_petrova = "petrova" in comb
    brand = "Petrova" if is_petrova else "AP Boots"
    manufacturer = "PT Waru Gunung"

    # =========================================================================
    # A. PETROVA BRAND CATALOG (Manufactured by PT Waru Gunung)
    # =========================================================================
    if is_petrova:
        # 1. Petrova Strength WB (Water Boots / Non-Steel Toe)
        if "strength wb" in comb or ("strength" in comb and ("wb" in comb or "air" in comb)):
            return {
                "group": "AGRICULTURE_UTILITY",
                "standard": "Internal Factory Standard",
                "certification_status": "NO_CERTIFICATION",
                "has_steel_toe": False,
                "has_steel_midsole": False,
                "is_safety_boot": False,
                "product_type": "Waterproof PVC Work Boots",
                "brand": "Petrova",
                "manufacturer": manufacturer,
                "default_angle": "Agriculture & Farming",
                "prohibited_claims": [
                    "Petrova Strength WB is a general waterproof boot, NOT a steel toe safety boot.",
                    "Do NOT claim EN ISO 20345, CE, or PPE certification without documentation.",
                    "Do NOT claim steel toe impact protection."
                ]
            }

        # 2. Petrova Pro Green (Plantation / Utility)
        if "pro green" in comb or "pro-green" in comb:
            return {
                "group": "AGRICULTURE_UTILITY",
                "standard": "Internal Factory Standard",
                "certification_status": "NO_CERTIFICATION",
                "has_steel_toe": False,
                "has_steel_midsole": False,
                "is_safety_boot": False,
                "product_type": "Flexible PVC Plantation Work Boots",
                "brand": "Petrova",
                "manufacturer": manufacturer,
                "default_angle": "Agriculture & Farming",
                "prohibited_claims": [
                    "Petrova Pro Green must not receive steel toe safety claims.",
                    "Do NOT claim EN ISO 20345 or CE certification without proof."
                ]
            }

        # 3. Petrova Classic (Flexible PVC)
        if "classic" in comb:
            return {
                "group": "AGRICULTURE_UTILITY",
                "standard": "Internal Factory Standard",
                "certification_status": "NO_CERTIFICATION",
                "has_steel_toe": False,
                "has_steel_midsole": False,
                "is_safety_boot": False,
                "product_type": "Flexible PVC Work Boots",
                "brand": "Petrova",
                "manufacturer": manufacturer,
                "default_angle": "Civil Construction",
                "prohibited_claims": [
                    "Petrova Classic is a standard utility boot, not a certified safety boot.",
                    "Do NOT claim steel toe or PPE category certification."
                ]
            }

        # 4. Petrova Nelayan (Fishery with Steel Toe Cap Anti Static)
        if "nelayan" in comb:
            return {
                "group": "FISHERY_SEAFOOD",
                "standard": "Factory Steel Toe Standard",
                "certification_status": "FACTORY_STANDARD",
                "has_steel_toe": True,
                "has_steel_midsole": False,
                "is_safety_boot": True,
                "product_type": "Fishery Safety Boots with Steel Toe",
                "brand": "Petrova",
                "manufacturer": manufacturer,
                "default_angle": "Fishery & Seafood",
                "prohibited_claims": [
                    "Do not claim CE/EN ISO certification without accredited lab test report.",
                    "Klaim steel toe cap impact resistance diizinkan, tetapi jangan mengklaim sertifikat Uni Eropa tanpa bukti."
                ]
            }

        # 5. Petrova Ultimate (Industrial Steel Toe Cap Anti Static)
        if "ultimate" in comb:
            return {
                "group": "VERIFIED_SAFETY",
                "standard": "Factory Steel Toe Standard",
                "certification_status": "FACTORY_STANDARD",
                "has_steel_toe": True,
                "has_steel_midsole": True,
                "is_safety_boot": True,
                "product_type": "Industrial Steel Toe Safety Boots",
                "brand": "Petrova",
                "manufacturer": manufacturer,
                "default_angle": "Civil Construction",
                "prohibited_claims": [
                    "Do not claim CE/ASTM without SKU-specific test certificate.",
                    "Highlight physical steel toe and anti-static sole without unverified European CE logos."
                ]
            }

        # 6. Petrova Phenom (Industrial Steel Toe Anti Static)
        if "phenom" in comb:
            return {
                "group": "VERIFIED_SAFETY",
                "standard": "Factory Steel Toe Standard",
                "certification_status": "FACTORY_STANDARD",
                "has_steel_toe": True,
                "has_steel_midsole": True,
                "is_safety_boot": True,
                "product_type": "Anti-Static Steel Toe Safety Boots",
                "brand": "Petrova",
                "manufacturer": manufacturer,
                "default_angle": "Oil & Gas Refinery",
                "prohibited_claims": [
                    "Do not claim CE/ASTM without SKU-specific test certificate."
                ]
            }

        # 7. Petrova Ergos (Steel Toe PVC)
        if "ergos" in comb:
            return {
                "group": "VERIFIED_SAFETY",
                "standard": "Factory Steel Toe Standard",
                "certification_status": "FACTORY_STANDARD",
                "has_steel_toe": True,
                "has_steel_midsole": False,
                "is_safety_boot": True,
                "product_type": "Ergonomic Steel Toe Work Boots",
                "brand": "Petrova",
                "manufacturer": manufacturer,
                "default_angle": "Civil Construction",
                "prohibited_claims": [
                    "Do not claim CE/ASTM without SKU-specific test certificate."
                ]
            }

        # 8. Petrova Strength Safety (Steel Toe PVC)
        if "strength" in comb:
            return {
                "group": "VERIFIED_SAFETY",
                "standard": "Factory Steel Toe Standard",
                "certification_status": "FACTORY_STANDARD",
                "has_steel_toe": True,
                "has_steel_midsole": False,
                "is_safety_boot": True,
                "product_type": "Heavy Duty Steel Toe Safety Boots",
                "brand": "Petrova",
                "manufacturer": manufacturer,
                "default_angle": "Civil Construction",
                "prohibited_claims": [
                    "Do not claim CE/ASTM without SKU-specific test certificate."
                ]
            }

    # =========================================================================
    # B. AP BOOTS BRAND CATALOG (Manufactured by PT Waru Gunung)
    # =========================================================================

    # 1. Verified Safety: S4, Metaguard, S5, Terra Safety with steel toe
    if any(k in comb for k in ["s5", "metaguard", "s4", "steel toe", "steel midsole"]):
        return {
            "group": "VERIFIED_SAFETY",
            "standard": "EN ISO 20345",
            "certification_status": "VERIFIED",
            "has_steel_toe": True,
            "has_steel_midsole": True,
            "is_safety_boot": True,
            "product_type": "Safety Boots",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "Civil Construction",
            "prohibited_claims": [
                "Do not claim certification for other non-safety SKUs in the catalog.",
                "Do not claim CE/ASTM without SKU-specific test certificate."
            ]
        }

    # 2. Unverified Safety: AP Max
    if "max" in comb and ("ap max" in comb or "boots max" in comb or comb.startswith("max") or "ap-max" in comb):
        return {
            "group": "UNVERIFIED_SAFETY",
            "standard": "Internal Factory Standard",
            "certification_status": "CERTIFICATION_PENDING",
            "has_steel_toe": False,
            "has_steel_midsole": False,
            "is_safety_boot": False,  # MUST NOT CLAIM EN ISO OR SAFETY BOOT UNTIL CONFIRMED
            "product_type": "Industrial Work Boots",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "Oil & Gas Refinery",
            "prohibited_claims": [
                "AP Max must NOT carry EN ISO 20345 certification claims until written WGI factory confirmation is available.",
                "Do not describe as steel toe boots."
            ]
        }

    # 3. Hospitality / Kitchen: AP Chef
    if "chef" in comb or "koki" in comb:
        return {
            "group": "KITCHEN_HOSPITALITY",
            "standard": "None",
            "certification_status": "NO_CERTIFICATION",
            "has_steel_toe": False,
            "has_steel_midsole": False,
            "is_safety_boot": False,
            "product_type": "Kitchen Chef Work Shoes",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "Medical & Kitchen Hygiene",
            "prohibited_claims": [
                "AP Chef is marked as having NO certification in approved sources.",
                "Do NOT claim HACCP, CE, autoclave, or EN ISO standards.",
                "Do NOT describe as safety toe boots."
            ]
        }

    # 4. Workplace Hygiene / Cleanroom: AP Medic (COMPLIANCE: Anti-Overclaim Medical Device)
    if "medic" in comb or "hospital" in comb:
        return {
            "group": "WORKPLACE_HYGIENE",
            "standard": "Internal Factory Standard",
            "certification_status": "NO_CERTIFICATION",
            "has_steel_toe": False,
            "has_steel_midsole": False,
            "is_safety_boot": False,
            "product_type": "PVC Anti-Slip Work Shoes",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "Medical & Kitchen Hygiene",
            "prohibited_claims": [
                "GPSR Anti-Overclaim Rule: Do NOT write Medical, Medical Device, Hospital, Surgical, Clinical, Healthcare, Sterile, or FDA.",
                "Do NOT claim medical device registration or CE medical device status.",
                "Position strictly as PVC Anti-Slip Work Shoes for General Workplace Hygiene."
            ]
        }

    # 5. Fishery & Marine: AP Orca
    if "orca" in comb or "fishery" in comb:
        return {
            "group": "FISHERY_SEAFOOD",
            "standard": "None",
            "certification_status": "NO_CERTIFICATION",
            "has_steel_toe": False,
            "has_steel_midsole": False,
            "is_safety_boot": False,
            "product_type": "High Waterproof Rain Boots",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "Fishery & Seafood",
            "prohibited_claims": [
                "Orca lines must not receive safety certification claims without documentation.",
                "Do not label as steel toe boots."
            ]
        }

    # 6. Motorcycle & Commuting: AP Allbike, AP Moto, AP Biker (COMPLIANCE: Splash Protection Only)
    if any(k in comb for k in ["allbike", "all bike", "moto", "biker", "riding"]):
        return {
            "group": "MOTORCYCLE_COURIER",
            "standard": "None",
            "certification_status": "NO_CERTIFICATION",
            "has_steel_toe": False,
            "has_steel_midsole": False,
            "is_safety_boot": False,
            "product_type": "Water-Resistant Motorcycle Shoe Covers",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "Motorcycle & Courier",
            "prohibited_claims": [
                "GPSR Compliance Rule: Do NOT claim PPE (Personal Protective Equipment) for motorcycle crash protection.",
                "Position strictly as Water-Resistant Motorcycle Shoe Covers for General Outdoor Splash Protection Only."
            ]
        }

    # 7. Kids & Rainwear: AP Kids, AP Safari, AP Fun
    if any(k in comb for k in ["kids", "safari", "anak", "fun"]):
        return {
            "group": "KIDS_RAIN",
            "standard": "None",
            "certification_status": "NO_CERTIFICATION",
            "has_steel_toe": False,
            "has_steel_midsole": False,
            "is_safety_boot": False,
            "product_type": "Children's Rain Boots",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "All-Weather Rain Utility",
            "prohibited_claims": [
                "Kids lines must not receive safety certification claims."
            ]
        }

    # 8. Football / Sports Cleats: AP Bola 963
    if any(k in comb for k in ["bola", "963", "cleat", "soccer", "sepak"]):
        return {
            "group": "FOOTBALL_CLEATS",
            "standard": "None",
            "certification_status": "NO_CERTIFICATION",
            "has_steel_toe": False,
            "has_steel_midsole": False,
            "is_safety_boot": False,
            "product_type": "Molded Cleated Football Boots",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "All-Weather Rain Utility",
            "prohibited_claims": [
                "Football series must not receive industrial safety claims."
            ]
        }

    # 9. Casual / Clogs / Star / Vantopel
    if any(k in comb for k in ["clog", "sandal", "selop", "star", "kets", "sneaker", "vantopel", "hobby"]):
        return {
            "group": "CASUAL_CLOGS",
            "standard": "None",
            "certification_status": "NO_CERTIFICATION",
            "has_steel_toe": False,
            "has_steel_midsole": False,
            "is_safety_boot": False,
            "product_type": "Slip-On Utility Clogs",
            "brand": "AP Boots",
            "manufacturer": manufacturer,
            "default_angle": "All-Weather Rain Utility",
            "prohibited_claims": [
                "Casual and Vantopel lines must not receive industrial safety certification claims."
            ]
        }

    # 10. Agriculture & Utility: Terra Series, AP 2003, 2005, 2006, 2015, 2017, 2018, XT, Roots n Leaves
    return {
        "group": "AGRICULTURE_UTILITY",
        "standard": "None",
        "certification_status": "NO_CERTIFICATION",
        "has_steel_toe": False,
        "has_steel_midsole": False,
        "is_safety_boot": False,  # Crucial rule: Terra & AP 2017 are utility/rain boots, not safety boots
        "product_type": "Waterproof Work Boots",
        "brand": brand,
        "manufacturer": manufacturer,
        "default_angle": "Agriculture & Farming",
        "prohibited_claims": [
            "Do not call a non-safety product a safety boot unless safety protection and certification are verified.",
            "Terra and general utility lines must not receive EN ISO 20345 claims."
        ]
    }

def generate_accio_keywords_formula(info, model_name="", angle="Agriculture & Farming", destination_country=None):
    """
    Implements Section 5 of Guide:
    1 Core Product Keyword
    3 Feature Keywords
    2 Material Keywords
    2 Application Keywords
    2 Buyer-Intent Keywords
    2 Customization Keywords (Conditional)
    3 Related Search Terms
    """
    grp = info["group"]
    angle_l = (angle or "").lower()

    if grp == "VERIFIED_SAFETY":
        core = "EN ISO 20345 safety boots"
        features = ["200J steel toe cap", "steel midsole puncture protection", "waterproof leak-resistant construction"]
        materials = ["PVC safety boots", "seamless injection molded"]
        applications = ["mining work boots", "construction site footwear"]
        buyer_intent = ["wholesale safety boots", "distributor supply"]
        customization = ["custom packaging available subject to MOQ", "private label inquiry subject to factory approval"]
        related = ["protective rain boots", "heavy duty work boots", "industrial rubber boots"]

    elif grp == "UNVERIFIED_SAFETY":
        core = "industrial work boots"
        features = ["oil-resistant outsole", "waterproof leak-resistant", "anti-slip heavy-duty tread"]
        materials = ["chemical-resistant PVC upper", "injection molded polymer"]
        applications = ["oil and gas refinery", "chemical plant work"]
        buyer_intent = ["wholesale industrial boots", "B2B supplier partner"]
        customization = ["custom logo option subject to MOQ", "custom packaging inquiry upon request"]
        related = ["heavy-duty work boots", "protective rain footwear", "refinery wellingtons"]

    elif grp == "KITCHEN_HOSPITALITY":
        core = "chef work boots"
        features = ["oil-resistant anti-slip outsole", "waterproof easy-clean surface", "anti-fatigue comfort footbed"]
        materials = ["hygienic PVC upper", "nitrile rubber slip-resistant sole"]
        applications = ["commercial kitchen", "food processing plant"]
        buyer_intent = ["hospitality wholesale supply", "restaurant footwear distributor"]
        customization = ["custom carton packaging available subject to MOQ", "private label inquiry subject to approval"]
        related = ["kitchen work shoes", "catering clogs", "food service boots"]

    elif grp == "MEDICAL_CLEANROOM":
        core = "medical work clogs"
        features = ["anti-slip outsole", "easy-clean fluid resistant surface", "lightweight flexible comfort"]
        materials = ["seamless injection molded PVC", "non-porous hygienic polymer"]
        applications = ["hospital and clinic", "cleanroom laboratory"]
        buyer_intent = ["healthcare wholesale supply", "medical distributor footwear"]
        customization = ["custom packaging inquiry subject to MOQ", "private label options subject to approval"]
        related = ["hospital clogs", "cleanroom shoes", "medical work footwear"]

    elif grp == "FISHERY_SEAFOOD":
        core = "waterproof rain boots"
        features = ["extra-high shaft protection", "anti-slip wet floor tread", "saline water leak-resistant"]
        materials = ["heavy-duty PVC upper", "durable rubberized sole"]
        applications = ["fishery and aquaculture", "seafood processing market"]
        buyer_intent = ["wholesale bulk supply", "distributor supply partner"]
        customization = ["custom packaging subject to approval", "private label inquiry subject to MOQ"]
        related = ["rubber wellington boots", "commercial fishing boots", "high rain boots"]

    elif grp == "MOTORCYCLE_COURIER":
        core = "motorcycle riding boots"
        features = ["waterproof slip-on construction", "gear-shift traction outsole", "flexible ankle comfort"]
        materials = ["durable PVC upper", "one-piece seamless molded"]
        applications = ["motorcycle delivery fleet", "daily monsoon courier commute"]
        buyer_intent = ["wholesale motorcycle gear", "fleet supplier bulk"]
        customization = ["custom logo branding subject to MOQ", "carton packaging customization"]
        related = ["courier rain shoes", "biker waterproof boots", "outdoor riding footwear"]

    elif grp == "KIDS_RAIN":
        core = "children's rain boots"
        features = ["lightweight flexible construction", "anti-slip grooved sole", "easy pull-on handles"]
        materials = ["soft PVC waterproof upper", "non-toxic injection molded"]
        applications = ["school rainy-season walk", "outdoor muddy playground"]
        buyer_intent = ["wholesale kids footwear", "retail distributor supply"]
        customization = ["custom cartoon packaging subject to MOQ", "custom color batches upon request"]
        related = ["toddler rain boots", "waterproof kids wellies", "cute children boots"]

    elif grp == "FOOTBALL_CLEATS":
        core = "cleated football boots"
        features = ["molded cleat traction studs", "waterproof one-piece body", "abrasion-resistant muddy grip"]
        materials = ["synthetic rubber upper", "molded PVC cleated sole"]
        applications = ["muddy field sports", "outdoor turf recreation"]
        buyer_intent = ["wholesale sports footwear", "bulk athletic supplier"]
        customization = ["custom packaging available subject to MOQ", "custom branding subject to approval"]
        related = ["rubber soccer boots", "turf football shoes", "outdoor cleated boots"]

    elif grp == "CASUAL_CLOGS":
        core = "slip-on utility clogs"
        features = ["lightweight ergonomic footbed", "anti-slip water channel tread", "easy-clean washable surface"]
        materials = ["injection molded polymer", "flexible PVC upper"]
        applications = ["garden work utility", "indoor casual footwear"]
        buyer_intent = ["wholesale footwear supply", "importer bulk supply"]
        customization = ["private label inquiries subject to approval", "custom carton packaging subject to MOQ"]
        related = ["waterproof mules", "gardening slip-ons", "casual rain shoes"]

    else: # AGRICULTURE_UTILITY
        core = "waterproof work boots"
        features = ["self-cleaning mud tread", "100% leak-resistant construction", "anti-slip durable outsole"]
        materials = ["heavy-duty PVC upper", "seamless injection molded"]
        applications = ["agriculture and plantation", "farm drainage outdoor work"]
        buyer_intent = ["wholesale bulk supply", "distributor partner supply"]
        customization = ["custom packaging available subject to MOQ", "private label inquiry subject to approval"]
        related = ["farm rubber boots", "plantation work wellies", "protective rain boots"]

    # Assemble comma-separated Alibaba keywords string
    p1 = f"{info['product_type'].lower()} {materials[0]}"
    p2 = f"{features[0]} {applications[0]}"
    p3 = f"{buyer_intent[0]}"

    # Section 7: Source-Country Keyword Layer (Indonesia Origin)
    source_country_keywords = [
        "Indonesia safety boots supplier" if grp == "VERIFIED_SAFETY" else "Indonesia waterproof work boots",
        "Jakarta B2B footwear supplier",
        "Indonesian industrial footwear supplier" if grp in ["VERIFIED_SAFETY", "UNVERIFIED_SAFETY"] else "Indonesia rubber boots B2B supplier",
        "Indonesia OEM footwear partner",
        "Surabaya safety boots supply" if grp == "VERIFIED_SAFETY" else "Indonesia ODM rubber boots project"
    ]

    # Section 7: Destination-Country Keyword Layer
    dest_name = (destination_country or "").strip().lower()
    destination_country_keywords = []
    selected_dest_info = None

    for c in ACCIO_DESTINATION_COUNTRIES:
        if c["id"] != "global" and (c["id"] in dest_name or c["country"].lower() in dest_name):
            selected_dest_info = c
            break

    if selected_dest_info:
        c_name = selected_dest_info["country"]
        c_app = selected_dest_info["application"]
        destination_country_keywords = [
            f"{core} for {selected_dest_info['id']} plantation projects in {c_name}" if "malaysia" in c_name.lower() else f"{core} for {c_app.split(',')[0]} in {c_name}",
            f"{info['product_type'].lower()} wholesale supplier for {c_name} buyers",
            f"{core} export supply to {c_name} subject to shipping and compliance confirmation"
        ]
    elif dest_name and dest_name not in ["global", "none", "auto"]:
        destination_country_keywords = [
            f"{core} for industrial projects in {destination_country}",
            f"{info['product_type'].lower()} wholesale supplier for {destination_country} buyers",
            f"{core} export supply to {destination_country} subject to compliance confirmation"
        ]
    else:
        destination_country_keywords = [
            f"{core} international wholesale export from Indonesia",
            f"{info['product_type'].lower()} B2B supplier for global importers"
        ]

    # Combine keywords including source country anchor
    combined_str = f"{p1}, {p2}, {p3}, {core}, {source_country_keywords[0]}, {source_country_keywords[1]}"
    if destination_country_keywords:
        combined_str += f", {destination_country_keywords[0]}"

    return {
        "primary_keyword": p1,
        "secondary_keyword": p2,
        "third_keyword": p3,
        "core_keyword": core,
        "feature_keywords": features,
        "material_keywords": materials,
        "application_keywords": applications,
        "buyer_intent_keywords": buyer_intent,
        "customization_keywords": customization,
        "related_search_terms": related,
        "source_country_keywords": source_country_keywords,
        "destination_country_keywords": destination_country_keywords,
        "destination_country": destination_country or "Global / General",
        "country_compliance_notes": "Export supply subject to destination country compliance, local labeling, and shipping confirmation.",
        "country_prohibited_claims": [
            "Do not claim local stock, local warehouse, local service, or fast delivery unless confirmed.",
            "Do not claim country-specific certification or import compliance without documentation.",
            "HOTS Trading should normally use terms such as B2B supplier, export supply partner, or authorized distributor rather than claiming direct factory ownership unless verified."
        ],
        "alibaba_keywords_string": combined_str
    }

def generate_accio_title_options(info, model_name, kw_data, angle="Agriculture & Farming", destination_country=None):
    """
    Implements Section 6, 7 & 10 of Guide & GPSR Batch Compliance PT Waru Gunung:
    Creates 3 distinct compliant title variations matching Alibaba B2B intent:
    - Option 1: Standard [Product Type] + [Main Feature] + [Application] + [Buyer Intent]
    - Option 2: Destination-Country / Project Focus (Section 7)
    - Option 3: Source-Country / Export Partner Focus (Section 7)
    Must be strictly <= 128 characters!
    """
    clean_mod = clean_model_name(model_name)
    brand = info.get("brand") or ("Petrova" if "petrova" in f"{clean_mod} {model_name}".lower() else "AP Boots")
    if brand == "Petrova":
        brand_prefix = f"Petrova {clean_mod}" if not clean_mod.upper().startswith("PETROVA") else clean_mod
    else:
        brand_prefix = f"AP Boots {clean_mod}" if not clean_mod.upper().startswith("AP") else clean_mod

    grp = info["group"]

    dest_str = (destination_country or "").strip()
    dest_is_valid = dest_str and dest_str.lower() not in ["global", "none", "auto", "general"]

    opt1 = ""
    opt2 = ""
    opt3 = ""

    if grp == "VERIFIED_SAFETY":
        opt1 = f"{brand_prefix} Steel Toe Safety Boots with Impact Cap for Industrial Construction Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Steel Toe Work Boots for {dest_str} Mining Infrastructure Wholesale"
        else:
            opt2 = f"{brand_prefix} Waterproof Industrial Safety Boots with Steel Toe for Distributors"
        opt3 = f"Indonesia Safety Footwear Supplier {brand_prefix} Steel Toe Cap for Industrial Bulk Supply"

    elif grp == "UNVERIFIED_SAFETY":
        opt1 = f"{brand_prefix} Heavy Duty Industrial Work Boots with Oil Resistant Sole for Refinery Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Industrial Work Boots with Oil Resistant Sole for {dest_str} Factory Bulk"
        else:
            opt2 = f"{brand_prefix} Water-Resistant PVC Work Boots for Chemical Plant Factory Bulk"
        opt3 = f"Indonesia Footwear Supplier {brand_prefix} Heavy Duty Work Rain Boots Wholesale"

    elif grp == "KITCHEN_HOSPITALITY":
        opt1 = f"{brand_prefix} Oil Resistant Kitchen Chef Work Shoes with Anti-Slip Sole for Food Service Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Anti-Slip Kitchen Work Shoes for {dest_str} Food Service Catering Bulk"
        else:
            opt2 = f"{brand_prefix} Waterproof Slip-On Kitchen Work Shoes for Commercial Catering Bulk"
        opt3 = f"Indonesia Footwear Supplier {brand_prefix} Anti-Fatigue Slip-Resistant Work Shoes Distributors"

    elif grp in ["WORKPLACE_HYGIENE", "MEDICAL_CLEANROOM"]:
        opt1 = f"{brand_prefix} Anti-Slip Workplace Hygiene Clogs for Commercial Cleanroom Food Service Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Slip-On Workplace Shoes for {dest_str} Commercial Hygiene Utility Bulk"
        else:
            opt2 = f"{brand_prefix} Waterproof Slip-On Workplace Hygiene Shoes for Commercial Facility Bulk"
        opt3 = f"Indonesia Footwear Supplier {brand_prefix} Anti-Slip Workplace Utility Clogs Wholesale"

    elif grp == "FISHERY_SEAFOOD":
        if info.get("has_steel_toe"):
            opt1 = f"{brand_prefix} Fishery Safety Boots with Steel Toe Cap for Seafood Aquaculture Wholesale"
            if dest_is_valid:
                opt2 = f"{brand_prefix} Anti-Static Steel Toe Fishery Boots for {dest_str} Marine Bulk"
            else:
                opt2 = f"{brand_prefix} Waterproof Marine Safety Boots with Impact Toe for Distributors"
            opt3 = f"Indonesia Footwear Supplier {brand_prefix} Fishery Steel Toe Boots Distributors"
        else:
            opt1 = f"{brand_prefix} High Waterproof PVC Rain Boots with Anti-Slip Outsole for Fishery Seafood Wholesale"
            if dest_is_valid:
                opt2 = f"{brand_prefix} High Waterproof PVC Rain Boots for {dest_str} Fishery Seafood Bulk"
            else:
                opt2 = f"{brand_prefix} Heavy Duty Waterproof Wet Floor Boots for Seafood Aquaculture Bulk"
            opt3 = f"Indonesia Footwear Supplier {brand_prefix} Deep Lug Traction Rain Boots for Seafood Importers"

    elif grp == "MOTORCYCLE_COURIER":
        opt1 = f"{brand_prefix} Water-Resistant Motorcycle Shoe Covers for Outdoor Courier Utility Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Water-Resistant Outdoor Footwear for {dest_str} Courier Delivery Bulk"
        else:
            opt2 = f"{brand_prefix} Reusable Motorcycle Shoe Covers Splash Protection for Daily Commute Bulk"
        opt3 = f"Indonesia Footwear Supplier {brand_prefix} Splash Protection Shoe Covers Wholesale"

    elif grp == "KIDS_RAIN":
        opt1 = f"{brand_prefix} Waterproof Anti-Slip Children Rain Boots with Flexible Sole for School Outdoor Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Waterproof Children Rain Boots for {dest_str} School Retail Bulk"
        else:
            opt2 = f"{brand_prefix} Lightweight Cute Kids Rain Boots Waterproof Slip-On for Playground Bulk"
        opt3 = f"Indonesia Footwear Supplier {brand_prefix} Durable PVC Children Waterproof Outerwear Boots"

    elif grp == "FOOTBALL_CLEATS":
        opt1 = f"{brand_prefix} Molded Cleated Rubber Football Boots with Turf Traction Studs for Muddy Field Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Cleated Rubber Football Boots for {dest_str} Muddy Turf Athletic Bulk"
        else:
            opt2 = f"{brand_prefix} Waterproof Cleated Soccer Boots for Muddy Field Athletic Bulk"
        opt3 = f"Indonesia Footwear Supplier {brand_prefix} Heavy Duty Turf Football Shoes Distributors"

    elif grp == "CASUAL_CLOGS":
        opt1 = f"{brand_prefix} Lightweight Slip-On Waterproof PVC Work Clogs with Anti-Slip Sole for Garden Utility Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Slip-On Waterproof Work Clogs for {dest_str} Utility Garden Bulk"
        else:
            opt2 = f"{brand_prefix} Waterproof Casual Slip-On Mules Shoes for Everyday Outdoor Bulk"
        opt3 = f"Indonesia Footwear Supplier {brand_prefix} Comfortable Waterproof Work Clogs Distributors"

    else: # AGRICULTURE_UTILITY
        opt1 = f"{brand_prefix} Waterproof PVC Work Boots with Self-Cleaning Mud Tread for Agriculture Plantation Wholesale"
        if dest_is_valid:
            opt2 = f"{brand_prefix} Waterproof PVC Work Boots for {dest_str} Plantation Farm Bulk Supply"
        else:
            opt2 = f"{brand_prefix} Heavy Duty Waterproof Work Rain Boots for Farm Plantation Bulk Supply"
        opt3 = f"Indonesia Footwear Supplier {brand_prefix} Leak-Resistant PVC Utility Work Boots Wholesale"

    # Enforce strictly <= 128 chars on each
    opts = []
    raw_list = [opt2, opt1, opt3] if dest_is_valid else [opt1, opt2, opt3]
    for raw in raw_list:
        cleaned = re.sub(r'\s+', ' ', raw).strip()
        if len(cleaned) > 128:
            cleaned = cleaned[:125].rstrip() + "..."
        opts.append(cleaned)

    return opts

def generate_accio_html_description(info, model_name, titles, kw_data, price_usd=5.50, weight_kg=1.7, sku="", destination_country=None):
    """
    Generates strict Accio-compliant B2B HTML description adhering to GPSR Batch Compliance PT Waru Gunung:
    - Legal Manufacturer (PT Waru Gunung) & Export Supply Partner (PT Indo Sukses Semesta)
    - GPSR Section 6: Mandatory Safety Information Box (Standardized Safety Instructions)
    - GPSR Section 11: Safe B2B Compliance & Anti-Overclaim General Use Disclaimer
    - Fact-checked Toe Protection (Steel Toe vs Plain Toe)
    - Verified Certification matrix & Safe conditional OEM/ODM disclaimer (Section 9.4)
    - Real Export Logistics (Tanjung Priok Jakarta & Tanjung Perak Surabaya)
    """
    clean_mod = clean_model_name(model_name)
    brand_title = titles[0]
    grp = info["group"]
    brand = info.get("brand") or ("Petrova" if "petrova" in f"{clean_mod} {model_name} {brand_title}".lower() else "AP Boots")
    cert_status = info["certification_status"]
    has_steel_toe = info.get("has_steel_toe", False)
    has_steel_midsole = info.get("has_steel_midsole", False)

    toe_protection_text = "Steel Toe Cap (Impact Resistant)" if has_steel_toe else "Reinforced Plain Toe (Non-Safety Utility)"
    midsole_text = "Steel Midsole (Puncture Resistant)" if has_steel_midsole else "Solid Flexible PVC Sole"

    dest_str = (destination_country or "").strip()
    dest_display = dest_str if dest_str and dest_str.lower() not in ["global", "none", "auto", "general"] else "International Trade Corridors (ASEAN, Australia, Middle East & Worldwide)"

    if cert_status == "VERIFIED":
        cert_display = "Verified Factory Steel Toe Standard (Industrial Heavy Duty)"
        cert_badge_color = "#16a34a"
    elif cert_status == "FACTORY_STANDARD":
        cert_display = "Factory Tested Steel Toe Standard (Subject to Sample Approval)"
        cert_badge_color = "#0284c7"
    elif cert_status == "CERTIFICATION_PENDING":
        cert_display = "Internal Factory QC Standard (Third-Party Testing Pending)"
        cert_badge_color = "#d97706"
    else:
        cert_display = "Standard Factory Export Grade (General Industrial / Utility)"
        cert_badge_color = "#64748b"

    html = f"""<div style="font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; color: #1e293b; line-height: 1.6; max-width: 960px; margin: 0 auto;">
    <!-- HEADER BRANDING -->
    <div style="background: linear-gradient(135deg, #0f172a, #1e3a8a, #0284c7); color: #ffffff; padding: 22px 26px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="margin: 0 0 6px 0; font-size: 20px; font-weight: 700; letter-spacing: 0.5px;">{brand.upper()}® — OFFICIAL B2B EXPORT LISTING</h2>
        <p style="margin: 0; font-size: 13px; opacity: 0.95;">Legal Manufacturer: <strong>PT Waru Gunung</strong> (Surabaya, Indonesia) | Export Partner: <strong>PT Indo Sukses Semesta</strong> (HOTS Trading)</p>
    </div>

    <!-- PRODUCT OVERVIEW -->
    <div style="margin-bottom: 20px;">
        <h3 style="font-size: 16.5px; color: #0f172a; border-left: 4px solid #0284c7; padding-left: 10px; margin-bottom: 10px;">Product Overview: {brand_title}</h3>
        <p style="font-size: 13.5px; color: #334155; margin-bottom: 10px;">
            The <strong>{brand_title}</strong> (Model Ref: <code>{sku or clean_mod}</code>) is manufactured by <strong>PT Waru Gunung</strong> utilizing high-pressure monolithic injection molding technology. Designed for intensive industrial, agricultural, and commercial operations, this footwear delivers reliable waterproof integrity, oil-resistant flexibility, and rugged traction.
        </p>
    </div>

    <!-- GPSR SECTION 11: SAFE B2B COMPLIANCE & ANTI-OVERCLAIM DISCLAIMER -->
    <div style="background-color: #f1f5f9; border-left: 4px solid #475569; border-radius: 6px; padding: 14px 18px; margin-bottom: 20px; font-size: 12px; color: #334155; line-height: 1.55;">
        <p style="margin: 0 0 6px 0; font-weight: 700; color: #0f172a;">Compliance & Anti-Overclaim Notice (GPSR Aligned):</p>
        <p style="margin: 0 0 6px 0;">This product is supplied for general workplace and industrial use according to the specifications stated in this listing. Product performance depends on application and operating conditions. Buyers should review technical specifications, safety data, and inspect physical samples before placing bulk orders.</p>
        <p style="margin: 0;">The product is not represented as a medical device or certified PPE under EU/UK/US regulations unless the specific certificate and declaration are formally provided for the exact model and destination market. Do not use for chemical, electrical, extreme thermal, or biological protection unless expressly tested and documented.</p>
    </div>

    <!-- GPSR SECTION 6: MANDATORY SAFETY INFORMATION -->
    <div style="background-color: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 16px 20px; margin-bottom: 20px;">
        <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #b45309; font-weight: 700; display: flex; align-items: center; gap: 6px;">
            <span>⚠️</span> Mandatory Safety Information & Usage Restrictions
        </h4>
        <ul style="margin: 0; padding-left: 20px; font-size: 12.5px; color: #78350f; line-height: 1.55;">
            <li style="margin-bottom: 4px;"><strong>Pre-Use Inspection:</strong> Inspect the product before each use. Do not use if torn, cracked, punctured, deformed, or damaged.</li>
            <li style="margin-bottom: 4px;"><strong>Scope of Utility:</strong> Designed for general industrial and utility use unless a verified protection standard is documented.</li>
            <li style="margin-bottom: 4px;"><strong>Non-Medical Device:</strong> This product is NOT a medical device and is not intended to diagnose, treat, cure, or prevent any illness.</li>
            <li style="margin-bottom: 4px;"><strong>Non-Certified PPE Disclaimer:</strong> Not certified as PPE unless applicable documentation is issued for the exact SKU.</li>
            <li style="margin-bottom: 4px;"><strong>Hazard Limitation:</strong> Keep away from open flames, concentrated acids/alkalis, high-voltage electricity, and sharp penetrations unless certified.</li>
            <li style="margin-bottom: 4px;"><strong>Storage & Care:</strong> Store in a cool, dry place away from direct sunlight and aggressive chemicals. Clean with mild soapy water.</li>
            <li style="margin-bottom: 0;"><strong>Sample Approval:</strong> Performance may vary with operational conditions. Buyers must evaluate physical samples before volume deployment.</li>
        </ul>
    </div>

    <!-- SECTION 7: SOURCE & DESTINATION COUNTRY LOGISTICS -->
    <div style="background-color: #f8fafc; border-left: 4px solid #0284c7; border-radius: 6px; padding: 14px 18px; margin-bottom: 20px; font-size: 12.5px; color: #334155;">
        <h4 style="margin: 0 0 8px 0; font-size: 14px; color: #0f172a; display: flex; align-items: center; gap: 6px;">
            <span>🌏</span> Source Origin & Export Supply Logistics
        </h4>
        <p style="margin: 0 0 6px 0;">• <strong>Legal Manufacturer:</strong> PT Waru Gunung (Surabaya, Indonesia). Direct factory loading via Tanjung Perak Port (Surabaya) and Tanjung Priok Port (Jakarta).</p>
        <p style="margin: 0 0 6px 0;">• <strong>Export Partner:</strong> PT Indo Sukses Semesta (HOTS Trading) — authorized B2B export facilitator.</p>
        <p style="margin: 0 0 6px 0;">• <strong>Target Destination:</strong> {dest_display}. Shipped directly from Indonesia to international commercial project sites and regional distribution hubs.</p>
        <p style="margin: 0; color: #475569; font-style: italic;">• <strong>Compliance Note:</strong> Destination country specific compliance standards, localized packaging/labeling, and shipping terms (FOB/CIF) are confirmed per project order prior to dispatch.</p>
    </div>

    <!-- ACCIO SECTION 9.4 SAFE OEM/ODM NOTICE -->
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
        <h4 style="margin: 0 0 8px 0; font-size: 14px; color: #1e3a8a; display: flex; align-items: center; gap: 6px;">
            <span>📢</span> Conditional OEM & ODM Customization Notice
        </h4>
        <p style="margin: 0 0 6px 0; font-size: 12.5px; color: #334155; line-height: 1.5;">
            • <strong>Genuine Factory Production:</strong> Ready-to-ship inventory strictly features original <strong>{brand}</strong> branding to preserve verified factory quality and compliance standards.
        </p>
        <p style="margin: 0; font-size: 12.5px; color: #334155; line-height: 1.5;">
            • <strong>OEM / ODM Inquiries:</strong> Custom branding, color variations, packaging, and tooling inquiries are subject to factory feasibility, MOQ thresholds, sample approval, and commercial confirmation.
        </p>
    </div>

    <!-- KEY ADVANTAGES -->
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px 20px; margin-bottom: 20px;">
        <h4 style="margin: 0 0 12px 0; font-size: 15px; color: #1e3a8a;">Engineered Performance & Key Selling Points</h4>
        <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #334155;">
            <li style="margin-bottom: 6px;"><strong>Seamless Waterproof Construction:</strong> Monolithic high-pressure injection molding eliminates seams to prevent liquid ingress.</li>
            <li style="margin-bottom: 6px;"><strong>High-Traction Anti-Slip Sole:</strong> Deep-cleated tread pattern disperses water and mud for solid footing on slippery surfaces.</li>
            <li style="margin-bottom: 6px;"><strong>Durability & Oil Resistance:</strong> Industrial polymer compound resists mild acids, alkalis, oils, and agricultural fertilizers.</li>
            <li style="margin-bottom: 6px;"><strong>Ergonomic Comfort:</strong> Anatomically shaped sole and shaft reduce foot fatigue during extended industrial duty.</li>
            <li style="margin-bottom: 0;"><strong>Direct Indonesian Factory Export:</strong> Cost-efficient volume supply directly from PT Waru Gunung via Tanjung Perak/Priok.</li>
        </ul>
    </div>

    <!-- TECHNICAL SPECIFICATION MATRIX -->
    <div style="margin-bottom: 20px;">
        <h4 style="font-size: 15px; color: #1e3a8a; border-left: 4px solid #0284c7; padding-left: 10px; margin-bottom: 12px;">Technical Specification Matrix</h4>
        <table style="width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left;">
            <tbody>
                <tr style="background-color: #f1f5f9;"><th style="padding: 8px 12px; border: 1px solid #cbd5e1; width: 32%;">Item / Model Code</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{sku or clean_mod}</td></tr>
                <tr><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Brand</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{brand}</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Legal Manufacturer</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">PT Waru Gunung (Surabaya, Indonesia)</td></tr>
                <tr><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Product Classification</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{info['product_type']}</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Toe Protection</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1; font-weight: 600;">{toe_protection_text}</td></tr>
                <tr><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Midsole Protection</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{midsole_text}</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Primary Material</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">High-Grade PVC / Synthetic Polymer</td></tr>
                <tr><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Outsole Specification</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">Deep-Cleated Anti-Slip High Density Sole</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Approximate Weight</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{weight_kg} kg per pair</td></tr>
                <tr><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Size Range</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">EU 38 - 44 / US 6 - 11</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Country of Origin</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1;">Indonesia (Factory Direct Export)</td></tr>
                <tr><th style="padding: 8px 12px; border: 1px solid #cbd5e1;">Verified Standard</th><td style="padding: 8px 12px; border: 1px solid #cbd5e1; font-weight: 700; color: {cert_badge_color};">{cert_display}</td></tr>
            </tbody>
        </table>
    </div>

    <!-- PACKAGING & SHIPPING -->
    <div style="background-color: #f1f5f9; border-radius: 8px; padding: 14px 18px; font-size: 12.5px; color: #334155;">
        <h5 style="margin: 0 0 6px 0; font-size: 13.5px; color: #0f172a;">Packaging & Export Shipping Logistics</h5>
        <p style="margin: 0 0 4px 0;">• <strong>Carton Packaging:</strong> 1 pair individual polybag; 12 to 24 pairs per reinforced export corrugated carton.</p>
        <p style="margin: 0 0 4px 0;">• <strong>Port of Dispatch:</strong> Tanjung Perak Seaport (Surabaya) / Tanjung Priok Seaport (Jakarta), Indonesia.</p>
        <p style="margin: 0;">• <strong>Dispatch Schedule:</strong> Prompt shipment for standard inventory; Full Container Load (FCL) shipping available worldwide.</p>
    </div>
</div>"""
    return html

def generate_accio_listing(sku="", product_title="", category_group="", preferred_angle=None, model_number="", existing_price=5.50, existing_weight=1.7, destination_country=None):
    """
    Main function to generate full Accio-compliant listing package for one product.
    Returns dictionary with:
    - titles (list of 3 options, all <= 128 chars)
    - primary_title (chosen best title)
    - keywords (Alibaba comma-separated string)
    - kw_data (full structured keyword dictionary)
    - classification (group, cert status, prohibited claims)
    - description_html (Accio verified HTML)
    - angle (target industry angle)
    - destination_country (target country)
    """
    model_name = model_number or clean_model_name(product_title or sku)
    info = classify_accio_sku(sku=sku, model=model_name, title=product_title, category=category_group)
    angle = preferred_angle if (preferred_angle and preferred_angle in ACCIO_INDUSTRY_ANGLES) else info["default_angle"]

    kw_data = generate_accio_keywords_formula(info, model_name=model_name, angle=angle, destination_country=destination_country)
    titles = generate_accio_title_options(info, model_name=model_name, kw_data=kw_data, angle=angle, destination_country=destination_country)
    primary_title = titles[0]

    desc_html = generate_accio_html_description(
        info=info,
        model_name=model_name,
        titles=titles,
        kw_data=kw_data,
        price_usd=existing_price or 5.50,
        weight_kg=existing_weight or 1.7,
        sku=sku,
        destination_country=destination_country
    )

    return {
        "sku": sku,
        "model_name": model_name,
        "classification": info,
        "target_industry_angle": angle,
        "destination_country": destination_country or "Global / General",
        "primary_title": primary_title,
        "title_options": titles,
        "title_length": len(primary_title),
        "primary_keyword_1": kw_data["primary_keyword"],
        "primary_keyword_2": kw_data["secondary_keyword"],
        "primary_keyword_3": kw_data["third_keyword"],
        "keywords": kw_data["alibaba_keywords_string"],
        "structured_keywords": kw_data,
        "source_country_keywords": kw_data.get("source_country_keywords", []),
        "destination_country_keywords": kw_data.get("destination_country_keywords", []),
        "country_compliance_notes": kw_data.get("country_compliance_notes", ""),
        "country_prohibited_claims": kw_data.get("country_prohibited_claims", []),
        "prohibited_claims": info["prohibited_claims"],
        "description_html": desc_html
    }

def batch_update_db_with_accio(product_ids=None, preferred_angle=None, destination_country=None, update_description=True):
    """
    Batch applies Accio generation to products in SQLite database.
    If product_ids is provided, updates only those IDs; otherwise updates all products.
    """
    db_file = os.path.join(BASE_DIR, "Database", "alibaba_master.db")
    if not os.path.exists(db_file):
        db_file = os.path.join(BASE_DIR, "alibaba_master.db")

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if product_ids and len(product_ids) > 0:
        placeholders = ','.join('?' * len(product_ids))
        cur.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", list(product_ids))
    else:
        cur.execute("SELECT * FROM products ORDER BY id ASC")

    prods = cur.fetchall()
    updated_count = 0

    for p in prods:
        sku = p['sku'] or ''
        title = p['product_title'] or ''
        model = p['model_number'] or ''
        cat = p['category_group'] or ''
        price = p['price_usd'] or 5.50
        weight = p['gross_weight_kg'] or 1.7

        res = generate_accio_listing(
            sku=sku,
            product_title=title,
            category_group=cat,
            preferred_angle=preferred_angle,
            model_number=model,
            existing_price=price,
            existing_weight=weight,
            destination_country=destination_country
        )

        if update_description:
            cur.execute("""
            UPDATE products SET
                product_title = ?,
                keywords = ?,
                industry_angle = ?,
                description_html = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (res['primary_title'], res['keywords'], res['target_industry_angle'], res['description_html'], p['id']))
        else:
            cur.execute("""
            UPDATE products SET
                product_title = ?,
                keywords = ?,
                industry_angle = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (res['primary_title'], res['keywords'], res['target_industry_angle'], p['id']))

        updated_count += 1

    conn.commit()
    conn.close()
    return updated_count
