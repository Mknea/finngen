from enum import Enum
from importlib import resources

import pandas as pd

from . import data


class DataFileType(str, Enum):
    feather = "fth"
    csv = "csv"


def read_data_file(file_name: str, file_type: DataFileType) -> pd.DataFrame:
    with resources.path(data, file_name + "." + file_type) as cm:
        reader = pd.read_feather if file_type == DataFileType.feather else pd.read_csv
        return reader(cm)  # type: ignore
