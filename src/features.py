import re
import numpy as np
import pandas as pd

REF_YEAR = 2024  # année de collecte du dataset

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
    return out