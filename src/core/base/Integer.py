# Горшков Дмитрий 5381

from core.base.Natural import Natural


class Integer:
    """
    Модель целого числа.

    Attributes:
        number (Natural): Абсолютная величина числа (натуральное).
        sign (int): Знак числа: 0 положительное, 1 отрицательное.
    """

    def __init__(self, number: Natural, sign: int = 0) -> None:
        """
        Инициализация целого числа.

        Args:
            number (Natural): Натуральное число (модуль).
            sign (int): Знак (0 или 1).

        Raises:
            ValueError: Если параметры не соответствуют типам.
        """
        if not isinstance(number, Natural) or not isinstance(sign, int):
            raise ValueError("Invalid value")

        if sign not in [0, 1]:
            raise ValueError("Sign must be 0 or 1")

        self.sign = 0 if number.length == 1 and number.digits[0] == 0 else sign
        self.number = number

    @classmethod
    def from_str(cls, value: str) -> "Integer":
        """
        Создание целого числа из строки.

        Args:
            value (str): Строка из цифр 0-9.

        Raises:
            ValueError: Параметры не соответствуют типам или значениям.

        Returns:
            Integer: Целое число.
        """
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Invalid value")

        sign = 0
        number_part = value

        if value[0] in ("+", "-"):
            sign = 1 if value[0] == "-" else 0
            number_part = value[1:]

        if not number_part:
            raise ValueError("No digits after sign")

        if not number_part.isdigit():
            raise ValueError(f"Invalid characters in number: {number_part}")

        return cls(Natural.from_str(number_part), sign)

    @classmethod
    def from_int(cls, value: int) -> "Integer":
        """
        Создание целого числа из стандартного int.

        Args:
            value (int): число.

        Raises:
            ValueError: Параметры не соответствуют типам или значениям.

        Returns:
            Integer: Целое число.
        """
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Invalid value")

        sign = 1 if value < 0 else 0
        return cls(Natural.from_int(abs(value)), sign)

    def __str__(self) -> str:
        """
        Строковое представление целого числа.

        Returns:
            str: Число в обычной записи (например, "-1234").
        """
        prefix = "-" if self.sign == 1 else ""
        return f"{prefix}{self.number}"

    def __repr__(self) -> str:
        """
        Отладочное представление.

        Returns:
            str: Строка вида "Integer(1234)".
        """
        return f"Integer({self})"

    def __int__(self) -> int:
        """
        Преобразование в стандартный int Python.

        Returns:
            int: Целочисленное представление числа.
        """
        value = int(self.number)
        return -value if self.sign == 1 else value
