def create_table(metadata, table_name, columns):
    """Создаёт таблицу в метаданных. Возвращает обновлённые метаданные."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    allowed_types = ("int", "str", "bool")
    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
        _, col_type = col.split(":", 1)
        if col_type not in allowed_types:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

    has_id = any(col.split(":", 1)[0] == "ID" for col in columns)
    if has_id:
        table_schema = []
    else:
        table_schema = [{"name": "ID", "type": "int"}]
    for col in columns:
        name, col_type = col.split(":", 1)
        table_schema.append({"name": name, "type": col_type})

    metadata[table_name] = table_schema

    cols_str = ", ".join(f'{c["name"]}:{c["type"]}' for c in table_schema)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    return metadata

def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных. Возвращает обновлённые метаданные."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

# ЭТАП 3
def _convert_value(value, col_type):
    """Преобразует строковое значение к нужному типу. Возвращает None при ошибке."""
    if col_type == "int":
        try:
            return int(value)
        except ValueError:
            return None
    if col_type == "bool":
        if value.lower() in ("true", "1"):
            return True
        if value.lower() in ("false", "0"):
            return False
        return None
    if col_type == "str":
        return str(value)
    return None


def insert(metadata, table_name, values):
    """Добавляет запись в таблицу. Возвращает обновлённые данные или None при ошибке."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    schema = metadata[table_name]
    expected = len(schema) - 1

    if len(values) != expected:
        print(f"Некорректное значение: {values}. Попробуйте снова.")
        return None

    record = {}
    for i, column in enumerate(schema[1:], start=0):
        col_name = column["name"]
        col_type = column["type"]
        converted = _convert_value(values[i], col_type)
        if converted is None:
            print(f"Некорректное значение: {values[i]}. Попробуйте снова.")
            return None
        record[col_name] = converted

    from primitive_db.utils import load_table_data

    data = load_table_data(table_name)
    new_id = max((r["ID"] for r in data), default=0) + 1
    record = {"ID": new_id, **record}
    data.append(record)

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return data


def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data
    result = []
    for record in table_data:
        if all(record.get(k) == v for k, v in where_clause.items()):
            result.append(record)
    return result


def update(table_data, set_clause, where_clause):
    updated_ids = []
    for record in table_data:
        if all(record.get(k) == v for k, v in where_clause.items()):
            for k, v in set_clause.items():
                record[k] = v
            updated_ids.append(record["ID"])
    return table_data, updated_ids


def delete(table_data, where_clause):
    deleted_ids = []
    kept = []
    for record in table_data:
        if all(record.get(k) == v for k, v in where_clause.items()):
            deleted_ids.append(record["ID"])
        else:
            kept.append(record)
    return kept, deleted_ids