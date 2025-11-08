# step3_targeted_zip_harvest.py
# Objectif : ajouter >=200 lignes par ZIP spécifié, en complétant year_built, zipcode, lot_area*.
# Reprend le CSV existant sans doublons. Compatible plan PRO (2 req/s) avec retry/backoff.

import os, sys, time, random
import pandas as pd
import requests
from dotenv import load_dotenv

# --- STDOUT UTF-8 (Windows) ---
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ===================== PARAMS =====================
# Fichier d'entrée (ton CSV actuel) et de sortie (sera réécrit avec ajouts)
IN_CSV   = "zillow_indy_10k_enriched.csv"   # adapte si besoin (ex: "zillow_indy_10k.csv")
OUT_CSV  = "zillow_indy_10k_enriched.csv"   # on réécrit par-dessus pour continuer le dataset

# ZIPs cibles (>=200 lignes à récolter par ZIP)
TARGET_ZIPS = [
    "46228","46229","46231","46234","46235","46236","46237","46239","46240","46241","46250",
    "46254","46256","46259","46260","46268","46278","46280","46290",
    "46032","46033","46074","46082",
    "46037","46038","46085",
    "46077",
    "46112","46123","46168",
    "46142","46143",
    "46060","46062","46075","46055",
    "46226","46107"
]
TARGET_PER_ZIP     = 200            # minimum de lignes à atteindre pour chaque ZIP
MAX_PAGES_PER_ZIP  = 30             # 1 page ~ 40-50 biens
RESULTS_PER_PAGE   = 50
SAVE_EVERY_NEW     = 200            # checkpoint toutes les N nouvelles lignes ajoutées

# Throttle/Retry pour plan PRO (~2 req/s)
BASE_SLEEP     = 0.55
MAX_RETRIES    = 6
COOLDOWN_429_S = 20
COOLDOWN_5xx_S = 20
TIMEOUT_S      = 30

# ===================== API SETUP =====================
load_dotenv()
HOST = os.getenv("RAPIDAPI_HOST", "zillow-com1.p.rapidapi.com")
KEY  = os.getenv("RAPIDAPI_KEY")
if not KEY:
    raise RuntimeError("RAPIDAPI_KEY manquant dans .env")

HEADERS = {"X-RapidAPI-Key": KEY, "X-RapidAPI-Host": HOST}
BASE = f"https://{HOST}"

EP_SEARCH            = "/propertyExtendedSearch"   # liste
EP_SEARCH_FALLBACK   = "/search"
EP_PROPERTY          = "/property"                 # détail par zpid
EP_BUILDING          = "/building"                 # complément (lot, building...)

# ===================== HELPERS =====================
def sleep_tick():
    time.sleep(BASE_SLEEP + random.random()*0.10)

def to_float(x):
    if x is None: return None
    if isinstance(x, (int, float)): return float(x)
    try:
        return float(str(x).replace("$","").replace(",","").strip())
    except Exception:
        return None

def api_get(path, params):
    url = BASE + path
    backoff = 1.2
    delay = BASE_SLEEP
    for attempt in range(1, MAX_RETRIES+1):
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT_S)
        except requests.RequestException as e:
            print(f"[WARN] reseau (try {attempt}/{MAX_RETRIES}) {e} | {path} {params}")
            time.sleep(delay); delay *= backoff; continue

        code = r.status_code
        if code == 200:
            try:
                return r.json()
            finally:
                sleep_tick()
        elif code == 429:
            print(f"[WARN] 429 (try {attempt}) {path} | pause {COOLDOWN_429_S}s")
            time.sleep(COOLDOWN_429_S); delay *= backoff; continue
        elif code in (500,502,503,504):
            print(f"[WARN] {code} (try {attempt}) {path} | pause {COOLDOWN_5xx_S}s")
            time.sleep(COOLDOWN_5xx_S); delay *= backoff; continue
        else:
            txt = r.text[:150]
            print(f"[WARN] status {code} {path} {params} | {txt}")
            sleep_tick()
            return None
    return None

def pick_list(d):
    if not isinstance(d, dict): return []
    for k in ("props", "results", "homes", "list"):
        v = d.get(k)
        if isinstance(v, list) and v:
            return v
    return []

