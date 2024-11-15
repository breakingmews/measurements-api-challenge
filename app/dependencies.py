import logging
from pathlib import Path
from typing import List

import pandas as pd
from fastapi import Request

_log = logging.getLogger(__name__)


def read_dataset(dataset_dirpath: str) -> List[pd.DataFrame]:
    dataset_dir = Path(dataset_dirpath)

    dataset: List[pd.DataFrame] = []
    for filename in dataset_dir.iterdir():
        if filename.suffix == ".csv":
            data: pd.DataFrame = pd.read_csv(filename, skiprows=1)
            dataset.append(data)
    return dataset


def prepare_dataset(dataset: List[pd.DataFrame]) -> pd.DataFrame:
    ds = pd.concat(dataset)
    column_mapping = {
        "Seriennummer": "serial_number",
        "Gerätezeitstempel": "device_timestamp",
        "Glukosewert-Verlauf mg/dL": "glucose_value_mgdl",
    }
    ds = ds[list(column_mapping.keys())]
    ds = ds.rename(columns=column_mapping)
    return ds


async def load_dataset() -> pd.DataFrame:
    _log.info("Loading dataset")
    sample_data_dir = "sample-data"

    dataset = read_dataset(sample_data_dir)
    dataset = prepare_dataset(dataset)
    _log.info(f"Loaded dataset with {len(dataset)} records")
    return dataset


def get_dataset(request: Request):
    _log.info("Returning dataset")
    return request.app.state.dataset
