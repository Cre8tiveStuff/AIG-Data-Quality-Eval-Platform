import csv
import json
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd


def load_dataset(file_path: str) -> List[Dict[str, Any]]:
    """
    Loads dataset from JSON, JSONL, CSV, or Parquet formats into a standard list of dictionaries.
    """
    path = Path(file_path)

    # 1. Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")

    # 2. Parse based on file extension
    ext = path.suffix.lower()

    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            raise ValueError("JSON file must contain a top-level array of objects.")

    elif ext == ".jsonl":
        dataset = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    dataset.append(json.loads(line))
        return dataset

    elif ext == ".csv":
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    elif ext == ".parquet":
        df = pd.read_parquet(path)
        return df.to_dict(orient="records")

    else:
        raise ValueError(f"Unsupported file extension '{ext}'. Supported formats: .json, .jsonl, .csv, .parquet")