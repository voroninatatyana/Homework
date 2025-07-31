import pytest

from src.masks import get_mask_account, get_mask_card_number


# Фикстуры для тестовых данных карт
@pytest.fixture
def valid_card_numbers() -> list[tuple[str, str]]:
    return [
        ("1234567890123456", "1234 56** **** 3456"),
        ("5105105105105100", "5105 10** **** 5100"),
        ("4111111111111111", "4111 11** **** 1111"),
        ("378282246310005", "3782 82** **** 0005")  # American Express
    ]


@pytest.fixture
def invalid_card_numbers() -> list[str]:
    return [
        ("1234"),  # Слишком короткий
        ("12345678901234567890"),  # Слишком длинный
        ("abcdefghijklmnop"),  # Не цифры
        (None),  # None
        ("")  # Пустая строка
    ]


# Фикстуры для тестовых данных счетов
@pytest.fixture
def valid_account_numbers() -> list[tuple[str, str]]:
    return [
        ("12345678901234567890", "**7890"),
        ("73654108430135874305", "**4305"),
        ("00000000000000000001", "**0001")
    ]


@pytest.fixture
def invalid_account_numbers() -> list[str]:
    return [
        ("1234"),  # Слишком короткий
        ("abcdefghijklmnop"),  # Не цифры
        (None),  # None
        ("")  # Пустая строка
    ]


# Тесты для get_mask_card_number
@pytest.mark.parametrize("card_number, expected", [
    ("1234567890123456", "1234 56** **** 3456"),
    ("4111111111111111", "4111 11** **** 1111"),
    ("5555555555554444", "5555 55** **** 4444"),
    ("371449635398431", "3714 49** **** 8431")  # American Express 15 цифр
])
def test_get_mask_card_number_valid(card_number: str, expected: str) -> None:
    """Тестирование корректных номеров карт"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("card_number", [
    "1234",  # 4 цифры
    "1234567890",  # 10 цифр
    "abcdefghijklmnop",  # буквы
    "",  # пустая строка
    None  # None
])
def test_get_mask_card_number_invalid(card_number: str | None) -> None:
    """Тестирование обработки невалидных номеров карт"""
    result = get_mask_card_number(card_number)
    assert result == card_number  # Или ожидайте другое поведение


def test_get_mask_card_number_edge_cases() -> None:
    """Тестирование граничных случаев"""
    assert get_mask_card_number("123456789012345") == "1234 56** **** 2345"  # 15 цифр
    assert get_mask_card_number("12345678901234567") == "1234 56** **** 4567"  # 17 цифр


# Тесты для get_mask_account
@pytest.mark.parametrize("account_number, expected", [
    ("12345678901234567890", "**7890"),
    ("73654108430135874305", "**4305"),
    ("00000000000000000001", "**0001")
])
def test_get_mask_account_valid(account_number: str, expected: str):
    """Тестирование корректных номеров счетов"""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize("account_number", [
    "1234",  # 4 цифры (меньше минимальной длины)
    "abcdefghijklmnop",  # буквы
    "",  # пустая строка
    None  # None
])
def test_get_mask_account_invalid(account_number: str):
    """Тестирование обработки невалидных номеров счетов"""
    result = get_mask_account(account_number)
    assert result == account_number  # Или ожидайте другое поведение


def test_get_mask_account_edge_cases() -> None:
    """Тестирование граничных случаев для счетов"""
    assert get_mask_account("123456") == "**3456"  # Минимальная длина
    assert get_mask_account("1") == "**1"  # Очень короткий
