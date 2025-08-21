from typing import Dict, List, Iterator


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """Фильтрует транзакции по валюте (поддерживает оба формата)."""

    for transaction in transactions:
        # Вариант 1: Простая строка "currency": "USD"
        if transaction.get("currency") == currency:
            yield transaction

        # Вариант 2: Вложенная структура "operationAmount": {"currency": {"code": "USD"}}
        elif "operationAmount" in transaction:
            op_amount = transaction["operationAmount"]
            if isinstance(op_amount.get("currency"), dict) and op_amount["currency"].get("code") == currency:
                yield transaction


def transaction_descriptions(transactions: List[Dict[str, str]]) -> Iterator[str]:
    """Генерирует описания транзакций одну за другой."""

    for tx in transactions:
        yield tx.get("description", "No description")  # Возвращает заглушку, если ключа нет


def card_number_generator(start: int = 1, end: int = 9999999999999999) -> str:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    """

    for number in range(start, end + 1):
        # Форматируем номер с ведущими нулями до 16 цифр
        card_num = f"{number:016d}"
        # Разбиваем на группы по 4 цифры
        yield f"{card_num[:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"
