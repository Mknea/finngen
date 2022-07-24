"""
Name datasets are only available as xlsx files.
Parse them to CSV for simpler & more efficient access.
"""
from pathlib import Path
from typing import Dict

import pandas as pd

from scripts.misc import (
    DEST_PATH_FROM_ROOT,
    SOURCE_PATH_FROM_ROOT,
    convert_amount_column_to_weight,
)

AVOINDATA_SOURCE_DIR = SOURCE_PATH_FROM_ROOT / "avoindata"
FIRST_NAMES_FILE = AVOINDATA_SOURCE_DIR / "etunimitilasto-2022-02-07-dvv.xlsx"
MENS_FIRST_NAMES_SHEET = "Miehet ens"
MENS_MIDDLE_NAMES_SHEET = "Miehet muut"

FEMALES_FIRST_NAMES_SHEET = "Naiset ens"
FEMALES_MIDDLE_NAMES_SHEET = "Naiset muut"

LAST_NAMES_FILE = AVOINDATA_SOURCE_DIR / "sukunimitilasto-2022-02-07-dvv.xlsx"
LAST_NAMES_SHEET = "Nimet"

DEST_MENS_FIRST_NAMES_FILE = DEST_PATH_FROM_ROOT / "men_first_names.csv"
DEST_MENS_MIDDLE_NAMES_FILE = DEST_PATH_FROM_ROOT / "men_middle_names.csv"

DEST_WOMENS_FIRST_NAMES_FILE = DEST_PATH_FROM_ROOT / "women_first_names.csv"
DEST_WOMENS_MIDDLE_NAMES_FILE = DEST_PATH_FROM_ROOT / "women_middle_names.csv"

DEST_LAST_NAMES_FILE = DEST_PATH_FROM_ROOT / "last_names.csv"

# TODO: take in save format as param
# As default save in feather file format, not CSV


def parse_first_name_dataset():
    for source_sheet, dest_file, name_type in [
        (MENS_FIRST_NAMES_SHEET, DEST_MENS_FIRST_NAMES_FILE, "first"),
        (MENS_MIDDLE_NAMES_SHEET, DEST_MENS_MIDDLE_NAMES_FILE, "middle"),
        (FEMALES_FIRST_NAMES_SHEET, DEST_WOMENS_FIRST_NAMES_FILE, "first"),
        (FEMALES_MIDDLE_NAMES_SHEET, DEST_WOMENS_MIDDLE_NAMES_FILE, "middle"),
    ]:
        _parse_name_excel(
            FIRST_NAMES_FILE,
            source_sheet,
            {"Etunimi": f"{name_type} name", "Lukumäärä": "amount"},
            dest_file,
        )


def parse_last_name_dataset():
    _parse_name_excel(
        LAST_NAMES_FILE,
        LAST_NAMES_SHEET,
        {"Sukunimi": "last name", "Yhteensä": "amount"},
        DEST_LAST_NAMES_FILE,
    )


def _parse_name_excel(
    source_file: Path, sheet_name: str, rename_columns: Dict[str, str], dest_file: Path
):
    df: pd.DataFrame = pd.read_excel(str(source_file), sheet_name=sheet_name)
    df = df.rename(columns=rename_columns)
    df = convert_amount_column_to_weight(df)
    df.to_csv(dest_file, index=False)
