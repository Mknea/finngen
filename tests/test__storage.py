import sys
from pathlib import Path
from unittest.mock import Mock, patch

from importlib_resources import path

from finngen._storage import load_data_file


@patch("pandas.read_feather")
def test_load_data_file(mocked_read_feather: Mock):
    fake_file = "this-does-not-actually-exist.asd"
    if sys.version_info < (3, 10):
        # Behaviour changes between versions, patch to backported version
        # https://bugs.python.org/issue44137
        with patch("finngen._storage.path", side_effect=path):
            load_data_file(fake_file)
    else:
        load_data_file(fake_file)
    mocked_read_feather.assert_called_once_with(Path.cwd() / "finngen" / "data" / fake_file)
