import urllib.request
import json
import time
from datetime import datetime

_EXCHANGE_CACHE = {
    "rate": 16250.0,
    "last_updated": 0,
    "source": "Default Baseline"
}

def get_live_usd_idr_rate():
    """
    Fetches actual real-time USD to IDR rate from public financial APIs.
    Caches for 30 minutes.
    """
    global _EXCHANGE_CACHE
    now = time.time()
    if now - _EXCHANGE_CACHE["last_updated"] < 1800 and _EXCHANGE_CACHE["rate"] > 10000:
        return _EXCHANGE_CACHE["rate"], _EXCHANGE_CACHE["source"], datetime.fromtimestamp(_EXCHANGE_CACHE["last_updated"]).strftime("%Y-%m-%d %H:%M:%S")

    apis = [
        ("https://api.exchangerate-api.com/v4/latest/USD", "ExchangeRate API (Live Google Market Sync)"),
        ("https://open.er-api.com/v6/latest/USD", "Open ER-API (Live Forex Market)")
    ]

    for url, src_name in apis:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                rate = data.get("rates", {}).get("IDR")
                if rate and rate > 10000:
                    _EXCHANGE_CACHE["rate"] = float(rate)
                    _EXCHANGE_CACHE["last_updated"] = now
                    _EXCHANGE_CACHE["source"] = src_name
                    return _EXCHANGE_CACHE["rate"], _EXCHANGE_CACHE["source"], datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            continue

    return _EXCHANGE_CACHE["rate"], "Fallback Market Baseline", datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_packaging_and_carton(price_idr=None, price_usd=None, pairs_per_carton=12, category_group="", custom_rate=None):
    """
    Calculates side-by-side:
    - USD to IDR conversion based on live or custom rate
    - Carton price in USD and IDR
    - Carton dimensions, gross weight, and CBM
    - Tiered bulk discounts
    - HOTS export service charge breakdown
    """
    rate, source, updated_time = get_live_usd_idr_rate()
    if custom_rate and float(custom_rate) > 1000:
        rate = float(custom_rate)
        source = "Custom User Input"

    # Price conversion
    if price_usd is not None and price_usd > 0:
        fob_usd = round(float(price_usd), 2)
        domestic_idr = round(fob_usd * rate)
    elif price_idr is not None and price_idr > 0:
        domestic_idr = round(float(price_idr))
        fob_usd = round(domestic_idr / rate, 2)
    else:
        domestic_idr = 85000
        fob_usd = 5.50

    # Determine default pairs per carton based on footwear category
    cat_lower = str(category_group).lower()
    if not pairs_per_carton or pairs_per_carton <= 0:
        if "safety" in cat_lower or "s5" in cat_lower or "orca" in cat_lower:
            pairs_per_carton = 12
        elif "chef" in cat_lower or "medic" in cat_lower:
            pairs_per_carton = 18
        elif "clogs" in cat_lower or "sandals" in cat_lower or "kids" in cat_lower:
            pairs_per_carton = 24
        else:
            pairs_per_carton = 12

    # Carton metrics calculation
    pairs = int(pairs_per_carton)
    carton_price_usd = round(fob_usd * pairs, 2)
    carton_price_idr = round(domestic_idr * pairs)

    # Standard export carton specs (AP Boots factory standards)
    if pairs <= 12:
        carton_dims = "60 x 40 x 40 cm"
        carton_cbm = 0.096
        weight_per_pair = 1.6
    elif pairs <= 18:
        carton_dims = "62 x 42 x 45 cm"
        carton_cbm = 0.117
        weight_per_pair = 0.9
    else:
        carton_dims = "65 x 45 x 50 cm"
        carton_cbm = 0.146
        weight_per_pair = 0.6

    carton_gross_weight = round(weight_per_pair * pairs + 1.2, 1)

    # Container loading estimates
    cbm_20ft = 28.0 # Usable volume
    cbm_40ft_hc = 68.0
    ctns_20ft = int(cbm_20ft / carton_cbm) if carton_cbm else 290
    ctns_40ft = int(cbm_40ft_hc / carton_cbm) if carton_cbm else 700

    # Tiered pricing structure
    tier1_usd = fob_usd # MOQ 100 pairs
    tier2_usd = round(fob_usd * 0.95, 2) # MOQ 500 pairs (-5%)
    tier3_usd = round(fob_usd * 0.90, 2) # MOQ 1000 pairs (-10%)

    # HOTS Service Charge (Company Knowledge Base)
    charge_member = round(fob_usd * 0.02, 3) # 2% Member regular
    charge_non_member = round(fob_usd * 0.05, 3) # 5% Non-member
    charge_full_export = round(fob_usd * 0.15, 3) # 15% Full Assistance

    return {
        "exchange_rate": rate,
        "exchange_source": source,
        "rate_updated_at": updated_time,
        "unit_fob_usd": fob_usd,
        "unit_price_usd": fob_usd,
        "unit_domestic_idr": domestic_idr,
        "unit_price_idr": domestic_idr,
        "pairs_per_carton": pairs,
        "carton_price_usd": carton_price_usd,
        "carton_price_idr": carton_price_idr,
        "carton_dimensions": carton_dims,
        "carton_cbm": carton_cbm,
        "carton_gross_weight_kg": carton_gross_weight,
        "specs": {
            "packaging_type": "Master Carton",
            "cbm_per_carton": carton_cbm,
            "carton_dimensions_cm": carton_dims,
            "gross_weight_kg_per_carton": carton_gross_weight
        },
        "container_loading": {
            "cartons_20ft": ctns_20ft,
            "pairs_20ft": ctns_20ft * pairs,
            "cartons_40ft_hc": ctns_40ft,
            "pairs_40ft_hc": ctns_40ft * pairs
        },
        "container_capacity": {
            "container_20ft_cartons": ctns_20ft,
            "container_20ft_pairs": ctns_20ft * pairs,
            "container_40ft_hc_cartons": ctns_40ft,
            "container_40ft_hc_pairs": ctns_40ft * pairs
        },
        "tiered_pricing": {
            "tier1": {"moq": 100, "price_usd": tier1_usd, "carton_price": round(tier1_usd * pairs, 2)},
            "tier2": {"moq": 500, "price_usd": tier2_usd, "carton_price": round(tier2_usd * pairs, 2), "discount": "5%"},
            "tier3": {"moq": 1000, "price_usd": tier3_usd, "carton_price": round(tier3_usd * pairs, 2), "discount": "10%"},
            "tier_1_moq100": {"moq": 100, "price_per_pair_usd": tier1_usd, "price_per_carton_usd": round(tier1_usd * pairs, 2)},
            "tier_2_moq500": {"moq": 500, "price_per_pair_usd": tier2_usd, "price_per_carton_usd": round(tier2_usd * pairs, 2), "discount": "5%"},
            "tier_3_moq1000": {"moq": 1000, "price_per_pair_usd": tier3_usd, "price_per_carton_usd": round(tier3_usd * pairs, 2), "discount": "10%"}
        },
        "hots_service_charge": {
            "member_regular_2pct": {"usd": charge_member, "idr": round(charge_member * rate)},
            "non_member_5pct": {"usd": charge_non_member, "idr": round(charge_non_member * rate)},
            "full_assistance_15pct": {"usd": charge_full_export, "idr": round(charge_full_export * rate)}
        },
        "hots_export_charges": {
            "member_regular_2pct": {"rate": "2.0%", "fee_per_pair_usd": charge_member, "fee_per_pair_idr": round(charge_member * rate)},
            "non_member_mandiri_5pct": {"rate": "5.0%", "fee_per_pair_usd": charge_non_member, "fee_per_pair_idr": round(charge_non_member * rate)},
            "full_assistance_15pct": {"rate": "15.0%", "fee_per_pair_usd": charge_full_export, "fee_per_pair_idr": round(charge_full_export * rate)}
        }
    }
