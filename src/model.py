import numpy as np
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor

from src.features import EQUIPMENT_VOCAB

NUM_COLS = ["mileage_num", "car_age", "fiscal_power_num", "Number of Doors",
            "mileage_suspect"] + ["eq_" + n for n in EQUIPMENT_VOCAB]
CAT_LOW = ["Condition", "Gearbox", "Fuel", "Origin", "First Owner"]
CAT_HIGH = ["Brand", "Model", "Location", "Sector"]


def categorical_pipeline(**encoder_params):
    return Pipeline([
        ("imp", SimpleImputer(strategy="constant", fill_value="Inconnu")),
        ("oh", OneHotEncoder(handle_unknown="ignore", **encoder_params)),
    ])


def build_model():
    prep = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), NUM_COLS),
        ("low", categorical_pipeline(), CAT_LOW),
        ("high", categorical_pipeline(min_frequency=30), CAT_HIGH),
    ])
    pipe = Pipeline([
        ("prep", prep),
        ("reg", XGBRegressor(n_estimators=1000, learning_rate=0.05,
                             max_depth=12, random_state=42, n_jobs=-1)),
    ])
    return TransformedTargetRegressor(
        regressor=pipe, func=np.log1p, inverse_func=np.expm1)