# Жуков Александр 5381


class Natural:
    """
    Модель натурального числа.

    Цифры хранятся от младшего разряда к старшему.
    Число 1234 хранится как [4, 3, 2, 1].

    Attributes:
        digits (list[int]): Массив цифр от младшего разряда к старшему.
        length (int): Количество разрядов числа.
    """

    def __init__(self, digits: list[int], need_reverse: bool = False) -> None:
        """
        Инициализация натурального числа из массива цифр.

        Args:
            digits (list[int]): Массив цифр числа.
            need_reverse (bool): Если True, массив разворачивается перед сохранением.

        Raises:
            ValueError: Параметры не соответствуют типам или значениям.
        """
        if not isinstance(digits, list) or not isinstance(need_reverse, bool):
            raise ValueError("Invalid value")
        if len(digits) == 0:
            raise ValueError("Invalid value")
        if not all(isinstance(d, int) and 0 <= d <= 9 for d in digits):
            raise ValueError("Invalid value")

        prepared = list(reversed(digits)) if need_reverse else list(digits)
        normalized = self._strip_leading_zeros(prepared)

        self.digits: list[int] = normalized
        self.length: int = len(normalized)

    @classmethod
    def from_str(cls, value: str, need_reverse: bool = False) -> "Natural":
        """
        Создание натурального числа из строки.

        Args:
            value (str): Строка из цифр 0-9.
            need_reverse (bool): Если True, строка трактуется как большая-маленькая.

        Raises:
            ValueError: Параметры не соответствуют типам или значениям.

        Returns:
            Natural: Натуральное число.
        """
        if not isinstance(value, str) or not isinstance(need_reverse, bool):
            raise ValueError("Invalid value")
        if len(value) == 0 or not value.isdigit():
            raise ValueError("Invalid value")

        digits = [int(ch) for ch in value]
        if not need_reverse:
            digits.reverse()
        return cls(digits, need_reverse=False)

    @classmethod
    def from_int(cls, value: int) -> "Natural":
        """
        Создание натурального числа из int.

        Args:
            value (int): Неотрицательное целое.
            need_reverse (bool): Не влияет на результат, оставлен для единообразия.

        Raises:
            ValueError: Параметры не соответствуют типам или значениям.

        Returns:
            Natural: Натуральное число.
        """
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Invalid value")
        if value < 0:
            raise ValueError("Invalid value")

        if value == 0:
            return cls([0], need_reverse=False)

        digits: list[int] = []
        while value > 0:
            digits.append(value % 10)
            value //= 10
        return cls(digits, need_reverse=False)

    @staticmethod
    def _strip_leading_zeros(digits: list[int]) -> list[int]:
        """
        Удаление ведущих нулей из массива (находятся в конце).

        Args:
            digits (list[int]): Массив цифр.

        Returns:
            list[int]: Массив без ведущих нулей. Для нуля вернёт [0].
        """
        result = list(digits)
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        return result

    def __str__(self) -> str:
        """
        Строковое представление числа.

        Returns:
            str: Число в обычной записи (например, "1234").
        """
        return "".join(str(d) for d in reversed(self.digits))

    def __repr__(self) -> str:
        """
        Отладочное представление.

        Returns:
            str: Строка вида "Natural(1234)".
        """
        return f"Natural({self})"

    def __int__(self) -> int:
        """
        Преобразование натурального числа в целое число.

        Returns:
            int: Целочисленное представление числа.
        """
        int_self = 0

        for digit in range(self.length - 1, -1, -1):
            int_self *= 10
            int_self += self.digits[digit]
        
        return int_self
