def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state' (через цикл).
    """

    filtered_transactions = []
    for transaction in transactions:
        if transaction.get('state') == state:
            filtered_transactions.append(transaction)
    return filtered_transactions

def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате (ключ 'date').
    """
    return sorted(transactions, key=lambda x: x['date'], reverse=reverse)

