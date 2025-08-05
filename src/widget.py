from datetime import datetime


def mask_account_card(data: str) -> str:
    """Маскирует номер карты или счета.

    Для карт: XXXX XX** **** XXXX (16 цифр)
    Для счетов: **XXXX (последние 4 цифры)

    Args:
        data: Строка формата "[Название] номер"

    Returns:
        Маскированную строку

    Raises:
        TypeError: Если вход не строка
        ValueError: Если номер не соответствует требованиям
    """
    if not isinstance(data, str):
        raise TypeError("Только строковый ввод")

    # Удаляем лишние пробелы и разделяем на части
    cleaned_data = " ".join(data.split())
    parts = cleaned_data.split()

    if not parts:
        raise ValueError("Пустой ввод")

    # Определяем тип данных (карта или счет)
    is_account = "Счет" in cleaned_data

    # Извлекаем номер (последняя часть после разделения)
    number = parts[-1] if parts else ""

    if is_account:
        # Валидация счета
        if len(parts) < 2:
            raise ValueError("Отсутствует номер счета")
        if len(number) < 4 or not number.isdigit():
            raise ValueError("Номер счета должен содержать минимум 4 цифры")
        return f"Счет **{number[-4:]}"
    else:
        # Валидация карты
        if len(number) != 16 or not number.isdigit():
            raise ValueError("Номер карты должен содержать 16 цифр")

        # Форматирование карты
        name = " ".join(parts[:-1]) if len(parts) > 1 else ""
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        return f"{name} {masked_number}" if name else masked_number


def get_date_safe(date_str: str | None) -> str | None:
    if not isinstance(date_str, str):
        return date_str
    try:
        return datetime.fromisoformat(date_str).strftime("%d.%m.%Y")
    except ValueError:
        return date_str
