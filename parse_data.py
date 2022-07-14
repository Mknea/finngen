from scripts.avoindata import parse_first_name_dataset, parse_last_name_dataset


def parse_all_datasets():
    parse_first_name_dataset()
    parse_last_name_dataset()


# TODO: Add handle to save in CSV
if __name__ == "__main__":
    parse_all_datasets()
