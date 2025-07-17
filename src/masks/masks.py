def get_mask_card_number (card_number: str) -> str:
    """Маскирует номер банковской карты."""
    # Приводим к строке и удаляем пробелы/дефисы
    str_number = str(card_number).strip().replace(" ", "").replace("-", "")

    # Проверяем, что номер состоит из цифр и имеет правильную длину
    if not str_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    if len(str_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Разбиваем на части и маскируем
    first_part = str_number[:4]  # Первые 4 цифры
    second_part = str_number[4:6]  # Следующие 2 цифры
    last_part = str_number[-4:]  # Последние 4 цифры

    return f"{first_part} {second_part}** **** {last_part}"

def get_mask_account ( account_number: str) -> str:
    """Маскирует номер банковского счета"""
    str_number = str(account_number)  # На случай, если передано число
    if len(str_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")
    return f"**{str_number[-4:]}"  # Последние 4 цифры с ** в начале