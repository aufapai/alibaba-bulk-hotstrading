import os
import sqlite3
from datetime import datetime
import json

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Continental Seasonal Demand Knowledge Base (Dynamic by Quarter / Month)
CONTINENTAL_MARKET_RULES = {
    "Europe": {
        "name": "Europe (EU & UK)",
        "icon": "🇪🇺",
        "top_countries": ["Germany", "United Kingdom", "Netherlands", "France", "Poland"],
        "seasonal_demand": {
            "Q4": { # Oct - Dec
                "score": 95,
                "driver": "Winter preparation, freezing outdoor work conditions, indoor hospitality peak (restaurants & catering for holiday season).",
                "focus_categories": ["AP Safety Boots", "AP Chef Series", "AP Medic & Cleanroom", "AP Orca Series"],
                "recommended_angle": "Civil Construction",
                "key_certifications": "EN ISO 20345:2011 S5, CE Marking, Slip Resistance SRC",
                "recommended_keywords": ["steel toe safety boots", "s5 winter waterproof boots", "kitchen work shoes anti slip", "cold resistant work shoes"],
                "pricing_strategy": "Higher margin Tier 1 ($6.50 - $9.00 USD), MOQ 200 - 500 pairs.",
                "packaging_advice": "Individually polybagged or retail color box with EAN/UPC barcode, multilingual user manual (EN/DE/FR)."
            },
            "Q1": { # Jan - Mar
                "score": 88,
                "driver": "Late winter construction thaw, spring agriculture planting.",
                "focus_categories": ["AP Safety Boots", "AP Terra Series"],
                "recommended_angle": "Civil Construction",
                "key_certifications": "EN ISO 20345 S5, REACH Compliance",
                "recommended_keywords": ["heavy duty safety boots", "waterproof outdoor work boots", "farming gumboots"],
                "pricing_strategy": "Standard FOB USD 5.50 - $7.50.",
                "packaging_advice": "Master carton 12 pairs."
            },
            "Q2": { # Apr - Jun
                "score": 75,
                "driver": "Spring & summer gardening, festival rainwear, light construction.",
                "focus_categories": ["AP Casual & Biker", "AP Sandals & Clogs", "AP Terra Series"],
                "recommended_angle": "Agriculture & Farming",
                "key_certifications": "CE, Non-toxic PVC",
                "recommended_keywords": ["lightweight garden clogs", "summer waterproof shoes", "casual rain boots"],
                "pricing_strategy": "FOB USD 3.50 - $5.50.",
                "packaging_advice": "Standard export carton."
            },
            "Q3": { # Jul - Sep
                "score": 82,
                "driver": "Autumn rain preparation, forestry, post-summer industrial ramping.",
                "focus_categories": ["AP Terra Series", "AP Orca Series", "AP Safety Boots"],
                "recommended_angle": "All-Weather Rain Utility",
                "key_certifications": "EN ISO 20345",
                "recommended_keywords": ["autumn rain boots", "forestry waterproof footwear", "industrial work boots"],
                "pricing_strategy": "FOB USD 5.00 - $7.50.",
                "packaging_advice": "Standard export carton."
            }
        }
    },
    "North America": {
        "name": "North America (USA & Canada)",
        "icon": "🇺🇸",
        "top_countries": ["United States", "Canada", "Mexico"],
        "seasonal_demand": {
            "Q4": { # Oct - Dec
                "score": 94,
                "driver": "Autumn/Winter rainstorms, sub-zero logistics operations, food service holiday rush.",
                "focus_categories": ["AP Safety Boots", "AP Chef Series", "AP Orca Series"],
                "recommended_angle": "Oil & Gas Refinery",
                "key_certifications": "ASTM F2413-18 (I/75 C/75 EH), OSHA Compliant, Slip Resistance",
                "recommended_keywords": ["astm safety boots", "waterproof slip resistant chef shoes", "commercial kitchen footwear", "oil resistant rubber boots"],
                "pricing_strategy": "High volume pricing ($6.00 - $8.50 USD), MOQ 500 - 1000 pairs.",
                "packaging_advice": "US shoe size labeling (US Men 7-13), UPC barcode sticker on each carton."
            },
            "Q1": {
                "score": 90,
                "driver": "Snow thaw mud season, industrial construction kick-off.",
                "focus_categories": ["AP Safety Boots", "AP Terra Series"],
                "recommended_angle": "Mining & Quarrying",
                "key_certifications": "ASTM F2413, MSHA",
                "recommended_keywords": ["mud boots waterproof", "steel toe muck boots", "industrial safety gumboots"],
                "pricing_strategy": "USD 6.00 - $8.00.",
                "packaging_advice": "Heavy duty carton."
            },
            "Q2": {
                "score": 80,
                "driver": "Spring lawn & garden, fisheries, general outdoor maintenance.",
                "focus_categories": ["AP Terra Series", "AP Sandals & Clogs", "AP Kids Boots"],
                "recommended_angle": "Agriculture & Farming",
                "key_certifications": "Prop 65 Warning Compliance",
                "recommended_keywords": ["garden rain shoes", "waterproof clogs slip on", "kids rubber boots"],
                "pricing_strategy": "USD 3.80 - $5.50.",
                "packaging_advice": "Retail ready packaging."
            },
            "Q3": {
                "score": 85,
                "driver": "Hurricane & storm season in Southeast US, back-to-school kids rainwear.",
                "focus_categories": ["AP Kids Boots", "AP Casual & Biker", "AP Terra Series"],
                "recommended_angle": "All-Weather Rain Utility",
                "key_certifications": "CPSIA (for Kids), ASTM",
                "recommended_keywords": ["kids rain boots waterproof", "storm rain shoes", "heavy duty work boots"],
                "pricing_strategy": "USD 4.50 - $6.50.",
                "packaging_advice": "Hangtags with size charts."
            }
        }
    },
    "Southeast Asia": {
        "name": "Southeast Asia (ASEAN)",
        "icon": "🌏",
        "top_countries": ["Malaysia", "Thailand", "Philippines", "Vietnam", "Singapore"],
        "seasonal_demand": {
            "Q4": { # Oct - Dec
                "score": 98,
                "driver": "Peak Monsoon (Northeast Monsoon) wet season, heavy flood risk, palm oil & paddy harvest seasons.",
                "focus_categories": ["AP Terra Series", "AP Classic Boots", "AP Casual & Biker", "AP Orca Series"],
                "recommended_angle": "Agriculture & Farming",
                "key_certifications": "SNI, TKDN, ISO 9001 (High regional brand trust for AP Boots)",
                "recommended_keywords": ["pvc rain boots wholesale", "oil palm plantation boots", "motorcycle waterproof shoes", "anti flood rubber boots"],
                "pricing_strategy": "Competitive regional export FOB USD 3.80 - $5.80, MOQ 1000 - 3000 pairs.",
                "packaging_advice": "Standard export bale or compact corrugated carton to maximize 20ft/40ft container loading."
            },
            "Q1": {
                "score": 92,
                "driver": "Post-flood agricultural recovery, continuous plantation harvesting.",
                "focus_categories": ["AP Terra Series", "AP Classic Boots"],
                "recommended_angle": "Agriculture & Farming",
                "key_certifications": "SNI 0111:2009",
                "recommended_keywords": ["rubber farming boots", "waterproof plantation shoes", "agriculture gumboots"],
                "pricing_strategy": "USD 3.80 - $5.20.",
                "packaging_advice": "Direct container bulk."
            },
            "Q2": {
                "score": 80,
                "driver": "Dry construction season, infrastructure building, fisheries.",
                "focus_categories": ["AP Safety Boots", "AP Orca Series"],
                "recommended_angle": "Civil Construction",
                "key_certifications": "SNI, CE",
                "recommended_keywords": ["safety boots construction", "fishery waterproof boots", "industrial pvc boots"],
                "pricing_strategy": "USD 4.80 - $6.50.",
                "packaging_advice": "Standard carton."
            },
            "Q3": {
                "score": 90,
                "driver": "Early monsoon onset (Southwest Monsoon), tropical rainstorms.",
                "focus_categories": ["AP Casual & Biker", "AP Terra Series"],
                "recommended_angle": "Motorcycle & Courier",
                "key_certifications": "SNI",
                "recommended_keywords": ["motorcycle riding rain boots", "courier waterproof shoes", "anti slip rain boots"],
                "pricing_strategy": "USD 3.80 - $5.50.",
                "packaging_advice": "Compact cartons."
            }
        }
    },
    "Middle East": {
        "name": "Middle East & GCC",
        "icon": "🇦🇪",
        "top_countries": ["United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Oman"],
        "seasonal_demand": {
            "Q4": { # Oct - Dec
                "score": 91,
                "driver": "Cooler outdoor working weather creates the peak civil construction and infrastructure building season.",
                "focus_categories": ["AP Safety Boots", "AP Orca Series", "AP Medic & Cleanroom"],
                "recommended_angle": "Civil Construction",
                "key_certifications": "SASO, GSO, CE, Oil & Chemical Resistant Outsole",
                "recommended_keywords": ["construction safety boots s5", "heat resistant work boots", "oilfield safety footwear", "chemical resistant pvc boots"],
                "pricing_strategy": "FOB USD 5.80 - $7.80, MOQ 500 - 2000 pairs.",
                "packaging_advice": "Heat-resistant packaging, Arabic/English bilingual carton markings."
            },
            "Q1": {
                "score": 92,
                "driver": "Ongoing peak construction & oil/gas turnaround maintenance.",
                "focus_categories": ["AP Safety Boots", "AP Orca Series"],
                "recommended_angle": "Oil & Gas Refinery",
                "key_certifications": "GSO ISO 20345",
                "recommended_keywords": ["oil refinery safety boots", "heavy duty safety footwear", "industrial pvc boots"],
                "pricing_strategy": "USD 6.00 - $8.00.",
                "packaging_advice": "Bilingual marks."
            },
            "Q2": {
                "score": 70,
                "driver": "Extreme heat summer setting in; outdoor work hours restricted by law.",
                "focus_categories": ["AP Medic & Cleanroom", "AP Chef Series"],
                "recommended_angle": "Medical & Kitchen Hygiene",
                "key_certifications": "HACCP, CE",
                "recommended_keywords": ["indoor cleanroom clogs", "slip resistant kitchen shoes", "sanitary hospital footwear"],
                "pricing_strategy": "USD 4.50 - $6.50.",
                "packaging_advice": "Standard carton."
            },
            "Q3": {
                "score": 72,
                "driver": "Summer heat wave, focus on indoor food processing and facilities.",
                "focus_categories": ["AP Chef Series", "AP Medic & Cleanroom"],
                "recommended_angle": "Medical & Kitchen Hygiene",
                "key_certifications": "CE, Anti-bacterial",
                "recommended_keywords": ["food factory shoes", "kitchen waterproof shoes", "hygienic clogs"],
                "pricing_strategy": "USD 4.50 - $6.50.",
                "packaging_advice": "Standard carton."
            }
        }
    },
    "Oceania": {
        "name": "Oceania (Australia & NZ)",
        "icon": "🇦🇺",
        "top_countries": ["Australia", "New Zealand", "Papua New Guinea"],
        "seasonal_demand": {
            "Q4": { # Oct - Dec (Southern Hemisphere Spring/Summer)
                "score": 86,
                "driver": "Spring/Summer agricultural boom, wine grape harvesting, dairy farming, and commercial fishing.",
                "focus_categories": ["AP Terra Series", "AP Orca Series", "AP Safety Boots"],
                "recommended_angle": "Fishery & Seafood",
                "key_certifications": "AS/NZS 2210.3 (Safety Footwear Standard), Acid/Fertilizer Resistant",
                "recommended_keywords": ["dairy farming gumboots", "commercial fishery boots", "agriculture work boots waterproof", "heavy duty gumboots"],
                "pricing_strategy": "FOB USD 5.50 - $7.50, MOQ 250 - 500 pairs.",
                "packaging_advice": "AU sizing conversion charts, ISPM 15 certified wooden pallets if palletized."
            },
            "Q1": {
                "score": 84,
                "driver": "Summer outdoor work, food processing, fisheries.",
                "focus_categories": ["AP Orca Series", "AP Chef Series"],
                "recommended_angle": "Fishery & Seafood",
                "key_certifications": "AS/NZS 2210",
                "recommended_keywords": ["commercial seafood boots", "food processing footwear", "rubber work gumboots"],
                "pricing_strategy": "USD 5.50 - $7.50.",
                "packaging_advice": "Standard carton."
            },
            "Q2": {
                "score": 92,
                "driver": "Autumn/Winter rainy season in Southern Australia/NZ, mud and cold wet conditions.",
                "focus_categories": ["AP Safety Boots", "AP Terra Series"],
                "recommended_angle": "Civil Construction",
                "key_certifications": "AS/NZS 2210.3",
                "recommended_keywords": ["winter safety gumboots", "heavy duty waterproof work boots", "mud gumboots"],
                "pricing_strategy": "USD 6.00 - $8.00.",
                "packaging_advice": "Standard export packaging."
            },
            "Q3": {
                "score": 89,
                "driver": "Winter weather, pastoral livestock farming.",
                "focus_categories": ["AP Terra Series", "AP Safety Boots"],
                "recommended_angle": "Agriculture & Farming",
                "key_certifications": "AS/NZS",
                "recommended_keywords": ["farm boots waterproof", "livestock work boots", "steel cap gumboots"],
                "pricing_strategy": "USD 5.80 - $7.80.",
                "packaging_advice": "Standard export packaging."
            }
        }
    }
}

