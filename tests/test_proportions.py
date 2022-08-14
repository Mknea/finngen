import random
from typing import List

import pytest
from pandas import DataFrame

from finngen import Gender, Person, create_finnish_people

PRESET_LOCATION_AGE_GENDER = {
    "area": ["Akaa", "Äänekoski"],
    "age": [20, 50],
    "gender": ["male", "female"],
    "weight": [0.4, 0.6],
}
PRESET_LAST_NAMES = {"last_name": ["McLastname", "Lasterburg"], "weight": [0.2, 0.8]}
PRESET_MENS_FIRST_NAMES = {"first_name": ["Testy", "Batman"], "weight": [0.1, 0.9]}
PRESET_MENS_MIDDLE_NAMES = {"middle_name": ["Middly", "MidMid"], "weight": [0.4, 0.6]}

PRESET_WOMENS_FIRST_NAMES = {"first_name": ["Päivi", "Batwoman"], "weight": [0.3, 0.7]}
PRESET_WOMENS_MIDDLE_NAMES = {
    "middle_name": ["Womiddly", "Dagger"],
    "weight": [0.55, 0.45],
}

PERCENTAGE_OF_MEN_IN_SOURCE = PRESET_LOCATION_AGE_GENDER["weight"][0]  # type: ignore


@pytest.fixture
def mocked_source_data(monkeypatch):
    mocked_data = {
        "location_age_gender": PRESET_LOCATION_AGE_GENDER,
        "last_names": PRESET_LAST_NAMES,
        "men_first_names": PRESET_MENS_FIRST_NAMES,
        "men_middle_names": PRESET_MENS_MIDDLE_NAMES,
        "women_first_names": PRESET_WOMENS_FIRST_NAMES,
        "women_middle_names": PRESET_WOMENS_MIDDLE_NAMES,
    }
    mocked_data.update((k, DataFrame.from_dict(v)) for k, v in mocked_data.items())
    monkeypatch.setattr("finngen.SOURCE_DATA", mocked_data)


@pytest.fixture
def generated_finns(mocked_source_data):
    random.seed(0)
    return create_finnish_people(amount=10000)


def count_amount_with_field_value(container, field_name, accepted_value):
    return len([item for item in container if getattr(item, field_name) == accepted_value])


# FIXME: Refactor mocked data access
def test_gender_is_assigned_in_set_proportions(generated_finns: List[Person]):
    count_of_generated_men = count_amount_with_field_value(generated_finns, "gender", Gender.Male)
    expected_amount_of_men = len(generated_finns) * PERCENTAGE_OF_MEN_IN_SOURCE
    assert count_of_generated_men == pytest.approx(expected_amount_of_men, rel=1e-1)


def test_names_are_assigned_in_set_proportions(generated_finns: List[Person]):
    count_of_specific_men_first_name = count_amount_with_field_value(
        generated_finns, "first_name", PRESET_MENS_FIRST_NAMES["first_name"][0]  # type: ignore
    )
    assert count_of_specific_men_first_name == pytest.approx(
        len(generated_finns)
        * PERCENTAGE_OF_MEN_IN_SOURCE
        * PRESET_MENS_FIRST_NAMES["weight"][0],  # type: ignore
        rel=1e-1,
    )

    count_of_specific_women_middle_name = count_amount_with_field_value(
        generated_finns,
        "middle_name",
        PRESET_WOMENS_MIDDLE_NAMES["middle_name"][1],  # type: ignore
    )
    assert count_of_specific_women_middle_name == pytest.approx(
        len(generated_finns)
        * (1 - PERCENTAGE_OF_MEN_IN_SOURCE)
        * PRESET_WOMENS_MIDDLE_NAMES["weight"][1],  # type: ignore
        rel=1e-1,
    )


def test_first_and_middle_names_are_tied_to_gender(generated_finns: List[Person]):
    for person in generated_finns:
        if person.gender == Gender.Male:
            assert person.first_name in PRESET_MENS_FIRST_NAMES["first_name"]  # type: ignore
            assert person.middle_name in PRESET_MENS_MIDDLE_NAMES["middle_name"]  # type: ignore
        else:
            assert person.first_name in PRESET_WOMENS_FIRST_NAMES["first_name"]  # type: ignore
            assert person.middle_name in PRESET_WOMENS_MIDDLE_NAMES["middle_name"]  # type: ignore