def normalize_item(it: dict) -> dict:
    zpid        = it.get("zpid") or it.get("id")
    price       = it.get("price") or it.get("unformattedPrice") or it.get("priceRaw")
    beds        = it.get("bedrooms") or it.get("beds")
    baths       = it.get("bathrooms") or it.get("baths")
    living_area = it.get("livingArea") or it.get("area") or it.get("livingAreaSqFt")
    year_built  = it.get("yearBuilt") or (it.get("hdpData",{}).get("homeInfo",{}).get("yearBuilt")
                                          if isinstance(it.get("hdpData"), dict) else None)
    zipcode     = (it.get("zipcode") or it.get("postalCode") or it.get("zipCode")
                   or it.get("addressZipcode"))
    address     = it.get("address") or it.get("formattedAddress") or it.get("streetAddress") or it.get("fullAddress")
    lat         = it.get("latitude") or (it.get("latLong",{}).get("latitude") if isinstance(it.get("latLong"), dict) else None)
    lon         = it.get("longitude") or (it.get("latLong",{}).get("longitude") if isinstance(it.get("latLong"), dict) else None)
    lot_val     = it.get("lotAreaValue")
    lot_unit    = it.get("lotAreaUnit")

    lat = to_float(lat); lon = to_float(lon)
    lot_val = to_float(lot_val)

    zip_str = None
    if isinstance(zipcode, (int, float)) and not pd.isna(zipcode):
        zip_str = str(int(zipcode)).zfill(5)
    elif isinstance(zipcode, str) and zipcode.strip():
        zip_str = zipcode.strip()

    lot_area_sqft = None
    if lot_val is not None and lot_unit:
        u = lot_unit.lower()
        if u in ("sqft","square feet","sq ft","ft2"): lot_area_sqft = lot_val
        elif u in ("acres","acre"):                  lot_area_sqft = lot_val * 43560.0
        elif u in ("sqm","m2","square meters"):      lot_area_sqft = lot_val * 10.7639

    return {
        "zpid": str(zpid) if zpid is not None else None,
        "address": address,
        "sale_price": to_float(price),
        "bedrooms": to_float(beds),
        "bathrooms": to_float(baths),
        "living_area": to_float(living_area),
        "year_built": to_float(year_built),
        "zipcode": zip_str,
        "lat": lat, "lon": lon,
        "lot_area_value": lot_val,
        "lot_area_unit": lot_unit,
        "lot_area_sqft": lot_area_sqft,
    }

def fetch_zip(zipcode: str, already_have: int, need_min: int) -> pd.DataFrame:
    """Récupère des items pour un ZIP jusqu'à atteindre need_min (ou épuiser les pages)."""
    acc = []
    for page in range(1, MAX_PAGES_PER_ZIP + 1):
        if already_have + len(acc) >= need_min:
            break
        params = {
            "location": zipcode,
            "status_type": "ForSale",
            "page": page,
            "limit": RESULTS_PER_PAGE,
            "sort": "newest"
        }
        data = api_get(EP_SEARCH, params)
        items = pick_list(data)
        if not items:
            # tentative fallback
            data2 = api_get(EP_SEARCH_FALLBACK, params)
            items = pick_list(data2)
        if not items:
            break
        acc.extend(items)
        print(f"[INFO] ZIP {zipcode} page {page} -> +{len(items)} (batch {len(acc)})")
    if not acc:
        return pd.DataFrame()
    rows = [normalize_item(x) for x in acc]
    return pd.DataFrame(rows)

def extract_from_detail(d):
    if not isinstance(d, dict): return {}
    yb = (d.get("yearBuilt") or (d.get("hdpData",{}).get("homeInfo",{}).get("yearBuilt")
                                 if isinstance(d.get("hdpData"), dict) else None))
    zp = (d.get("zipcode") or d.get("postalCode") or d.get("zipCode") or d.get("addressZipcode"))
    if isinstance(zp, (int, float)) and not pd.isna(zp):
        zp = str(int(zp)).zfill(5)
    elif isinstance(zp, str):
        zp = zp.strip() or None
    lot_val  = d.get("lotAreaValue") or d.get("lotSize")
    lot_unit = d.get("lotAreaUnit")
    lot_val  = to_float(lot_val)
    lot_sqft = None
    if lot_val is not None:
        u = (lot_unit or "").lower()
        if u in ("sqft","square feet","sq ft","ft2"): lot_sqft = lot_val
        elif u in ("acres","acre"):                  lot_sqft = lot_val * 43560.0
        elif u in ("sqm","m2","square meters"):      lot_sqft = lot_val * 10.7639
    return {
        "year_built": to_float(yb),
        "zipcode": zp,
        "lot_area_value": lot_val,
        "lot_area_unit": lot_unit,
        "lot_area_sqft": lot_sqft,
    }

def enrich_one_zpid(zpid: str) -> dict:
    d = api_get(EP_PROPERTY, {"zpid": zpid}) or {}
    info = extract_from_detail(d)
    # si encore incomplet, tenter /building
    if (info.get("year_built") is None) or (info.get("lot_area_sqft") is None):
        b = api_get(EP_BUILDING, {"zpid": zpid}) or {}
        more = extract_from_detail(b)
        for k, v in more.items():
            if info.get(k) is None and v is not None:
                info[k] = v
    return info

