import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata

DB_FILE = "db_meta.json"

def print_start_screen():
    """Prints the start screen before the main loop."""
    print("\n***База данных***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def print_help():
    """Prints the help message for the current mode."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


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
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")