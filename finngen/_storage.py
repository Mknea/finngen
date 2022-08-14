from importlib.resources import path

import pandas as pd

from . import data


def load_data_file(file_name: str) -> pd.DataFrame:
    with path(data, file_name) as cm:
        return pd.read_feather(cm)
