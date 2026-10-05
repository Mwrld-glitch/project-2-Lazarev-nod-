from primitive_db.constants import VALID_TYPES
from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import load_table_data


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создаёт новую таблицу с указанными столбцами."""
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    for col in columns:
        name, col_type = col.split(":", 1)
        if col_type not in VALID_TYPES:
            raise ValueError(col)

    table_schema = [{"name": "ID", "type": "int"}]
    for col in columns:
        name, col_type = col.split(":", 1)
        table_schema.append({"name": name, "type": col_type})

    metadata[table_name] = table_schema

    cols_str = ", ".join(f'{c["name"]}:{c["type"]}' for c in table_schema)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу."""
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def _convert_value(value, col_type):
    """Преобразует строку в значение нужного типа."""
    if col_type == "int":
        return int(value)
    if col_type == "bool":
        if value.lower() in ("true", "1"):
            return True
        if value.lower() in ("false", "0"):
            return False
        raise ValueError(value)
    if col_type == "str":
        return str(value)
    raise ValueError(col_type)


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет новую запись в таблицу."""
    schema = metadata[table_name]
    expected = len(schema) - 1

    if len(values) != expected:
        raise ValueError(values)

    record = {}
    for i, column in enumerate(schema[1:], start=0):
        col_name = column["name"]
        col_type = column["type"]
        converted = _convert_value(values[i], col_type)
        if converted is None:
            raise ValueError(values[i])
        record[col_name] = converted

    data = load_table_data(table_name)
    if data is None:
        data = []
    new_id = max((r["ID"] for r in data), default=0) + 1
    record = {"ID": new_id, **record}
    data.append(record)

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return data

@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает записи таблицы — все или по условию."""
    if where_clause is None:
        return table_data
    result = []
    for record in table_data:
        if all(record.get(k) == v for k, v in where_clause.items()):
            result.append(record)
    return result


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет записи таблицы по условию."""
    updated_ids = []
    for record in table_data:
        if all(record.get(k) == v for k, v in where_clause.items()):
            for k, v in set_clause.items():
                record[k] = v
            updated_ids.append(record["ID"])
    if not updated_ids:
        raise ValueError("нет записей для обновления")
    return table_data, updated_ids


@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause):
    """Удаляет записи таблицы по условию."""
    deleted_ids = []
    kept = []
    for record in table_data:
        if all(record.get(k) == v for k, v in where_clause.items()):
            deleted_ids.append(record["ID"])
        else:
            kept.append(record)
    if not deleted_ids:
        raise ValueError("нет записей для удаления")
    return kept, deleted_ids


@handle_db_errors
def list_tables(metadata):
    """Возвращает список всех таблиц."""
    return list(metadata.keys())


@handle_db_errors
def info(metadata, table_name):
    """Возвращает информацию о таблице."""
    return metadata[table_name]