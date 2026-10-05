# primitive_db

Простая консольная база данных с таблицами.

## Установка

uv tool install dist/*.whl

После установки команда database запускает базу данных.

## Управление таблицами

### Команды

- create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ... — создать таблицу
- list_tables — показать список всех таблиц
- drop_table <имя_таблицы> — удалить таблицу
- help — справочная информация
- exit — выйти из программы

### Поддерживаемые типы данных

int, str, bool

Столбец ID:int добавляется автоматически.

### Пример использования

>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>>Введите команду: list_tables
- users

>>>Введите команду: drop_table users
Таблица "users" успешно удалена.

>>>Введите команду: exit

>>>Введите команду: help
***Процесс работы с таблицей***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> exit - выход из программы
<command> help - справочная информация 


## Демо этап 2

https://asciinema.org/a/KmFAXYk6z8vlczSS


## CRUD-операции

### Команды

- insert into <имя_таблицы> values (<значение1>, <значение2>, ...) — создать запись
- select from <имя_таблицы> — прочитать все записи
- select from <имя_таблицы> where <столбец> = <значение> — прочитать записи по условию
- update <имя_таблицы> set <столбец> = <новое_значение> where <столбец> = <значение> — обновить запись
- delete from <имя_таблицы> where <столбец> = <значение> — удалить запись
- info <имя_таблицы> — информация о таблице

### Пример использования

>>> Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>> Введите команду: insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".

>>> Введите команду: select from users where age = 28
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei | 28  |    True   |
+----+--------+-----+-----------+

>>> Введите команду: update users set age = 29 where name = "Sergei"
Запись с ID=1 в таблице "users" успешно обновлена.

>>> Введите команду: delete from users where ID = 1
Запись с ID=1 успешно удалена из таблицы "users".

>>> Введите команду: info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0

## Демо этап 3

https://asciinema.org/a/cOBDFU1MIWzgGmj0
