
def get_mask_card_number (data: str) -> str:
    """Маскирует номер карты/счета.

    Args:
        data: Строка с номером карты/счета

    Returns:
        Маскированную строку

    Raises:
        TypeError: Если вход не строка
        ValueError: Если строка слишком короткая
    """
    # Приводим к строке и удаляем пробелы/дефисы
    str_number = str(data).strip().replace(" ", "").replace("-", "")

    # Проверяем, что номер состоит из цифр и имеет правильную длину
    if not isinstance(data, str):
        raise TypeError(f"Ожидается строка, получено {type(data)}")
    if len(data) < 16:
        raise ValueError("Номер карты слишком короткий")
    if not str_number.isdigit():
        raise TypeError("Номер карты должен содержать цифры")

    # Разбиваем на части и маскируем
    first_part = str_number[:4]  # Первые 4 цифры
    second_part = str_number[4:6]  # Следующие 2 цифры
    last_part = str_number[-4:]  # Последние 4 цифры

    return f"{first_part} {second_part}** **** {last_part}"


def get_mask_account(data: str | int) -> str:
    """Маскирует номер банковского счета"""
    if not isinstance(data, (str, int)):
        raise TypeError("Номер счета должен быть строкой или числом")
    # Преобразуем в строку и удаляем лишнее
    str_num = str(data).replace("Счет", "").strip()
    # Проверяем минимальную длину
    if len(str_num) < 10:
        raise ValueError("Номер счета должен содержать минимум 10 цифр")
    # Оставляем только цифры
    digits = [c for c in str_num if c.isdigit()]
    if len(digits) < 10:
        raise ValueError("Номер счета должен содержать минимум 10 цифр")
    last_four = "".join(digits)[-4:]
    return f"**{last_four}"  # Последние 4 цифры с ** в начале