def get_current_quarter(month=None):
    if not month:
        month = datetime.now().month
    if month in [1, 2, 3]:
        return "Q1", "January - March"
    elif month in [4, 5, 6]:
        return "Q2", "April - June"
    elif month in [7, 8, 9]:
        return "Q3", "July - September"
    else:
        return "Q4", "October - December"

def get_category_groups_overview():
    """
    Groups all products by category and cross-references with marketplace_raw
    to calculate price benchmarks, competitor count, sales metrics, and image readiness.
    """
    conn = get_db()
    cur = conn.cursor()

    # 1. Catalog Products stats by category
    cur.execute("""
    SELECT 
        COALESCE(category_group, 'AP Classic Boots') as cat_grp,
        COUNT(*) as total_skus,
        AVG(price_usd) as avg_price_usd,
        MIN(price_usd) as min_price_usd,
        MAX(price_usd) as max_price_usd,
        AVG(inventory) as avg_inv
    FROM products
    GROUP BY cat_grp
    ORDER BY total_skus DESC
    """)
    cat_rows = cur.fetchall()

    # 2. Competitor / Marketplace Raw items stats
    cur.execute("""
    SELECT 
        source,
        COUNT(*) as total_items,
        AVG(price_idr) as avg_idr,
        SUM(sold_count) as total_sold,
        AVG(rating_score) as avg_rating
    FROM marketplace_raw
    GROUP BY source
    """)
    raw_sources = {r['source']: dict(r) for r in cur.fetchall()}

    overview = []
    for cr in cat_rows:
        grp = cr['cat_grp']
        
        # Sample products in this group
        cur.execute("""
        SELECT sku, product_title, price_usd, image_1, feature, target_keywords
        FROM products 
        WHERE category_group = ? 
        ORDER BY id ASC LIMIT 5
        """, (grp,))
        sample_prods = [dict(p) for p in cur.fetchall()]

        # Find competitor matches in marketplace_raw
        keyword_token = grp.replace('AP ', '').split()[0]
        cur.execute("""
        SELECT 
            COUNT(*) as comp_count,
            AVG(price_idr) as avg_comp_idr,
            SUM(sold_count) as comp_sold_total,
            AVG(rating_score) as comp_avg_rating,
            AVG(unique_images_count) as comp_avg_imgs
        FROM marketplace_raw
        WHERE product_name LIKE ?
        """, (f'%{keyword_token}%',))
        comp_stat = cur.fetchone()

        overview.append({
            "category_group": grp,
            "total_skus": cr['total_skus'],
            "price_usd_range": {
                "min": round(cr['min_price_usd'] or 5.50, 2),
                "avg": round(cr['avg_price_usd'] or 5.50, 2),
                "max": round(cr['max_price_usd'] or 5.50, 2)
            },
            "competitor_benchmark": {
                "sample_competitor_records": comp_stat['comp_count'] or 0,
                "avg_price_idr": int(comp_stat['avg_comp_idr'] or 85000),
                "total_sold_marketplace": int(comp_stat['comp_sold_total'] or 0),
                "avg_rating": round(comp_stat['comp_avg_rating'] or 4.8, 1),
                "avg_images_per_product": round(comp_stat['comp_avg_imgs'] or 4.0, 1)
            },
            "sample_products": sample_prods
        })

    conn.close()
    return overview, raw_sources

