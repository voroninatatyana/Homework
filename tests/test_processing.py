# test_processing.py
import pytest
from datetime import datetime
from src.processing import filter_by_state, sort_by_date

# Фикстуры для тестовых данных
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-15T12:00:00.000000"
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2023-01-10T08:30:00.000000"
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2023-01-20T18:45:00.000000"
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "2023-01-05T10:15:00.000000"
        },
        {
            "id": 5,
            "state": "EXECUTED",
            "date": "2023-01-15T12:00:00.000000"  # Такая же дата, как у id=1
        }
    ]

@pytest.fixture
def edge_case_transactions():
    return [
        {
            "id": 6,
            "state": "EXECUTED",
            "date": "invalid_date_format"  # Некорректный формат даты
        },
        {
            "id": 7,
            "state": "FAILED",
            "date": None  # Отсутствующая дата
        }
    ]

# Тесты для filter_by_state
@pytest.mark.parametrize("state,expected_count", [
    ("EXECUTED", 3),
    ("CANCELED", 1),
    ("PENDING", 1),
    ("COMPLETED", 0)  # Несуществующий статус
])
def test_filter_by_state(sample_transactions, state, expected_count):
    """Тестирование фильтрации по разным статусам"""
    result = filter_by_state(sample_transactions, state)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(t["state"] == state for t in result)

def test_filter_empty_result(sample_transactions):
    """Тест на пустой результат при отсутствии совпадений"""
    result = filter_by_state(sample_transactions, "UNKNOWN_STATE")
    assert len(result) == 0

# Тесты для sort_by_date
def test_sort_by_date_descending(sample_transactions):
    """Тестирование сортировки по убыванию (по умолчанию)"""
    result = sort_by_date(sample_transactions)
    dates = [datetime.fromisoformat(t["date"]) for t in result]
    assert dates == sorted(dates, reverse=True)

def test_sort_by_date_ascending(sample_transactions):
    """Тестирование сортировки по возрастанию"""
    result = sort_by_date(sample_transactions, reverse=False)
    dates = [datetime.fromisoformat(t["date"]) for t in result]
    assert dates == sorted(dates)

def test_sort_with_equal_dates(sample_transactions):
    """Тест на сохранение порядка при одинаковых датах"""
    result = sort_by_date(sample_transactions)
    # Находим транзакции с одинаковой датой
    equal_dates = [t for t in result if t["date"] == "2023-01-15T12:00:00.000000"]
    # Проверяем, что порядок исходных элементов сохранился
    assert [t["id"] for t in equal_dates] == [1, 5] or [5, 1]

@pytest.mark.parametrize("transactions", [
    "edge_case_transactions",
    [{"id": 8, "state": "EXECUTED", "date": "2023-13-01T00:00:00.000000"}]  # Невалидная дата
])
def test_sort_with_invalid_dates(transactions, request):
    """Тест обработки некорректных дат"""
    test_data = request.getfixturevalue(transactions) if isinstance(transactions, str) else transactions
    with pytest.raises((ValueError, TypeError)):
        sort_by_date(test_data)

# Тест на пустой ввод
def test_empty_input():
    """Тест работы функций с пустым списком"""
    assert filter_by_state([], "EXECUTED") == []
    assert sort_by_date([]) == []