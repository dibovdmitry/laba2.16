#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import jsonschema


def get_airplane():
    """
    Запросить данные о работнике.
    """
    path = input("Название пункта назначения рейса ")
    number = input("Номер рейса ")
    model = float(input("Тип самолёта "))

    # Создать словарь.
    return {
        'path': path,
        'number': number,
        'model': model,
    }


def display_airplanes(race):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if race:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолёта"
            )
        )
        print(line)

        for idx, airplane in enumerate(race, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    airplane.get('path', ''),
                    airplane.get('number', ''),
                    airplane.get('model', 0)
                )
            )
        print(line)

    else:
        print("Таких рейсов нет.")


def select_airplanes(race, sel):
    """
    Выбрать работников с заданным стажем.
    """
    result = []
    for airplane in race:
        if airplane.get('path') <= sel:
            result.append(airplane)

    return result


def save_races(file_name, race):
    """
    Сохранить всех работников в файл JSON.
    """

    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(race, fout, ensure_ascii=False, indent=4)


def load_races(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    # Открыть файл с JSON schema.
    with open("schema.json", 'r', encoding="utf-8") as schem:
        schema = json.load(schem)

    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fl:
        data = json.load(fl)

        validator = jsonschema.Draft7Validator(schema)

        try:
            if not validator.validate(data):
                print("Данные успешно загружены")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка загрузки данных", file=sys.stderr)
            exit(1)

        return data


def main():
    """
    Главная функция программы.
    """

    airplanes = []

    while True:
        command = input(">>> ").lower()

        if command == 'exit':
            break

        elif command == 'add':
            airplane = get_airplane()

            airplanes.append(airplane)
            if len(airplanes) > 1:
                airplanes.sort(key=lambda item: item.get('number', ''))

        elif command == 'list':
            display_airplanes(airplanes)

        elif command.startswith('select '):
            parts = command.split(' ', maxsplit=2)
            sel = str(parts[1])

            selected = select_airplanes(airplanes, sel)
            display_airplanes(selected)

        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить работника;")
            print("list - вывести список работников;")
            print("select <стаж> - запросить работников со стажем;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
