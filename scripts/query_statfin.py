import json
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

QUERYS_PATH = Path.cwd() / "scripts" / "querys"

DEST_PATH = Path.cwd() / "data" / "source" / "statfin"


def fetch_location_age_and_gender_distribution_data():
    request_and_save_to_csv(
        "location_age_gender_distr",
        "11re -- Väestö iän (1-v.) ja sukupuolen mukaan alueittain, 1972-2021 - 2020",
    )


def request_and_save_to_csv(query_file_name: str, dest_file_name: str):
    response = request_data_from_statsfinn(QUERYS_PATH / f"{query_file_name}.json")
    with open(DEST_PATH / f"{dest_file_name}.csv", mode="w") as w_file:
        w_file.write(response.text)


def request_data_from_statsfinn(query_file_path: Path):
    """Note to request response data in query in CSV format"""
    with open(query_file_path, mode="r") as file:
        preset = json.load(file)
        response = requests.post(url=preset["url"], json=preset["query"])
        if response.status_code != 200:
            raise Exception(
                f"Request to {preset['url']} failed!\n"
                f"Status code: {response.status_code}, {response.reason}\n"
                f"Source file: {query_file_path}"
            )
        return response


def inspect_res(res):
    df = pd.read_csv(StringIO(res.text))
    print(df)
    breakpoint()  # noqa: T100