def generate_monthly_continental_intelligence(selected_category=None, month=None):
    """
    Generates dynamic seasonal continental market strategy for the given category and month.
    """
    if not month:
        month = datetime.now().month
    q_key, q_label = get_current_quarter(month)
    month_name = datetime.now().strftime("%B")

    overview, raw_sources = get_category_groups_overview()

    continent_results = []
    for c_key, c_info in CONTINENTAL_MARKET_RULES.items():
        q_data = c_info['seasonal_demand'].get(q_key, {})
        
        # Check relevance to selected_category
        is_primary_focus = False
        if selected_category:
            is_primary_focus = selected_category in q_data.get("focus_categories", [])
        else:
            is_primary_focus = True

        suitability = q_data.get("score", 70)
        if selected_category and not is_primary_focus:
            suitability = max(50, suitability - 20)

        continent_results.append({
            "continent": c_key,
            "name": c_info["name"],
            "icon": c_info["icon"],
            "top_countries": c_info["top_countries"],
            "suitability_score": suitability,
            "is_primary_focus": is_primary_focus,
            "quarter": q_key,
            "quarter_label": q_label,
            "current_month": month_name,
            "market_driver": q_data.get("driver", ""),
            "focus_categories": q_data.get("focus_categories", []),
            "recommended_angle": q_data.get("recommended_angle", "All-Weather Rain Utility"),
            "key_certifications": q_data.get("key_certifications", "Standard"),
            "recommended_keywords": q_data.get("recommended_keywords", []),
            "pricing_strategy": q_data.get("pricing_strategy", "Standard FOB USD"),
            "packaging_advice": q_data.get("packaging_advice", "Standard export carton")
        })

    # Sort continents by suitability score descending
    continent_results.sort(key=lambda x: x['suitability_score'], reverse=True)

    return {
        "current_month": month_name,
        "quarter": q_key,
        "quarter_label": q_label,
        "selected_category": selected_category or "All Footwear Categories",
        "categories_overview": overview,
        "raw_sources_summary": raw_sources,
        "continents_strategy": continent_results
    }