def enrich_batch(df_zip_new: pd.DataFrame, forced_zip: str) -> pd.DataFrame:
    """Complète year_built/zipcode/lot_area* pour les nouvelles lignes d'un ZIP.
       Si zipcode reste manquant, force le ZIP courant."""
    if df_zip_new.empty:
        return df_zip_new

    need = (df_zip_new["year_built"].isna()
            | df_zip_new["zipcode"].isna()
            | df_zip_new["lot_area_sqft"].isna())
    idxs = df_zip_new[need].index.tolist()

    for i in idxs:
        zpid = df_zip_new.at[i, "zpid"]
        if not zpid: 
            continue
        info = enrich_one_zpid(zpid)
        if pd.isna(df_zip_new.at[i, "year_built"]) and info.get("year_built") is not None:
            df_zip_new.at[i, "year_built"] = info["year_built"]
        if (pd.isna(df_zip_new.at[i, "zipcode"]) or not str(df_zip_new.at[i, "zipcode"]).strip()):
            if info.get("zipcode"):
                df_zip_new.at[i, "zipcode"] = info["zipcode"]
            else:
                # fallback final : utiliser le ZIP en cours si vraiment absent
                df_zip_new.at[i, "zipcode"] = forced_zip
        if pd.isna(df_zip_new.at[i, "lot_area_value"]) and info.get("lot_area_value") is not None:
            df_zip_new.at[i, "lot_area_value"] = info["lot_area_value"]
        if (pd.isna(df_zip_new.at[i, "lot_area_unit"]) or not str(df_zip_new.at[i, "lot_area_unit"]).strip()) and info.get("lot_area_unit"):
            df_zip_new.at[i, "lot_area_unit"] = info["lot_area_unit"]
        if pd.isna(df_zip_new.at[i, "lot_area_sqft"]) and info.get("lot_area_sqft") is not None:
            df_zip_new.at[i, "lot_area_sqft"] = info["lot_area_sqft"]

    # coercions légères
    for c in ["sale_price","bedrooms","bathrooms","living_area","year_built","lot_area_value","lot_area_sqft"]:
        if c in df_zip_new.columns:
            df_zip_new[c] = pd.to_numeric(df_zip_new[c], errors="coerce")

    return df_zip_new

# ===================== MAIN =====================
def main():
    # Charger CSV existant
    if not os.path.exists(IN_CSV):
        raise FileNotFoundError(f"{IN_CSV} introuvable")
    df_all = pd.read_csv(IN_CSV)
    if "zpid" not in df_all.columns:
        raise ValueError("Colonne 'zpid' manquante dans le CSV d'entrée")
    df_all["zpid"] = df_all["zpid"].astype(str)

    # S'assurer des colonnes cibles
    for c in ["year_built","zipcode","lot_area_value","lot_area_unit","lot_area_sqft","lat","lon","living_area","bedrooms","bathrooms","sale_price"]:
        if c not in df_all.columns:
            df_all[c] = pd.NA

    seen = set(df_all["zpid"].dropna().astype(str))
    added_since_save = 0
    print(f"[START] lignes existantes: {len(df_all)} | zpid uniques: {len(seen)}")

    # Compter par ZIP déjà présentes
    def zip_count(zipcode):
        return int((df_all["zipcode"] == zipcode).sum()) if "zipcode" in df_all.columns else 0

    for z in TARGET_ZIPS:
        have = zip_count(z)
        if have >= TARGET_PER_ZIP:
            print(f"[SKIP] ZIP {z} deja {have} >= {TARGET_PER_ZIP}")
            continue

        need = TARGET_PER_ZIP
        print(f"[ZIP] {z} besoin: {need} | existant: {have}")

        # Récupérer pages jusqu'à atteindre le quota
        df_new_raw = fetch_zip(z, already_have=have, need_min=need)
        if df_new_raw.empty:
            print(f"[WARN] ZIP {z} aucun nouveau resultat des endpoints liste.")
            continue

        # Dédupliquer vs existant
        df_new_raw["zpid"] = df_new_raw["zpid"].astype(str)
        before = len(df_new_raw)
        df_new_raw = df_new_raw[~df_new_raw["zpid"].isin(seen)].copy()
        after = len(df_new_raw)
        if after == 0:
            print(f"[INFO] ZIP {z} aucun zpid neuf (batch {before}).")
            continue

        # Enrichissement ciblé des nouvelles lignes
        df_new_enriched = enrich_batch(df_new_raw, forced_zip=z)

        # Concat au master
        df_all = pd.concat([df_all, df_new_enriched], ignore_index=True)
        seen |= set(df_new_enriched["zpid"])
        added_since_save += len(df_new_enriched)
        total_zip = int((df_all["zipcode"] == z).sum())
        print(f"[ADD] ZIP {z} +{len(df_new_enriched)} (filtre {before}->{after}) | total ZIP {z} = {total_zip} | total all = {len(df_all)}")

        # Checkpoint périodique
        if added_since_save >= SAVE_EVERY_NEW:
            df_all.to_csv(OUT_CSV, index=False)
            print(f"[SAVE] checkpoint -> {OUT_CSV} ({len(df_all)} lignes)")
            added_since_save = 0

    # Sauvegarde finale
    df_all.to_csv(OUT_CSV, index=False)
    print(f"[SAVE] final -> {OUT_CSV} ({len(df_all)} lignes)")

    # Diagnostic final minimal
    cols = ["sale_price","bedrooms","bathrooms","living_area","year_built","zipcode","lot_area_sqft"]
    exist = [c for c in cols if c in df_all.columns]
    if exist:
        print("\n[DIAG] taux de NaN :")
        print(df_all[exist].isna().mean().round(3))

if __name__ == "__main__":
    main()
