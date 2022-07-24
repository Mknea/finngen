import random
from collections import Counter
from typing import List

import pytest
from pandas import DataFrame

from finngen import Gender, Person, create_finnish_people

PRESET_LAST_NAMES = {"last_name": ["McLastname", "Lasterburg"], "weight": [0.2, 0.8]}
PRESET_MENS_FIRST_NAMES = {"first_name": ["Testy", "Batman"], "weight": [0.1, 0.9]}
PRESET_MENS_MIDDLE_NAMES = {"middle_name": ["Middly", "MidMid"], "weight": [0.4, 0.6]}

PRESET_WOMENS_FIRST_NAMES = {"first_name": ["Päivi", "Batwoman"], "weight": [0.3, 0.7]}
PRESET_WOMENS_MIDDLE_NAMES = {
    "middle_name": ["Womiddly", "Dagger"],
    "weight": [0.55, 0.45],
}


@pytest.fixture
def mocked_source_data(monkeypatch):
    monkeypatch.setattr(
        "finngen.SOURCE_DATA",
        {
            "last_names": DataFrame.from_dict(PRESET_LAST_NAMES),
            "men_first_names": DataFrame.from_dict(PRESET_MENS_FIRST_NAMES),
            "men_middle_names": DataFrame.from_dict(PRESET_MENS_MIDDLE_NAMES),
            "women_first_names": DataFrame.from_dict(PRESET_WOMENS_FIRST_NAMES),
            "women_middle_names": DataFrame.from_dict(PRESET_WOMENS_MIDDLE_NAMES),
        },
    )


@pytest.fixture
def generated_finns(mocked_source_data):
    random.seed(0)
    return create_finnish_people(amount=10000)


def sum_counter_counts_of_values(counter, field, accepted_values):
    return sum(
        [
            count
            for val, count in counter.items()
            if getattr(val, field) in accepted_values
        ]
    )


def test_gender_is_assigned_in_equal_proportion(generated_finns: List[Person]):
    counts = Counter(generated_finns)
    count_of_men = sum_counter_counts_of_values(counts, "gender", Gender.Male)
    assert count_of_men == pytest.approx(len(generated_finns) / 2, rel=5e-3)


def test_names_are_assigned_in_set_proportions(generated_finns: List[Person]):
    counts = Counter(generated_finns)
    count_of_specific_men_first_name = sum_counter_counts_of_values(
        counts, "first_name", [PRESET_MENS_FIRST_NAMES["first_name"][0]]  # type: ignore
    )
    assert count_of_specific_men_first_name == pytest.approx(
        len(generated_finns)
        * 0.5
        * PRESET_MENS_FIRST_NAMES["weight"][0],  # type: ignore
        rel=1e-1,
    )

    count_of_specific_women_middle_name = sum_counter_counts_of_values(
        counts,
        "middle_name",
        [PRESET_WOMENS_MIDDLE_NAMES["middle_name"][1]],  # type: ignore
    )
    assert count_of_specific_women_middle_name == pytest.approx(
        len(generated_finns)
        * 0.5
        * PRESET_WOMENS_MIDDLE_NAMES["weight"][1],  # type: ignore
        rel=1e-1,
    )
