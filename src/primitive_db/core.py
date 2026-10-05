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

