# Finngen

<!-- Badges -->

![CI status](https://github.com/mknea/finngen/actions/workflows/lint_and_test.yaml/badge.svg)
![Supported python versions](https://img.shields.io/badge/-Python%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)

Finngen is a library for generating more statistically believable instances of finnish people's personal data.

Persons are generated from datasets made publicly available by Finnish governmental agencies.

## Usage

```python
>>> from finngen import create_finnish_person
>>> create_finnish_person()
Person(
    residence='Lempäälä',
    age=18,
    gender=<Gender.Female: 'Female'>,
    first_name='Jenna',
    middle_name='Anneli',
    last_name='Nousiainen'
)
```

Generate any number of people:

```python
>>> from finngen import create_finnish_people
>>> create_finnish_people(10000)
[
    Person(
        residence='Jyväskylä',
        age=39,
        gender=<Gender.Male: 'Male'>,
        first_name='Joel',
        middle_name='Olavi',
        last_name='Laari'
    ),
    Person(
        residence='Hämeenlinna',
        age=19,
        gender=<Gender.Female: 'Female'>,
        first_name='Hilkka',
        middle_name='Kaarina',
        last_name='Roivanen'
    ),
    ...
]
```

Some fields are only generated when first accessed:

```python traceback
>>> from finngen import create_finnish_person
>>> finn = create_finnish_person()
>>> finn
Person(
    residence='Porvoo',
    age=45,
    gender=<Gender.Male: 'Male'>,
    first_name='Alex',
    middle_name='Tapani',
    last_name='Kupari'
)

>>> finn.birthday
datetime.date(1977, 11, 15)

>>> finn.personal_identity_code
'151177-223L'

>>> finn
Person(
    residence='Porvoo',
    age=45,
    gender=<Gender.Male: 'Male'>,
    first_name='Alex',
    middle_name='Tapani',
    last_name='Kupari',
    birthday=datetime.date(1977, 11, 15),
    personal_identity_code='151177-223L'
)
```

## Installation

To install Finngen, simply:

```bash
$ pip install finngen
```

## How it works

### In brief

`age`, `gender` and `residence` combinations are first generated based on the weight's in the respective dataset. Then `fist_name`, `middle_name` and `last_name` combinations are generated from name datasets based on the amount of each gender from previous step. Finally the data are combined into dataclass instances.

The `birthday` and `personal_identity_code` properties are generated on the first access.
`birthday` is generated backwards from the age, with random date from the birth year. If the birth year is the current one, the date is only generated up to current date.
`personal_identity_code` is generated based on gender, birthday and random number (for the individual number).

### Simplifications

### Age, location and gender datasets:

- Dataset combines all over 100 years old persons to one group
- Do not include non-binary or other genders as category
- Age is defined as the number of whole years person has lived at the last day of the year

### Name datasets:

- Do not include non-binary or other genders as category
- Do not include first names with less than 5 holders, or last names with less than 20 holders
- Data on the relation of first to middle name combinations does not exist in the dataset
- Middle name counts are likely skewed as the number of middle names of individuals in Finland varies

### Data generation rules:

- As it is expensive to setup `random.choice`, both gender's names are generated at once and then paired to the name + gender + location combinations
- The point above means that the generated persons are ordered by gender. Consider generating people with `create_finnish_people(.., shuffled=True)` flag if the order needs to be random
- Each generated person has one middle name, in reality one can have multiple or no middle names

### Development

its recommended to use some python version manager, like `pyenv` / `asdf`.

The used dependency management tool is `poetry`.
Refer to its instructions in installation.

Activate virtual env:

```bash
$ poetry shell
```

Install dependencies and git hooks:

```bash
$ poetry install # Creates the virtual env based on pyproject.toml
$ poetry run pre-commit install
```

Run tests:

```bash
$ pytest
```

For all supported python versions:

```bash
$ tox
```

Manually deploying to test pypi:

```bash
# If not set, add token
poetry config pypi-token.test-pypi <pypi-YYYYYYYY>
# Point to test pypi
poetry config repositories.test-pypi https://test.pypi.org/legacy/
```
First up the version
```bash
poetry version prerelease
# or
poetry version patch
```

```bash
poetry build
poetry publish -r test-pypi
```
