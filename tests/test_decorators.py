import pytest
import functools
from src.decorators import log


# Тестовые функции для декорирования
def successful_function(a, b):
    """Функция, которая всегда выполняется успешно"""
    return a + b


def error_function(a, b):
    """Функция, которая всегда вызывает ошибку"""
    raise ValueError("Custom error message")


def function_with_kwargs(a, b=10):
    """Функция с ключевыми аргументами"""
    return a * b


# Тесты для логирования в консоль
class TestConsoleLogging:
    """Тесты для вывода логов в консоль"""

    def test_successful_execution_console(self, capsys):
        """Тест успешного выполнения с выводом в консоль"""

        @log()
        def test_func(a, b):
            return a + b

        result = test_func(5, 3)

        # Проверяем результат
        assert result == 8

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out.strip()

        # Проверяем содержание лога
        assert "test_func" in output
        assert "Аргументы: args=(5, 3), kwargs={}" in output
        assert "Результат: 8" in output
        assert "Ошибка:" not in output

    def test_error_execution_console(self, capsys):
        """Тест ошибки выполнения с выводом в консоль"""

        @log()
        def test_func(a, b):
            raise ValueError("Test error")

        # Проверяем, что ошибка пробрасывается
        with pytest.raises(ValueError, match="Test error"):
            test_func(5, 3)

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out.strip()

        # Проверяем содержание лога об ошибке
        assert "test_func" in output
        assert "Аргументы: args=(5, 3), kwargs={}" in output
        assert "Ошибка: ValueError: Test error" in output
        assert "Результат:" not in output

    def test_function_with_kwargs_console(self, capsys):
        """Тест функции с ключевыми аргументами"""

        @log()
        def test_func(a, b=2):
            return a * b

        result = test_func(5, b=3)

        # Проверяем результат
        assert result == 15

        # Перехватываем вывод
        captured = capsys.readouterr()
        output = captured.out.strip()

        # Проверяем содержание лога
        assert "test_func" in output
        assert "Аргументы: args=(5,), kwargs={'b': 3}" in output
        assert "Результат: 15" in output


# Тесты для логирования в файл
class TestFileLogging:
    """Тесты для записи логов в файл"""

    @pytest.fixture
    def log_file(self, tmp_path):
        """Фикстура для создания временного файла логов"""
        return tmp_path / "test.log"

    def test_successful_execution_file(self, log_file):
        """Тест успешного выполнения с записью в файл"""

        @log(filename=str(log_file))
        def test_func(a, b):
            return a - b

        result = test_func(10, 4)

        # Проверяем результат
        assert result == 6

        # Проверяем запись в файл
        assert log_file.exists()

        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        assert "test_func" in content
        assert "Аргументы: args=(10, 4), kwargs={}" in content
        assert "Результат: 6" in content
        assert "Ошибка:" not in content

    def test_error_execution_file(self, log_file):
        """Тест ошибки выполнения с записью в файл"""

        @log(filename=str(log_file))
        def test_func(a, b):
            raise TypeError("Type error occurred")

        # Проверяем, что ошибка пробрасывается
        with pytest.raises(TypeError, match="Type error occurred"):
            test_func("string", 5)

        # Проверяем запись в файл
        assert log_file.exists()

        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        assert "test_func" in content
        assert "Аргументы: args=('string', 5), kwargs={}" in content
        assert "Ошибка: TypeError: Type error occurred" in content

    def test_multiple_calls_file(self, log_file):
        """Тест множественных вызовов с записью в файл"""

        @log(filename=str(log_file))
        def test_func(x):
            return x * 2

        # Множественные вызовы
        test_func(1)
        test_func(2)
        test_func(3)

        # Проверяем, что все вызовы записаны
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert all("test_func" in line for line in lines)
        assert any("Результат: 2" in line for line in lines)
        assert any("Результат: 4" in line for line in lines)
        assert any("Результат: 6" in line for line in lines)


# Тесты для различных типов ошибок
class TestErrorTypes:
    """Тесты для различных типов исключений"""

    def test_different_error_types_console(self, capsys):
        """Тест различных типов ошибок"""

        @log()
        def zero_division():
            return 10 / 0

        @log()
        def type_error():
            return "string" + 5

        @log()
        def index_error():
            return [][0]

        # Тестируем ZeroDivisionError
        with pytest.raises(ZeroDivisionError):
            zero_division()

        captured = capsys.readouterr()
        assert "ZeroDivisionError" in captured.out

        # Тестируем TypeError
        with pytest.raises(TypeError):
            type_error()

        captured = capsys.readouterr()
        assert "TypeError" in captured.out

        # Тестируем IndexError
        with pytest.raises(IndexError):
            index_error()

        captured = capsys.readouterr()
        assert "IndexError" in captured.out


# Тесты для проверки формата вывода
class TestOutputFormat:
    """Тесты для проверки формата вывода"""

    def test_timestamp_format(self, capsys):
        """Тест формата временной метки"""

        @log()
        def test_func():
            return "success"

        test_func()

        captured = capsys.readouterr()
        output = captured.out.strip()

        # Проверяем формат timestamp (YYYY-MM-DD HH:MM:SS)
        import re
        timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        assert re.search(timestamp_pattern, output) is not None

    def test_function_name_preservation(self, capsys):
        """Тест сохранения имени функции"""

        @log()
        def very_long_function_name_for_testing():
            return "test"

        very_long_function_name_for_testing()

        captured = capsys.readouterr()
        output = captured.out.strip()

        # Проверяем, что имя функции сохранилось
        assert "very_long_function_name_for_testing" in output


# Тесты для edge cases
class TestEdgeCases:
    """Тесты для граничных случаев"""

    def test_empty_arguments(self, capsys):
        """Тест функции без аргументов"""

        @log()
        def no_args():
            return "no args"

        result = no_args()
        assert result == "no args"

        captured = capsys.readouterr()
        output = captured.out.strip()

        assert "Аргументы: args=(), kwargs={}" in output

    def test_none_return(self, capsys):
        """Тест функции, возвращающей None"""

        @log()
        def return_none():
            return None

        result = return_none()
        assert result is None

        captured = capsys.readouterr()
        output = captured.out.strip()

        assert "Результат: None" in output
