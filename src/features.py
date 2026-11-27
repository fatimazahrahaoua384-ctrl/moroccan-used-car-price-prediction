import re
import numpy as np
import pandas as pd
import ast 

REF_YEAR = 2024  # année de collecte du dataset
EQUIPMENT_VOCAB = [
    "Electric Windows", "CD/MP3/Bluetooth", "Alloy Wheels", "Air Conditioning",
    "Airbags", "Central Locking", "Rear Camera", "ABS", "Leather Seats",
    "Speed Limiter", "Cruise Control", "Parking Sensors", "Onboard Computer",
    "ESP", "Navigation System/GPS", "Sunroof",
]

def parse_equipment(s):
    """"['ABS', 'ESP']" -> ['ABS', 'ESP'] sans doublons ; NaN si manquant ou illisible."""
    if pd.isna(s):
        return np.nan
    try:
        return sorted(set(ast.literal_eval(s)))
    except (ValueError, SyntaxError):
        return np.nan
def parse_mileage(s):
    """'200 000 - 249 999' -> milieu de tranche (224999.5)."""
    if pd.isna(s):
        return np.nan
    nums = [int(x.replace(" ", "")) for x in re.findall(r"\d[\d ]*\d|\d", str(s))]
    return float(np.mean(nums)) if nums else np.nan

def parse_year(s):
    """'1980 ou plus ancien' -> 1980."""
    m = re.search(r"\d{4}", str(s))
    return float(m.group()) if m else np.nan

def parse_fiscal_power(s):
    """'8 CV' -> 8."""
    m = re.search(r"\d+", str(s))
    return float(m.group()) if m else np.nan

def add_features(df):
    out = df.copy()
    out["mileage_num"] = out["Mileage"].map(parse_mileage)
    out["year_num"] = out["Year"].map(parse_year)
    out["car_age"] = REF_YEAR - out["year_num"]
    out["fiscal_power_num"] = out["Fiscal Power"].map(parse_fiscal_power)

    # Règle métier : "0 - 4 999" sur une voiture de 3 ans ou plus = valeur par défaut
    suspect = (out["Mileage"] == "0 - 4 999") & (out["car_age"] >= 3)
    out["mileage_suspect"] = suspect.astype(int)
    out.loc[suspect, "mileage_num"] = np.nan 
    # Kilométrage par an ; un âge de 0 compte comme 1 an
    out["km_per_year"] = out["mileage_num"] / out["car_age"].clip(lower=1)
    eq = out["Equipment"].map(parse_equipment)
    out["n_equipment"] = eq.map(lambda L: len(L) if isinstance(L, list) else np.nan)
    for name in EQUIPMENT_VOCAB:
        out["eq_" + name] = eq.map(
            lambda L, n=name: (1.0 if n in L else 0.0) if isinstance(L, list) else np.nan
        )
    return out