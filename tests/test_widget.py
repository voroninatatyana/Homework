import pytest
from src.widget import get_date_safe, mask_account_card

# Общие фикстуры
@pytest.fixture
def valid_data_samples() -> list[tuple[str, str]]:
    return [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("2023-01-15T12:00:00.000000", "15.01.2023")
    ]

# Параметризованные тесты для mask_account_card
@pytest.mark.parametrize("input_data, expected", [
    ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
    ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("1234567890123456", "1234 56** **** 3456")  # Без названия
])
def test_valid_masking(input_data, expected):
    assert mask_account_card(input_data) == expected

@pytest.mark.parametrize("invalid_input, expected_error", [
    (None, TypeError),
    (1234567890, TypeError),
    ("Short", ValueError),
    ("Card 1234", ValueError),
    ("Счет 123", ValueError)
])
def test_invalid_masking(invalid_input, expected_error):
    with pytest.raises(expected_error):
        mask_account_card(invalid_input)

# Параметризованные тесты для get_date_safe
@pytest.mark.parametrize("date_str, expected", [
    ("2023-01-15T12:00:00", "15.01.2023"),
    ("2020-02-29T00:00:00", "29.02.2020"),
    ("1999-12-31T00:00:00", "31.12.1999")
])
def test_valid_dates(date_str: str, expected: str) -> None:
    assert get_date_safe(date_str) == expected

@pytest.mark.parametrize("invalid_date, expected_result", [
    (None, None),
    ("2023-13-01", "2023-13-01"),
    (20230115, 20230115)
])
def test_invalid_dates(invalid_date, expected_result):
    assert get_date_safe(invalid_date) == expected_result