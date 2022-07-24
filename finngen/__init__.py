__version__ = "0.1.0"

"""
Generate statistically (somewhat) accurate instances of finnish people!
"""

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from random import choices
from typing import Iterator, List, Literal, Sequence, Tuple, cast

from . import _storage


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"

    @classmethod
    def from_str(cls, label: str):
        if label.lower() == "male":
            return cls.Male
        elif label.lower() == "female":
            return cls.Female
        else:
            raise NotImplementedError


@dataclass(eq=True, frozen=True)
class Person:
    residence: str
    age: int
    gender: Gender
    first_name: str
    middle_name: str
    last_name: str

    @property
    def full_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name


SOURCE_DATA = {
    key: _storage.load_data_file(f"{key}.ftr")
    for key in (
        "location_age_gender",
        "last_names",
        "men_first_names",
        "men_middle_names",
        "women_first_names",
        "women_middle_names",
    )
}


def _generate(k: int = 1) -> Iterator[Person]:

    # It's expensive to setup choices:
    # Generate fields per dataset as few times as possible and just pair them at the end
    residence_age_genders = _create_residence_age_gender(k)
    residence_age_genders = sorted(
        residence_age_genders, key=lambda x: x[2], reverse=True
    )
    counts_per_gender = Counter(x[2] for x in residence_age_genders)

    last_names: List[str] = choices(
        SOURCE_DATA["last_names"]["last_name"],
        cast(Sequence[float], SOURCE_DATA["last_names"]["weight"]),
        k=k,
    )
    first_names: List[str] = []
    middle_names: List[str] = []
    for gender, amount in counts_per_gender.items():
        first_names.extend(_create_names_based_on_gender(gender, amount, "first"))
        middle_names.extend(_create_names_based_on_gender(gender, amount, "middle"))

    for (residence, age, gender), last_name, first_name, middle_name in zip(
        residence_age_genders, last_names, first_names, middle_names, strict=True
    ):
        yield Person(
            residence=residence,
            age=age,
            gender=Gender.from_str(gender),
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )


def _create_residence_age_gender(amount: int) -> List[Tuple[str, int, str]]:
    df = SOURCE_DATA["location_age_gender"]
    return choices(
        df[["area", "age", "gender"]].to_records(index=False),
        cast(Sequence[float], df["weight"]),
        k=amount,
    )


def _create_names_based_on_gender(
    gender: str, amount: int, name_type: Literal["first"] | Literal["middle"]
) -> List[str]:
    prefix = "men" if Gender.from_str(gender) == Gender.Male else "women"
    df = SOURCE_DATA[f"{prefix}_{name_type}_names"]
    return choices(
        df[f"{name_type}_name"], cast(Sequence[float], df["weight"]), k=amount
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
