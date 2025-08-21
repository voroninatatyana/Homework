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


@pytest.fixture
def mixed_transactions():
    return [
        # Простой формат
        {"id": 1, "currency": "USD", "amount": "100"},
        {"id": 2, "currency": "EUR", "amount": "200"},

        # Вложенный формат
        {
            "id": 3,
            "operationAmount": {
                "amount": "300",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 4,
            "operationAmount": {
                "amount": "400",
                "currency": {"code": "RUB"}
            }
        }
    ]


@pytest.mark.parametrize("currency, expected_ids", [
    ("USD", [1, 3]),  # Оба формата USD
    ("EUR", [2]),  # Простой формат
    ("RUB", [4]),  # Вложенный формат
    ("JPY", [])  # Отсутствующая валюта
])
def test_filter_mixed_formats(mixed_transactions, currency, expected_ids):
    result = list(filter_by_currency(mixed_transactions, currency))
    assert [tx["id"] for tx in result] == expected_ids


def test_empty_list():
    result = list(filter_by_currency([], "USD"))
    assert result == []


# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions():
    return [
        {"description": "Перевод организации", "amount": "100", "currency": "USD"},
        {"description": "Перевод со счета на счет", "amount": "200", "currency": "EUR"},
        {"description": "Оплата услуг", "amount": "50", "currency": "RUB"},
        {"description": "Пополнение счета", "amount": "75", "currency": "USD"}
    ]


# Тест 1: Корректность возвращаемых описаний
def test_returns_correct_descriptions(sample_transactions):
    """Проверяет, что функция возвращает корректные описания"""
    # Act
    result = list(transaction_descriptions(sample_transactions))

    # Assert
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Оплата услуг",
        "Пополнение счета"
    ]
    assert result == expected


# Тест 2: Работа с разным количеством данных
@pytest.mark.parametrize("transactions_data, expected_descriptions", [
    # Множество транзакций
    ([
         {"description": "Транзакция 1"},
         {"description": "Транзакция 2"},
         {"description": "Транзакция 3"},
         {"description": "Транзакция 4"},
         {"description": "Транзакция 5"}
     ], ["Транзакция 1", "Транзакция 2", "Транзакция 3", "Транзакция 4", "Транзакция 5"]),

    # Одна транзакция
    ([{"description": "Единственная транзакция"}], ["Единственная транзакция"]),

    # Пустой список
    ([], []),

    # Транзакции с одинаковыми описаниями
    ([
         {"description": "Повтор"},
         {"description": "Повтор"},
         {"description": "Повтор"}
     ], ["Повтор", "Повтор", "Повтор"])
])
def test_different_data_volumes(transactions_data, expected_descriptions):
    """Проверяет работу функции с разным количеством данных"""
    # Act
    result = list(transaction_descriptions(transactions_data))

    # Assert
    assert result == expected_descriptions


# Тест 3: Поведение генератора
def test_generator_behavior(sample_transactions):
    """Проверяет, что функция возвращает итератор и работает поэлементно"""
    # Arrange
    gen = transaction_descriptions(sample_transactions)

    # Assert - проверяем тип
    assert hasattr(gen, '__iter__')
    assert hasattr(gen, '__next__')

    # Act & Assert - проверяем поэлементную работу
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Оплата услуг"
    assert next(gen) == "Пополнение счета"

    # Проверяем завершение генератора
    with pytest.raises(StopIteration):
        next(gen)


# Тест 4: Пустой список (отдельный тест для ясности)
def test_empty_list():
    """Проверяет работу с пустым списком транзакций"""
    result = list(transaction_descriptions([]))
    assert result == []


# Тест 5: Проверка на отсутствие ошибок с минимальными данными
def test_minimal_transaction():
    """Проверяет работу с транзакцией, содержащей только описание"""
    transactions = [{"description": "Минимальная транзакция"}]
    result = list(transaction_descriptions(transactions))
    assert result == ["Минимальная транзакция"]


# Тест 6: Проверка порядка возвращаемых описаний
def test_order_preservation(sample_transactions):
    """Проверяет, что порядок описаний соответствует порядку транзакций"""
    result = list(transaction_descriptions(sample_transactions))

    # Порядок должен сохраняться
    assert result[0] == "Перевод организации"
    assert result[1] == "Перевод со счета на счет"
    assert result[2] == "Оплата услуг"
    assert result[3] == "Пополнение счета"