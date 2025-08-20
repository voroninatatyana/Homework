import pytest
from typing import Dict, List, Iterator
from collections.abc import Iterator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions
from src.generators import card_number_generator

# Исходные данные
TRANSACTIONS = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"code": "USD"}
        },
        "description": "Перевод организации"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"code": "USD"}
        },
        "description": "Перевод со счета на счет"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"code": "RUB"}
        },
        "description": "Перевод со счета на счет"
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {"code": "USD"}
        },
        "description": "Перевод с карты на карту"
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {"code": "RUB"}
        },
        "description": "Перевод организации"
    }
]


def test_format_correctness():
    """Проверка корректности форматирования"""
    gen = card_number_generator(1, 3)
    numbers = list(gen)

    assert numbers == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]


def test_range_limits():
    """Проверка обработки крайних значений диапазона"""
    # Минимальное значение
    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001"

    # Максимальное значение
    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999"

    # Диапазон из одного элемента
    gen = card_number_generator(1234567890123456, 1234567890123456)
    assert next(gen) == "1234 5678 9012 3456"


def test_generator_behavior():
    """Проверка поведения генератора"""
    gen = card_number_generator(42, 44)

    # Поэлементное получение значений
    assert next(gen) == "0000 0000 0000 0042"
    assert next(gen) == "0000 0000 0000 0043"
    assert next(gen) == "0000 0000 0000 0044"

    # Проверка завершения генератора
    with pytest.raises(StopIteration):
        next(gen)


def test_empty_range():
    """Проверка пустого диапазона (start > end)"""
    gen = card_number_generator(10, 5)
    assert list(gen) == []


def test_large_range():
    """Проверка работы с большим диапазоном"""
    gen = card_number_generator(9999999999999990, 9999999999999999)
    numbers = list(gen)

    assert len(numbers) == 10
    assert numbers[0] == "9999 9999 9999 9990"
    assert numbers[-1] == "9999 9999 9999 9999"
    assert all(len(num) == 19 for num in numbers)  # 16 цифр + 3 пробела


# Дополнительные параметризованные тесты
@pytest.mark.parametrize("start,end,expected_first,expected_last,expected_count", [
    (1, 5, "0000 0000 0000 0001", "0000 0000 0000 0005", 5),
    (9999, 10001, "0000 0000 0000 9999", "0000 0000 0001 0001", 3),
    (42, 42, "0000 0000 0000 0042", "0000 0000 0000 0042", 1),
])
def test_parametrized_ranges(start, end, expected_first, expected_last, expected_count):
    """Параметризованные тесты для разных диапазонов"""
    gen = card_number_generator(start, end)
    numbers = list(gen)

    assert numbers[0] == expected_first
    assert numbers[-1] == expected_last
    assert len(numbers) == expected_count
    assert all(len(num) == 19 for num in numbers)


