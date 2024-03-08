from importlib.resources import as_file, files

import pandas as pd

from . import data


def load_data_file(file_name: str) -> pd.DataFrame:
    source = files(data).joinpath(file_name)
    with as_file(source) as file_path:
        return pd.read_feather(file_path)
