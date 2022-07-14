"""
Name datasets are only available as xlsx files.
Parse them to CSV for simpler & more efficient access.
"""
from pathlib import Path

import pandas as pd

SOURCE_PATH_FROM_ROOT = Path.cwd() / "data" / "source" / "avoindata"
FIRST_NAMES_FILE = SOURCE_PATH_FROM_ROOT / "etunimitilasto-2022-02-07-dvv.xlsx"
MENS_FIRST_NAMES_SHEET = "Miehet ens"
MENS_MIDDLE_NAMES_SHEET = "Miehet muut"

FEMALES_FIRST_NAMES_SHEET = "Naiset ens"
FEMALES_MIDDLE_NAMES_SHEET = "Naiset muut"

LAST_NAMES_FILE = SOURCE_PATH_FROM_ROOT / "sukunimitilasto-2022-02-07-dvv.xlsx"
LAST_NAMES_SHEET = "Nimet"

DEST_PATH_FROM_ROOT = Path.cwd() / "data" / "avoindata"
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
        first_names_sheet: pd.DataFrame = pd.read_excel(
            FIRST_NAMES_FILE,
            sheet_name=source_sheet,
        )
        first_names_sheet.rename(
            columns={"Etunimi": f"{name_type} name", "Lukumäärä": "amount"},
            inplace=True,
        )
        first_names_sheet.to_csv(dest_file, index=False)


def parse_last_name_dataset():
    last_names_sheet: pd.DataFrame = pd.read_excel(
        LAST_NAMES_FILE, sheet_name=LAST_NAMES_SHEET
    )
    last_names_sheet.rename(
        columns={"Sukunimi": "last name", "Yhteensä": "amount"}, inplace=True
    )
    last_names_sheet.to_csv(DEST_LAST_NAMES_FILE, index=False)
