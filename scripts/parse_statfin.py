import pandas as pd

from scripts.misc import (
    DEST_PATH_FROM_ROOT,
    SOURCE_PATH_FROM_ROOT,
    convert_amount_column_to_weight,
)

SOURCE_LOC_AGE_GENDER_FILE = (
    SOURCE_PATH_FROM_ROOT / "statfin" / "location_age_gender_distr.csv"
)

HEADER_TRANSFORMATION_TABLE = {
    "Alue": "area",
    "Ikä": "age",
    "Miehet 2020 Väestö 31.12.": "men",
    "Naiset 2020 Väestö 31.12.": "women",
}

DEST_LOC_AGE_GENDER_FILE = DEST_PATH_FROM_ROOT / "location_age_gender_distr.ftr"


def parse_location_age_gender_dataset():
    """Refactor columns, data to english,
    melt parallel gender amount columns in order to have single weights column"""
    df = pd.read_csv(SOURCE_LOC_AGE_GENDER_FILE)
    df = (
        df.drop(
            columns=[col for col in df if col not in HEADER_TRANSFORMATION_TABLE.keys()]
        )
        .rename(columns=HEADER_TRANSFORMATION_TABLE)
        .melt(id_vars=["area", "age"], var_name="gender", value_name="amount")
        .replace({"gender": {"men": "man", "women": "woman"}})
    )
    df = df.drop(df[(df["amount"] == 0)].index)
    df = convert_amount_column_to_weight(df)
    df.reset_index().to_feather(DEST_LOC_AGE_GENDER_FILE)
