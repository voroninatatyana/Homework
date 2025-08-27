import os
import json
from typing import List, Dict, Any


def load_transactions(data/operations.json: str) -> List[Dict[str, Any]]:
    """
    Загружает список финансовых транзакций из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Возвращает пустой список если:
                              - файл не найден
                              - файл пустой
                              - файл не содержит список
    """
    try:
        with open(data/operations.json, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []

    except FileNotFoundError:
        # Файл не найден
        return []
    except json.JSONDecodeError:
        # Файл пустой или содержит некорректный JSON
        return []
    except Exception:
        # Любые другие ошибки (например, проблемы с доступом)
        return []