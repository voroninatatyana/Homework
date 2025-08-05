import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number, expected",
    [("1234567890123456", "1234 56** **** 3456"), ("7000792289606361", "7000 79** **** 6361")],
)
def test_valid_masking(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("invalid_input, expected_error", [
    (None, TypeError),
    (123, TypeError),
    ("Short", ValueError)
])
def test_invalid_input_returns(invalid_input, expected_error):
    with pytest.raises(expected_error):
        get_mask_card_number(invalid_input)


@pytest.mark.parametrize("account_number, expected", [
    ("Счет 73654108430135874305", "**4305"),
    ("73654108430135874305", "**4305"),
    (73654108430135874305, "**4305"),  # Число
    ("  Счет 1234567890  ", "**7890"),  # Пробелы
    ("ACC1234567890", "**7890")         # Без "Счет"
])
def test_valid_account_masking(account_number, expected):
    assert get_mask_account(account_number) == expected

@pytest.mark.parametrize("invalid_input, expected_error", [
    ("Счет 123", ValueError),  # Слишком короткий
    (123, ValueError),         # Слишком короткое число
    (None, TypeError)         # None
   ])
def test_invalid_account_input(invalid_input, expected_error):
    with pytest.raises(expected_error):
        get_mask_account(invalid_input)
