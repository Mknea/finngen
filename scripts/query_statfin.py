import json
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

QUERYS_PATH = Path.cwd() / "scripts" / "querys"

DEST_PATH = Path.cwd() / "data" / "source" / "statfin"


def fetch_location_age_and_gender_distribution_data():
    response = request_data_from_statsfinn(
        QUERYS_PATH / "location_age_gender_distr.json"
    )
    df = pd.read_csv(StringIO(response.text))
    print(df)
    with open(DEST_PATH / "location_age_gender_distr.csv", mode="w") as w_file:
        w_file.write(response.text)


def request_data_from_statsfinn(query_file_path: Path):
    """Note to request it in CSV"""
    with open(query_file_path, mode="r") as file:
        preset = json.load(file)
        response = requests.post(url=preset["url"], json=preset["query"])
        if code := response.status_code != 200:
            raise Exception(
                f"Request to {preset['url']} failed \
                with status code: {code}, {response.reason}"
            )
        return response
