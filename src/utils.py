import json
import os
from typing import List, Dict, Any

# Узнаем текущую рабочую директорию
print(f"Текущая рабочая директория: {os.getcwd()}")

# Узнаем путь к директории скрипта
print(f"Директория скрипта: {os.path.dirname(os.path.abspath(__file__))}")

# Посмотрим что есть в текущей директории
print("Содержимое текущей директории:")
for item in os.listdir():
    print(f"  {item}")
file_path = os.path.join(os.path.dirname(__file__), "data", "operations.json")
print(f"Путь существует: {os.path.exists(file_path)}")
print(f"Это файл: {os.path.isfile(file_path)}")


def find_json_file():
    """Ищет файл operations.json в различных местах"""
    possible_paths = [
        "data/operations.json",
        "operations.json",
        "../data/operations.json",
        "../../data/operations.json"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"Файл найден: {os.path.abspath(path)}")
            return path
    return None


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден!")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            else:
                print("Файл не содержит список!")
                return []

    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле {file_path}.")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return []


# Пример использования

if __name__ == "__main__":
    # Создаем правильный путь
    file_path = os.path.join("data", "operations.json")
    file_path = find_json_file()

    if file_path:
        transactions = read_json_file(file_path)
        print(f"Загружено {len(transactions)} транзакций")
    else:
        print("Файл operations.json не найден ни в одном из возможных мест!")
        print("Пожалуйста, поместите файл в одну из следующих папок:")
        print("- data/operations.json")
        print("- operations.json (в корне проекта)")
    # Читаем файл
    transactions = read_json_file(file_path)
    print(f"Загружено {len(transactions)} транзакций")