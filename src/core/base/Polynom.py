from __future__ import annotations

from core.base.Rational import Rational

# Жуков Александр 5381


class Polynom:
    """
    Модель многочлена с рациональными коэффициентами.

    Коэффициенты хранятся от младшей степени к старшей.
    Например, многочлен 5x^2 + 3 хранится как [3, 0, 5].

    Attributes:
        coefficients (list[Rational]): Коэффициенты многочлена.
        degree (int): Степень многочлена.
    """

    def __init__(self, coefficients: list[Rational]) -> None:
        """
        Инициализация многочлена.

        Args:
            coefficients (list[Rational]): Коэффициенты от младшей степени
                к старшей.

        Raises:
            ValueError: Если параметры не соответствуют типам или значениям.
        """
        if not isinstance(coefficients, list):
            raise ValueError("Invalid value")
        if len(coefficients) == 0:
            raise ValueError("Invalid value")
        if not all(isinstance(c, Rational) for c in coefficients):
            raise ValueError("Invalid value")

        normalized = self._strip_leading_zeros(coefficients)
        self.coefficients: list[Rational] = normalized
        self.degree: int = len(normalized) - 1

    @staticmethod
    def _strip_leading_zeros(coeffs: list[Rational]) -> list[Rational]:
        """
        Удаление нулевых коэффициентов при старших степенях.

        Args:
            coeffs (list[Rational]): Исходный список коэффициентов.

        Returns:
            list[Rational]: Список без старших нулевых коэффициентов.
                Для нуль-многочлена вернёт список с одним нулевым элементом.
        """
        result = list(coeffs)
        while len(result) > 1 and Polynom._is_zero(result[-1]):
            result.pop()
        return result

    @staticmethod
    def _is_zero(r: Rational) -> bool:
        """
        Проверка рационального числа на равенство нулю.

        Args:
            r (Rational): Рациональное число.

        Returns:
            bool: True, если числитель равен нулю.
        """
        n = r.numer.number
        return n.length == 1 and n.digits[0] == 0

    def __str__(self) -> str:
        """
        Строковое представление многочлена.

        Возвращает читаемый вид от старшей степени к младшей:
        "5x^2 + 3", "-2x + 1/2", "0".

        Returns:
            str: Многочлен в обычной записи.
        """
        if self.degree == 0 and self._is_zero(self.coefficients[0]):
            return "0"

        parts: list[str] = []
        for power in range(self.degree, -1, -1):
            coef = self.coefficients[power]
            if self._is_zero(coef):
                continue

            coef_str = str(coef)
            is_negative = coef_str.startswith("-")
            abs_coef_str = coef_str[1:] if is_negative else coef_str

            if power == 0:
                term = abs_coef_str
            else:
                if abs_coef_str == "1":
                    body = ""
                else:
                    body = abs_coef_str
                var = "x" if power == 1 else f"x^{power}"
                term = f"{body}{var}"

            if not parts:
                parts.append(f"-{term}" if is_negative else term)
            else:
                parts.append(f" - {term}" if is_negative else f" + {term}")

        return "".join(parts)

    def __repr__(self) -> str:
        """
        Отладочное представление.

        Returns:
            str: Строка вида "Polynom(5x^2 + 3)".
        """
        return f"Polynom({self})"
