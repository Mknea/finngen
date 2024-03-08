import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from importlib_resources import path

from finngen._storage import load_data_file
from finngen.constants import SOURCE_FILES_TO_COLUMNS


@patch("pandas.read_feather")
def test_load_data_file(mocked_read_feather: Mock) -> None:
    fake_file = "this-does-not-actually-exist.asd"
    if sys.version_info < (3, 10):
        # Behaviour changes between versions, patch to backported version
        # https://bugs.python.org/issue44137
        with patch("finngen._storage.path", side_effect=path):
            load_data_file(fake_file)
    else:
        load_data_file(fake_file)
    mocked_read_feather.assert_called_once_with(Path.cwd() / "finngen" / "data" / fake_file)


@pytest.mark.parametrize(
    "file_name",
    SOURCE_FILES_TO_COLUMNS.keys(),
)
def test_expected_files_really_exist(file_name: str) -> None:
    assert (Path.cwd() / "finngen" / "data" / f"{file_name}.ftr").exists()


@pytest.mark.parametrize(
    "file_name",
    SOURCE_FILES_TO_COLUMNS.keys(),
)
def test_expected_feather_headers(file_name: str) -> None:
    data = load_data_file(f"{file_name}.ftr")
    assert set(data.columns.tolist()).issuperset(SOURCE_FILES_TO_COLUMNS[file_name])
