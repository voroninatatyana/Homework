import pytest
from typing import Dict, List, Iterator
from collections.abc import Iterator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions
from src.generators import card_number_generator

@pytest.fixture
def sample_transactions() -> List[Dict[str, str]]:
    return [
        {"amount": "100", "currency": "USD"},
        {"amount": "200", "currency": "EUR"},
        {"amount": "300", "currency": "USD"},
        {"amount": "400", "currency": "GBP"},
        {"amount": "500"},  # Транзакция без валюты
        {"amount": "600", "currency": "RUB"}
    ]

# Основные тесты
def test_filter_usd_transactions(sample_transactions):
    """Тест фильтрации USD транзакций."""
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert result == [
        {"amount": "100", "currency": "USD"},
        {"amount": "300", "currency": "USD"}
    ]

def test_empty_result_for_absent_currency(sample_transactions):
    """Тест для валюты, которой нет в транзакциях."""
    result = list(filter_by_currency(sample_transactions, "JPY"))
    assert result == []

# Параметризованный тест
@pytest.mark.parametrize("currency, expected_count, expected_amounts", [
    ("USD", 2, ["100", "300"]),
    ("EUR", 1, ["200"]),
    ("GBP", 1, ["400"]),
    ("RUB", 1, ["600"]),
    ("JPY", 0, []),
])
def test_with_parameters(sample_transactions, currency, expected_count, expected_amounts):
    """Тест с параметрами для разных валют."""
    result = list(filter_by_currency(sample_transactions, currency))
    assert len(result) == expected_count
    assert [tx["amount"] for tx in result] == expected_amounts

# Тест для особых случаев
def test_empty_input():
    """Тест с пустым списком транзакций."""
    assert list(filter_by_currency([], "USD")) == []

def test_transactions_without_currency_field(sample_transactions):
    """Тест обработки транзакций без поля currency."""
    result = list(filter_by_currency(sample_transactions, "RUB"))
    assert result == [{"amount": "600", "currency": "RUB"}]

# Тест типа возвращаемого значения
def test_return_type(sample_transactions):
    """Проверка, что возвращается итератор."""
    result = filter_by_currency(sample_transactions, "USD")
    assert isinstance(result, Iterator)


@pytest.fixture
def sample_transactions(self) -> List[Dict[str, str]]:
    """Фикстура с тестовыми данными транзакций"""
    return [
        {"description": "Payment for coffee", "amount": "100"},
        {"description": "Grocery shopping", "amount": "200"},
        {"description": "Taxi ride", "amount": "50"},
        {"description": "Restaurant bill", "amount": "75"}
    ]


def test_returns_correct_descriptions(self, sample_transactions):
    """Проверка корректности возвращаемых описаний"""
    gen = transaction_descriptions(sample_transactions)

    # Проверяем тип возвращаемого значения
    assert isinstance(gen, Iterator)

    # Получаем все описания
    descriptions = list(gen)

    # Проверяем корректность данных
    assert descriptions == [
        "Payment for coffee",
        "Grocery shopping",
        "Taxi ride",
        "Restaurant bill"
    ]


def test_empty_list(self):
    """Тестирование с пустым списком транзакций"""
    gen = transaction_descriptions([])
    assert list(gen) == []


def test_single_transaction(self):
    """Тестирование с одной транзакцией"""
    single_transaction = [{"description": "Single payment", "amount": "10"}]
    gen = transaction_descriptions(single_transaction)
    assert list(gen) == ["Single payment"]


def test_large_number_of_transactions(self):
    """Тестирование с большим количеством транзакций"""
    large_transactions = [
        {"description": f"Transaction {i}", "amount": str(i)}
        for i in range(1000)
    ]
    gen = transaction_descriptions(large_transactions)

    # Проверяем первое и последнее описание
    first = next(gen)
    assert first == "Transaction 0"

    # Пропускаем остальные
    remaining = list(gen)
    assert remaining[-1] == "Transaction 999"
    assert len(remaining) == 999


def test_transaction_without_description(self):
    """Тестирование обработки транзакции без описания"""
    transactions = [
        {"description": "Valid transaction", "amount": "100"},
        {"amount": "200"},  # Транзакция без описания
        {"description": "Another valid", "amount": "300"}
    ]

    gen = transaction_descriptions(transactions)

    # Проверяем, что функция вызовет KeyError
    with pytest.raises(KeyError):
        list(gen)  # Попытка получить все описания вызовет ошибку


# Дополнительные тесты для проверки работы с next()
def test_generator_behavior():
    """Тестирование поэлементной работы генератора"""
    transactions = [
        {"description": "First", "amount": "1"},
        {"description": "Second", "amount": "2"}
    ]

    gen = transaction_descriptions(transactions)

    # Получаем описания по одному
    assert next(gen) == "First"
    assert next(gen) == "Second"

    # Проверяем завершение генератора
    with pytest.raises(StopIteration):
        next(gen)

    def test_format_correctness(self):
        """Проверка корректности форматирования"""
        gen = card_number_generator(1, 3)
        numbers = list(gen)

        assert numbers == [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]

    def test_range_limits(self):
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

    def test_generator_behavior(self):
        """Проверка поведения генератора"""
        gen = card_number_generator(42, 44)

        # Поэлементное получение значений
        assert next(gen) == "0000 0000 0000 0042"
        assert next(gen) == "0000 0000 0000 0043"
        assert next(gen) == "0000 0000 0000 0044"

        # Проверка завершения генератора
        with pytest.raises(StopIteration):
            next(gen)

    def test_empty_range(self):
        """Проверка пустого диапазона (start > end)"""
        gen = card_number_generator(10, 5)
        assert list(gen) == []

    def test_large_range(self):
        """Проверка работы с большим диапазоном"""
        gen = card_number_generator(9999999999999990, 9999999999999999)
        numbers = list(gen)

        assert len(numbers) == 10
        assert numbers[0] == "9999 9999 9999 9990"
        assert numbers[-1] == "9999 9999 9999 9999"
        assert all(len(num) == 19 for num in numbers)  # 16 цифр + 3 пробела

    def test_default_parameters(self):
        """Проверка работы с параметрами по умолчанию"""
        gen = card_number_generator()
        first = next(gen)
        assert first == "0000 0000 0000 0001"

        # Проверяем, что генератор бесконечный (не бросает StopIteration)
        for _ in range(100):
            next(gen)


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
    assert all(len(num) == 19 for num in numbers)  # Проверка формата
