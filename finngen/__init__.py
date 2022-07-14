__version__ = "0.1.0"


from dataclasses import dataclass
from enum import Enum
from random import choices
from typing import List


class Gender(Enum, str):
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


def _generate(k: int = 1) -> Person:

    # It's expensive to setup choices: Initialize them as little times as possible
    gender_choices = choices(
        [Gender.Female, Gender.Male], [0.5, 0.5], k=k
    )  # TODO: add sophistication
    for gender_choice in gender_choices:
        pass


def generate_finnish_person() -> Person:
    return _generate(k=1)


def generate_finnish_people(amount: int) -> List[Person]:
    if amount == 0:
        return []
    elif amount < 0:
        raise ValueError("Cannot generate negative amount of people!")
    return _generate(k=amount)
