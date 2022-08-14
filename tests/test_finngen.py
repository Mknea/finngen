from datetime import datetime
from unittest.mock import Mock, patch

import numpy as np
import pytest
from freezegun import freeze_time

from finngen import (
    Gender,
    Person,
    __version__,
    create_finnish_people,
    create_finnish_person,
    generate_finnish_people,
)


def test_version():
    assert __version__ == "0.1.0"


def test_zero_people_generation():
    for _ in generate_finnish_people(amount=0):
        pytest.fail("Should not loop empty generator!")
    assert [] == create_finnish_people(0)


def test_fail_on_negative_people_generation():
    for func in (create_finnish_people, generate_finnish_people):
        with pytest.raises(ValueError) as cm:
            func(amount=-5)
        assert "Cannot generate negative amount of people!" in str(cm._excinfo)


def assert_valid_person_with_valid_fields(person):
    assert type(person) is Person
    for field, expected_type in [
        ("residence", str),
        ("age", (int, np.integer)),
        ("gender", Gender),
        ("first_name", str),
        ("middle_name", str),
        ("last_name", str),
        ("full_name", str),
    ]:
        assert hasattr(person, field)
        assert isinstance(getattr(person, field), expected_type)


def test_single_person_creation():
    person = create_finnish_person()
    assert_valid_person_with_valid_fields(person)


def test_people_creation():
    people = create_finnish_people(amount=100)
    assert 100 == len(people)
    assert_valid_person_with_valid_fields(people[50])


def test_people_generation():
    people = [x for x in generate_finnish_people(amount=100)]
    assert 100 == len(people)
    assert_valid_person_with_valid_fields(people[50])


# --------- Test properties ----------------


def create_person(**kwargs):
    """Create person for tests with default fields filled"""
    return Person(
        **{
            **{
                "residence": "asd-municipality",
                "age": 5,
                "gender": Gender.Female,
                "first_name": "Testy",
                "middle_name": "asd",
                "last_name": "LastNamy",
            },
            **kwargs,
        }
    )


@freeze_time(datetime(2022, 6, 25))
@patch("finngen.randint")
@pytest.mark.parametrize("age, expected_birth_year", [(1, 2021), (16, 2006), (100, 1922)])
def test_birthday_basic_case_generation(mock_randint: Mock, age: int, expected_birth_year: int):
    mocked_delta_randint = 5
    mock_randint.return_value = mocked_delta_randint
    person = create_person(age=age)
    assert (
        datetime(year=expected_birth_year, month=1, day=mocked_delta_randint + 1).date()
        == person.birthday
    )


@freeze_time(datetime(2000, 1, 10))
@patch("finngen.randint")
def test_birthday_born_in_current_year(mock_randint: Mock):
    """Should generate date only up to current day"""
    mocked_delta_randint = 7
    mock_randint.return_value = mocked_delta_randint
    person = create_person(age=0)
    assert datetime(year=2000, month=1, day=mocked_delta_randint + 1).date() == person.birthday
    mock_randint.assert_called_once_with(0, 10 - 1)
