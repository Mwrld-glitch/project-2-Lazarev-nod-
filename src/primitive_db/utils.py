import json
import os

from primitive_db.decorators import handle_db_errors

DATA_DIR = "data"


@handle_db_errors
def load_metadata(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@handle_db_errors
@handle_db_errors
def load_table_data(table_name):
    filepath = f"{DATA_DIR}/{table_name}.json"
    if not os.path.exists(filepath):
        return []
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def save_table_data(table_name, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)