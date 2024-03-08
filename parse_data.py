import argparse

from scripts.parse_avoindata import parse_first_name_dataset, parse_last_name_dataset
from scripts.parse_statfin import parse_location_age_gender_dataset
from scripts.query_statfin import fetch_location_age_and_gender_distribution_data


def fetch_source_data_from_statfin():
    fetch_location_age_and_gender_distribution_data()


def parse_all_datasets():
    parse_location_age_gender_dataset()
    parse_first_name_dataset()
    parse_last_name_dataset()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Parse and transform source data in data/source/"
            "into data files used by the package in finngen/data/"
        )
    )
    parser.add_argument(
        "-f",
        "--fetch",
        help="fetch fresh data from statfin in addition to parsing all source data",
        action="store_true",
    )
    args = parser.parse_args()

    green_text = lambda x: f"\033[92m{x}\033[00m"  # noqa: E731
    print_with_arrow = lambda x: print(f"-> {x}")  # noqa: E731

    if args.fetch:
        print_with_arrow("Fetching datasets from Statfin...")
        fetch_source_data_from_statfin()
        print_with_arrow(green_text("New data fetched and stored!"))

    print_with_arrow("Parsing datasets in data/source/ to finngen/data/...")
    parse_all_datasets()
    print_with_arrow(green_text("Parsed all datasets successfully!"))
