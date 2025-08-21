import datetime
import functools


def log(filename=None):
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename (str, optional): Имя файла для записи логов.
                                 Если None - вывод в консоль.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем информацию о вызове
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            # Пытаемся выполнить функцию
            try:
                result = func(*args, **kwargs)

                # Успешное выполнение
                log_message = (
                    f"{timestamp} - {func_name} - "
                    f"Аргументы: args={args}, kwargs={kwargs} - "
                    f"Результат: {result}"
                )

                # Записываем лог
                write_log(log_message, filename)
                return result

            except Exception as e:
                # Ошибка при выполнении
                error_message = (
                    f"{timestamp} - {func_name} - "
                    f"Аргументы: args={args}, kwargs={kwargs} - "
                    f"Ошибка: {type(e).__name__}: {e}"
                )

                # Записываем лог об ошибке
                write_log(error_message, filename)
                raise  # Пробрасываем ошибку дальше

        return wrapper

    return decorator


def write_log(message, filename):
    """Вспомогательная функция для записи лога"""
    if filename:
        # Запись в файл
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    else:
        # Вывод в консоль
        print(message)
