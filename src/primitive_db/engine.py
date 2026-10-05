import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from primitive_db.parser import parse_set, parse_where
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

DB_FILE = "db_meta.json"

def print_start_screen():
    """Prints the start screen before the main loop."""
    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where "
        "<столбец> = <значение> - прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where "
        "<столбец> = <значение> - удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help- справочная информация\n")

def print_help():
    """Prints the help message for the current mode."""
    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where "
        "<столбец> = <значение> - прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where "
        "<столбец> = <значение> - удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help- справочная информация\n")


def print_table(table_data):
    """Выводит список записей в виде таблицы."""
    if not table_data:
        print("Нет записей.")
        return
    columns = list(table_data[0].keys())
    table = PrettyTable()
    table.field_names = columns
    for record in table_data:
        table.add_row([record.get(c) for c in columns])
    print(table)

def run():
    """Main loop of the database."""
    print_start_screen()
    while True:
        metadata = load_metadata(DB_FILE)

        user_input = prompt.string(">>>Введите команду: ")
        args = shlex.split(user_input)

        if not args:
            continue

        command = args[0]

        match command:
            case "exit":
                break
            case "help":
                print_help()
            case "list_tables":
                for table_name in metadata:
                    print(f"- {table_name}")
            case "create_table":
                table_name = args[1]
                columns = args[2:]
                metadata = create_table(metadata, table_name, columns)
                save_metadata(DB_FILE, metadata)
            case "drop_table":
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata(DB_FILE, metadata)
            case "insert":
                table_name = args[2]
                values_str = " ".join(args[4:]).strip("()")
                values = [
                    v.strip().strip('"').strip("'")
                    for v in values_str.split(",")
                ]
                data = insert(metadata, table_name, values)
                if data is not None:
                    save_table_data(table_name, data)
            case "select":
                table_name = args[2]
                data = load_table_data(table_name)
                if "where" in args:
                    where_index = args.index("where")
                    where_clause = parse_where(args[where_index + 1:])
                    data = select(data, where_clause)
                else:
                    data = select(data)
                print_table(data)
            case "update":
                table_name = args[1]
                set_index = args.index("set")
                where_index = args.index("where")
                set_clause = parse_set(args[set_index + 1:where_index])
                where_clause = parse_where(args[where_index + 1:])
                data = load_table_data(table_name)
                data, updated_ids = update(data, set_clause, where_clause)
                save_table_data(table_name, data)
                for record_id in updated_ids:
                    print(
                        f'Запись с ID={record_id} в таблице "{table_name}" '
                        "успешно обновлена."
                    )
            case "delete":
                table_name = args[2]
                where_index = args.index("where")
                where_clause = parse_where(args[where_index + 1:])
                data = load_table_data(table_name)
                data, deleted_ids = delete(data, where_clause)
                save_table_data(table_name, data)
                for record_id in deleted_ids:
                    print(
                        f'Запись с ID={record_id} успешно удалена '
                        f'из таблицы "{table_name}".'
                    )
            case "info":
                table_name = args[1]
                schema = metadata[table_name]
                columns_str = ", ".join(f'{c["name"]}:{c["type"]}' for c in schema)
                data = load_table_data(table_name)
                print(f"Таблица: {table_name}")
                print(f"Столбцы: {columns_str}")
                print(f"Количество записей: {len(data)}")
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")
