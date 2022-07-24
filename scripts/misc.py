from pathlib import Path

import pandas as pd

SOURCE_PATH_FROM_ROOT = Path.cwd() / "data" / "source"
DEST_PATH_FROM_ROOT = Path.cwd() / "finngen" / "data"


def convert_amount_column_to_weight(df: pd.DataFrame) -> pd.DataFrame:
    total = df["amount"].sum()
    df["weight"] = df["amount"] / total
    return df.drop("amount", axis=1)
