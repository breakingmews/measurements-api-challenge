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
            data: pd.DataFrame = pd.read_csv(filename, dtype={"user_id": str})
            data["device_timestamp"] = pd.to_datetime(
                data["device_timestamp"], format="mixed", errors="raise"
            )
            data["id"] = data.apply(
                lambda x: generate_unique_id(x["device_id"], x["device_timestamp"]),
                axis=1,
            )
            dataset.append(data)
    return dataset


def load_dataset() -> pd.DataFrame:
    _log.info("Loading dataset")
    dataset = read_dataset(settings.sample_data_dir)
    df = pd.concat(dataset)
    _log.info(f"Loaded dataset with {len(dataset)} records")
    return df
