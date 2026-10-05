import json
import os


def load_metadata(filepath):
    """
    Загружает метаданные из JSON-файла.
    Если файла нет — возвращает пустой словарь.
    Этап 2. Задача 6
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл.
     Этап 2. Задача 6
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

DATA_DIR = "data"

# ЭТАП 3
def load_table_data(table_name):
    """Загружает данные таблицы из файла data/<table_name>.json."""
    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет данные таблицы в файл data/<table_name>.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)