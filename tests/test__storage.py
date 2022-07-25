from pathlib import Path
from unittest.mock import Mock, patch

from finngen._storage import load_data_file


@patch("pandas.read_feather")
def test_load_data_file(mocked_read_feather: Mock):
    fake_file = "this-does-not-actually-exist.asd"
    load_data_file(fake_file)
    mocked_read_feather.assert_called_once_with(
        Path.cwd() / "finngen" / "data" / fake_file
    )
