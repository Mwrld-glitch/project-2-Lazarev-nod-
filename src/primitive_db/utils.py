import json
import os

from primitive_db.constants import DATA_DIR
from primitive_db.decorators import handle_db_errors


@handle_db_errors
def load_metadata(filepath):
    """Загружает метаданные из JSON-файла."""
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@handle_db_errors
def load_table_data(table_name):
    """Загружает данные таблицы из файла data/<имя>.json."""
    filepath = f"{DATA_DIR}/{table_name}.json"
    if not os.path.exists(filepath):
        return []
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def save_table_data(table_name, data):
    """Сохраняет данные таблицы в файл data/<имя>.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)