import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd

from app.config import settings

_log = logging.getLogger(__name__)


def generate_unique_id(device_id: str, timestamp: datetime) -> str:
    timestamp_str = timestamp.isoformat()
    combined = f"{device_id}_{timestamp_str}"
    hash_object = hashlib.sha256(combined.encode())
    unique_id = hash_object.hexdigest()
    return unique_id[:16]


def read_dataset(dataset_dirpath: str) -> List[pd.DataFrame]:
    dataset_dir = Path(dataset_dirpath)

    dataset: List[pd.DataFrame] = []
    for filename in dataset_dir.iterdir():
        if filename.suffix == ".csv":
            data: pd.DataFrame = pd.read_csv(filename, skiprows=1)
            data["Gerätezeitstempel"] = pd.to_datetime(
                data["Gerätezeitstempel"], format="mixed", errors="raise"
            )
            data["user_id"] = (
                filename.stem
            )  # The naming pattern for the files is: user_id.csv.
            data["id"] = data.apply(
                lambda x: generate_unique_id(x["Seriennummer"], x["Gerätezeitstempel"]),
                axis=1,
            )
            dataset.append(data)
    return dataset


def prepare_dataset(dataset: List[pd.DataFrame]) -> pd.DataFrame:
    ds = pd.concat(dataset)
    column_mapping = {
        "Seriennummer": "device_id",
        "Gerätezeitstempel": "device_timestamp",
        "Glukosewert-Verlauf mg/dL": "value",
        "user_id": "user_id",
        "id": "id",
    }
    ds = ds[list(column_mapping.keys())]
    ds = ds.rename(columns=column_mapping)
    ds = ds[ds["value"].notna()]
    return ds


def load_dataset() -> pd.DataFrame:
    _log.info("Loading dataset")
    dataset = read_dataset(settings.sample_data_dir)
    dataset = prepare_dataset(dataset)
    _log.info(f"Loaded dataset with {len(dataset)} records")
    return dataset
