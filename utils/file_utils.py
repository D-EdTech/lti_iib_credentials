# utils/file_utils.py
import json
import csv
from pathlib import Path
from typing import Any, List, Dict, Union
import os

# Set the base directory for data files (e.g., a folder named "data" at the project root).
# __file__ is the path to the current file (config.py), so we move one level up and then into "data".
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Ensure the data directory exists.
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Default filenames for the core data store and CSV export (placed in the data directory).
JSON_FILENAME = os.path.join(DATA_DIR, "blackboard_users.json")
CSV_FILENAME = os.path.join(DATA_DIR, "blackboard_users.csv")

# Sleep time between API calls (in seconds)
API_SLEEP_TIME = 0.5





# A static list of CSV column names in the desired order.
CSV_FIELDNAMES = [
    "uuid",
    "inspera_username",
    "blackboard_sync_timestamp",
    "name_given",
    "name_family",
    "contact_email",
    "inspera_sync_timestamp",
    "sync_to_inspera",
    "inspera_password",
]


def read_json(filepath: Union[str, Path]) -> Any:
    """
    Read and return JSON data from the given file.

    Args:
        filepath: The path to the JSON file.

    Returns:
        The data parsed from JSON.
    """
    path = Path(filepath)
    return json.loads(path.read_text())

def write_json(data: Any, filepath: Union[str, Path]) -> None:
    """
    Write the provided data as JSON to the specified file.

    Args:
        data: The data to serialize.
        filepath: The path to the output JSON file.
    """
    path = Path(filepath)
    # Using json.dumps to serialize with indentation and then writing text.
    path.write_text(json.dumps(data, indent=2))

def regenerate_csv(
    data_records: List[Dict[str, Any]],
    csv_path: Union[str, Path],
    fieldnames: List[str]
) -> None:
    """
    Write a list of record dictionaries to a CSV file using the specified columns.

    Args:
        data_records: A list of dictionaries containing the data.
        csv_path: The path to the output CSV file.
        fieldnames: The list of field names (columns) for the CSV.

    Each record is filtered so that only keys present in 'fieldnames' are written.
    If a key is missing in a record, an empty string is used as its value.
    """
    csv_path = Path(csv_path)
    with csv_path.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in data_records:
            row = {}
            for field in fieldnames:
                if field == "sync_to_inspera":
                    row[field] = record.get(field, "False")
                else:
                    row[field] = record.get(field, "")
            writer.writerow(row)
