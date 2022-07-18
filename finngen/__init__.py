__version__ = "0.1.0"

"""
Generate statistically (somewhat) accurate instances of finnish people!
"""

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from random import choices
from typing import Iterator, List, Literal, Sequence, cast

from . import _storage


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


def _generate(k: int = 1) -> Iterator[Person]:

    # It's expensive to setup choices:
    # Initialize non-gender related once, gender related once per gender
    gender_choices = choices(
        [Gender.Female, Gender.Male], [0.5, 0.5], k=k
    )  # TODO: add sophistication
    gender_choices.sort()
    counts = Counter(gender_choices)

    last_names: List[str] = choices(
        SOURCE_DATA["last_names"]["last name"],
        cast(Sequence[float], SOURCE_DATA["last_names"]["weight"]),
        k=k,
    )
    first_names: List[str] = []
    middle_names: List[str] = []
    for gender, amount in counts.items():
        first_names.extend(_generate_names_based_on_gender(gender, amount, "first"))
        middle_names.extend(_generate_names_based_on_gender(gender, amount, "middle"))

    for gender, last_name, first_name, middle_name in zip(
        gender_choices, last_names, first_names, middle_names, strict=True
    ):
        yield Person(
            gender=gender,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )


def _generate_names_based_on_gender(
    gender: Gender, amount: int, name_type: Literal["first"] | Literal["middle"]
) -> List[str]:
    prefix = "men" if gender == Gender.Male else "women"
    df = SOURCE_DATA[f"{prefix}_{name_type}_names"]
    return choices(
        df[f"{name_type} name"], cast(Sequence[float], df["weight"]), k=amount
    )


def generate_finnish_people(amount: int) -> Iterator[Person]:
    if amount == 0:
        return iter(())
    elif amount < 0:
        raise ValueError("Cannot generate negative amount of people!")
    return _generate(k=amount)


def create_finnish_person() -> Person:
    return next(_generate(k=1))


def create_finnish_people(amount: int) -> List[Person]:
    return list(generate_finnish_people(amount=amount))
