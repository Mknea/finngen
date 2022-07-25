__version__ = "0.1.0"

"""
Generate statistically (somewhat) accurate instances of finnish people!
"""

import calendar
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from random import choices, randint
from typing import Iterator, List, Literal, Optional, Sequence, Tuple, cast

from . import _storage


class Gender(str, Enum):
    """Available genders from source data"""

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


@dataclass(eq=True)
class Person:
    """

    `birthday` is computed property, randomly generated only once from age on access:
    >>> person = create_finnish_person()
    >>> person.age
    58
    >>> person.birthday
    datetime.date(1964, 11, 4)
    """

    residence: str
    age: int
    gender: Gender
    first_name: str
    middle_name: str
    last_name: str
    _birthday: Optional[date] = field(init=False, repr=False, default=None)

    @property
    def full_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

    @property
    def birthday(self):
        if self._birthday is None:
            birth_year = (datetime.utcnow() - timedelta(weeks=52 * int(self.age))).date().year
            days_in_that_year = 365 + calendar.isleap(birth_year)
            self._birthday = date(birth_year, 1, 1) + timedelta(
                days=randint(0, days_in_that_year - 1)
            )
        return self._birthday


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


def _generate(amount: int = 1) -> Iterator[Person]:

    # It's expensive to setup choices:
    # Generate fields per dataset as few times as possible and just pair them at the end
    residence_age_genders = _create_residence_age_gender(amount)
    residence_age_genders = sorted(residence_age_genders, key=lambda x: x[2], reverse=True)

    counts_per_gender = Counter(x[2] for x in residence_age_genders)
    last_names, first_names, middle_names = _create_all_names(counts_per_gender)

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


def _create_all_names(
    counts_per_gender: Counter[str],
) -> Tuple[List[str], List[str], List[str]]:
    last_names: List[str] = choices(
        SOURCE_DATA["last_names"]["last_name"],
        cast(Sequence[float], SOURCE_DATA["last_names"]["weight"]),
        k=sum(counts_per_gender.values()),
    )
    first_names: List[str] = []
    middle_names: List[str] = []
    for gender, amount in counts_per_gender.items():
        first_names.extend(_create_names_based_on_gender(gender, amount, "first"))
        middle_names.extend(_create_names_based_on_gender(gender, amount, "middle"))
    return last_names, first_names, middle_names


def _create_names_based_on_gender(
    gender: str, amount: int, name_type: Literal["first"] | Literal["middle"]
) -> List[str]:
    prefix = "men" if Gender.from_str(gender) == Gender.Male else "women"
    df = SOURCE_DATA[f"{prefix}_{name_type}_names"]
    return choices(df[f"{name_type}_name"], cast(Sequence[float], df["weight"]), k=amount)


def generate_finnish_people(amount: int) -> Iterator[Person]:
    if amount == 0:
        return iter(())
    elif amount < 0:
        raise ValueError("Cannot generate negative amount of people!")
    return _generate(amount=amount)


def create_finnish_person() -> Person:
    return next(_generate(amount=1))


def create_finnish_people(amount: int) -> List[Person]:
    return list(generate_finnish_people(amount=amount))
