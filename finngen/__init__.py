__version__ = "0.1.0"

"""
Generate statistically (somewhat) accurate instances of finnish people!
"""

from dataclasses import dataclass
from enum import Enum
from random import choices
from typing import List

from . import _storage, _utils


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"


@dataclass
class Person:
    gender: Gender
    first_name: str
    middle_name: str
    last_name: str

    @property
    def full_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name


SOURCE_DATA = {
    key: _storage.load_data_file(f"{key}.csv")
    for key in (
        "last_names",
        "men_first_names",
        "men_middle_names",
        "women_first_names",
        "women_middle_names",
    )
}


def _generate(k: int = 1) -> List[Person]:

    # It's expensive to setup choices: Initialize them as little times as possible
    gender_choices = choices(
        [Gender.Female, Gender.Male], [0.5, 0.5], k=k
    )  # TODO: add sophistication
    persons = []
    for gender_choice in gender_choices:
        data = {"gender": gender_choice}
        prefix = "men" if gender_choice == Gender.Male else "women"
        for frame_key, data_key in (
            ("last_names", "last name"),
            (f"{prefix}_first_names", "first name"),
            (f"{prefix}_middle_names", "middle name"),
        ):
            df = SOURCE_DATA[frame_key]
            choice = choices(df[data_key], df["weight"])
            data_key = data_key.replace(" ", "_")
            data[data_key] = choice
        persons.append(_utils.DataClassUnpack.instantiate(Person, data))
    return persons


def generate_finnish_person() -> Person:
    return _generate(k=1)[0]


def generate_finnish_people(amount: int) -> List[Person]:
    if amount == 0:
        return []
    elif amount < 0:
        raise ValueError("Cannot generate negative amount of people!")
    return _generate(k=amount)
