from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from finngen._storage import load_data_file
from finngen.constants import SOURCE_FILES_TO_COLUMNS


@patch("pandas.read_feather")
def test_load_data_file(mocked_read_feather: Mock) -> None:
    fake_file = "this-does-not-actually-exist.asd"
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
