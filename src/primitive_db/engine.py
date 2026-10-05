import prompt


def welcome():
    print("Первая попытка запустить проект!")
    while True:
        print("***")
        print("<command> exit - выйти из программы")
        print("<command> help - справочная информация")
        prompt.string("Введите команду: ")