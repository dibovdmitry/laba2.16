#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import jsonschema


def get_airplane():
    path = input("Пункт назначения ")
    number = input("Номер рейса ")
    model = input("Тип самолёта ")

    return {
        'path': path,
        'number': number,
        'model': model
    }


def display_airplanes(race):
    if race:
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
        print("Таких рейсов нет")


def select_airplanes(race, sel):
    result = []
    for airplane in race:
        if airplane.get('path') <= sel:
            result.append(airplane)

    return result


def save_airplanes(file_name, race):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(race, f, ensure_ascii=False, indent=4)


def load_airplanes(file_name):

    with open("schema.json", 'r', encoding="utf-8") as schem:
        schema = json.load(schem)

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

        elif command == 'select':
            parts = command.split(' ', maxsplit=2)
            sel = int(parts[1])

        elif command.startswith("save "):
            parts = command.split(' ', maxsplit=2)
            file_name = parts[1]

            save_airplanes(file_name, airplanes)

        elif command.startswith("load "):
            parts = command.split(' ', maxsplit=2)
            file_name = parts[1]

            airplanes = load_airplanes(file_name)

        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить маршрут;")
            print("list - вывести список маршрутов;")
            print("select - нати маршруты по времени")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
