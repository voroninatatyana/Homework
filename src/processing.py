from datetime import datetime
def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state' (через цикл).
    """

    filtered_transactions = []
    for transaction in transactions:
        if transaction.get('state') == state:
            filtered_transactions.append(transaction)
    return filtered_transactions


"""функция явно проверяет валидность дат"""
def validate_date(date_str: str) -> bool:
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")
    valid_transactions = []
    for t in transactions:
        if "date" not in t:
            continue
        try:
            parse_date(t["date"])  # Проверяем валидность даты
            valid_transactions.append(t)
        except ValueError:
            continue


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортировка транзакций по дате с проверкой валидности дат.
    """

    return sorted(
        [t for t in transactions if "date" in t and validate_date(t["date"])],
        key=lambda x: datetime.fromisoformat(x["date"]),
        reverse=reverse
    )
