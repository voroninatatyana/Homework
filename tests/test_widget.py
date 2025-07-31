from typing import Any

import pytest

from src.widget import get_date_safe, mask_account_card


# Фикстуры для тестовых данных
@pytest.fixture
def valid_cards_and_accounts() -> list[tuple[str, str]]:
    """Фикстура возвращает список кортежей: (входные данные, ожидаемый результат)"""
    return [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ]


@pytest.fixture
def invalid_inputs() -> list[Any]:
    return [
        None,
        "",
        "InvalidString",
        "Card 1234",  # Слишком короткий номер
        "Счет 123",  # Слишком короткий номер счета
        1234567890,  # Число вместо строки
    ]


@pytest.fixture
def date_samples() -> list[tuple[str, str]]:
    return [
        ("2023-01-15T12:00:00.000000", "15.01.2023"),
        ("2022-12-31T23:59:59.999999", "31.12.2022"),
        ("2020-02-29T00:00:00.000000", "29.02.2020"),  # Високосный год
    ]


@pytest.fixture
def invalid_dates() -> list[Any]:
    return [
        None,
        "",
        "2023-13-01T00:00:00",  # Несуществующий месяц
        "2023-01-32T00:00:00",  # Несуществующий день
        "InvalidDateString",
        20230115,  # Число вместо строки
    ]


# Тесты для mask_account_card
@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ],
)
def test_mask_account_card_valid(input_data: str, expected: str) -> None:
    """Тестирование корректной маскировки карт и счетов"""
    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize("input_data", [None, "", "InvalidString", "Card 1234", "Счет 123", 1234567890])
def test_mask_account_card_invalid(input_data: str | None) -> None:
    """Тестирование обработки некорректных входных данных"""
    result = mask_account_card(input_data)
    assert result == input_data  # Или ожидаемое поведение для ошибок


# Тесты для get_date
@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2023-01-15T12:00:00.000000", "15.01.2023"),
        ("2022-12-31T23:59:59.999999", "31.12.2022"),
        ("2020-02-29T00:00:00.000000", "29.02.2020"),
        ("1999-12-31T00:00:00", "31.12.1999"),  # Разные форматы времени
    ],
)
def test_get_date_valid(input_date: str, expected: str) -> None:
    """Тестирование корректного преобразования даты"""
    assert get_date_safe(input_date) == expected


@pytest.mark.parametrize(
    "input_date", [None, "", "2023-13-01T00:00:00", "2023-01-32T00:00:00", "InvalidDateString", 20230115]
)
def test_get_date_invalid(input_date: str | None) -> None:
    """Тестирование обработки некорректных дат"""
    result = get_date_safe(input_date)
    assert result == input_date  # Или ожидаемое поведение для ошибок


def test_get_date_edge_cases() -> None:
    """Тестирование граничных случаев для дат"""
    assert get_date_safe("2023-01-01T00:00:00.000000") == "01.01.2023"
    assert get_date_safe("9999-12-31T23:59:59.999999") == "31.12.9999"
    assert get_date_safe("0001-01-01T00:00:00") == "01.01.0001"  # Минимальная дата
