from pathlib import Path
from typing import List

import pandas


def read_dataset(dataset_dirpath: str) -> List[pandas.DataFrame]:
    dataset_dir = Path(dataset_dirpath)

    dataset: List[pandas.DataFrame] = []
    for filename in dataset_dir.iterdir():
        if filename.suffix == ".csv":
            data: pandas.DataFrame = pandas.read_csv(filename, skiprows=1)
            dataset.append(data)

    return dataset


def prepare_dataset(dataset: List[pandas.DataFrame]) -> pandas.DataFrame:
    ds = pandas.concat(dataset)
    column_mapping = {
        "Seriennummer": "serial_number",
        "Gerätezeitstempel": "device_timestamp",
        "Glukosewert-Verlauf mg/dL": "glucose_value_mgdl",
    }

    return ds[list(column_mapping.keys())].rename(columns=column_mapping)


def load_dataset() -> pandas.DataFrame:
    sample_data_dir = "sample-data"
    dataset = read_dataset(sample_data_dir)
    return prepare_dataset(dataset)
