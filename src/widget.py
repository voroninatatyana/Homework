from .masks import get_mask_account  # относительный импорт
from .masks import get_mask_card_number


def mask_account_card (full_data: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа.
        Форматы:
        - Карта: "XXXX XX** **** XXXX" (16 цифр)
        - Счет: "**XXXX" (последние 4 цифры)"""
    #Извлекаем все цифры из строки
    mask_digits = ''.join([char for char in full_data if char.isdigit()])
    # Определяем тип по наличию ключевых слов
    #if mask_digits not digits:
     #   raise ValueError("Не найден номер карты/счета")
    if "счет" in full_data.lower():
        # Обработка счета
        if len(mask_digits) < 4:
            raise ValueError("Номер счета должен содержать минимум 4 цифры")
        masked_number = get_mask_card_number(mask_digits)
        # Сохраняем оригинальное название "Счет"
        account_prefix = "Счет"
        for word in full_data.split():
            if word.lower() == "счет":
                account_prefix = word
                break

        return f"{account_prefix} {masked_number}"
    else:
        # Обработка карты
        if len(mask_digits) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")

        masked_number = get_mask_card_number(mask_digits)
        # Сохраняем оригинальное название карты
        card_name = ' '.join([word for word in full_data.split() if not word.isdigit()])

        return f"{card_name} {masked_number}"

from datetime import datetime


def get_date_safe(iso_date_str: str) -> str | None:
    try:
        date_obj = datetime.fromisoformat(iso_date_str)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return None
