from __future__ import annotations

import re

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

    __slots__ = ("coefficients", "degree")

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

    def is_zero(self) -> bool:
        return self.degree == 0 and self.coefficients[0].is_zero()

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
        while len(result) > 1 and result[-1].is_zero():
            result.pop()
        return result

    @staticmethod
    def _expand_brackets(s: str) -> str:
        """
        Раскрытие группирующих скобок в строке многочлена.

        Поддерживаются скобки любой глубины вложенности и унарный минус
        перед скобкой: "-(2x+1)" -> "-2x-1", "3x-(x-1)" -> "3x-x+1".
        Умножение на скобку (вида "2(x+1)" или "(x+1)(x-1)") не поддерживается.

        Args:
            s (str): Строка без пробелов.

        Raises:
            ValueError: Скобки несбалансированы или перед скобкой стоит
                символ, означающий умножение.

        Returns:
            str: Строка без скобок.
        """
        if s.count("(") != s.count(")"):
            raise ValueError("Unbalanced brackets")

        inner = re.compile(r"\(([^()]*)\)")

        while "(" in s:
            match = inner.search(s)
            if match is None:
                raise ValueError("Unbalanced brackets")

            start, end = match.span()
            content = match.group(1)

            if len(content) == 0:
                raise ValueError("Empty brackets")

            left_char = s[start - 1] if start > 0 else ""
            right_char = s[end] if end < len(s) else ""

            sign_char = "+"
            prefix_end = start
            if left_char in ("+", "-"):
                sign_char = left_char
                prefix_end = start - 1
            elif left_char not in ("", "("):
                raise ValueError(
                    f"Multiplication by bracketed group is not supported: '{left_char}('"
                )

            if right_char not in ("", "+", "-", ")"):
                raise ValueError(
                    f"Multiplication by bracketed group is not supported: ')${right_char}'"
                )

            if sign_char == "-":
                expanded = Polynom._flip_signs(content)
            else:
                expanded = content

            need_plus_glue = (
                prefix_end > 0
                and s[prefix_end - 1] not in "+-("
                and expanded
                and expanded[0] not in "+-"
            )
            if need_plus_glue:
                expanded = "+" + expanded
            elif (prefix_end == 0 or s[prefix_end - 1] == "(") and expanded.startswith("+"):
                expanded = expanded[1:]

            s = s[:prefix_end] + expanded + s[end:]

        return s

    @staticmethod
    def _flip_signs(expr: str) -> str:
        """
        Инверсия знаков всех слагаемых в выражении без скобок.

        Args:
            expr (str): Выражение без скобок, например "2x-1" или "-x+3".

        Returns:
            str: Выражение с инвертированными знаками: "-2x+1", "x-3".
        """
        if len(expr) == 0:
            return expr

        if expr[0] not in "+-":
            expr = "+" + expr

        flipped_chars: list[str] = []
        for ch in expr:
            if ch == "+":
                flipped_chars.append("-")
            elif ch == "-":
                flipped_chars.append("+")
            else:
                flipped_chars.append(ch)

        result = "".join(flipped_chars)
        if result.startswith("+"):
            result = result[1:]
        return result

    @staticmethod
    def from_str(s: str) -> Polynom:
        """
        Создание многочлена из строки.

        Args:
            value (str): Строка многочлена.

        Raises:
            ValueError: Параметры не соответствуют типам или значениям.

        Returns:
            Polynom: Многочлен.
        """
        s = s.replace(" ", "")
        s = Polynom._expand_brackets(s)
        s = s.replace("-", "+-")
        parts = s.split("+")

        poly_dict = {}
        max_degree = 0

        for part in parts:
            if not part:
                continue

            if "x^" in part:
                coeff_part, degree_part = part.split("x^")
                degree = int(degree_part)
            elif "x" in part:
                coeff_part = part.replace("x", "")
                degree = 1
            else:
                coeff_part = part
                degree = 0

            if coeff_part == "" or coeff_part == "+":
                coeff = Rational.from_str("1")
            elif coeff_part == "-":
                coeff = Rational.from_str("-1")
            else:
                coeff = Rational.from_str(coeff_part)

            if degree in poly_dict:
                raise ValueError(f"Duplicate degree {degree} is not supported")
            poly_dict[degree] = coeff
            max_degree = max(max_degree, degree)

        coefficients = []
        for i in range(max_degree + 1):
            coefficients.append(poly_dict.get(i, Rational.from_str("0")))

        return Polynom(coefficients)

    def __str__(self) -> str:
        """
        Строковое представление многочлена.

        Возвращает читаемый вид от старшей степени к младшей:
        "5x^2 + 3", "-2x + 1/2", "0".

        Returns:
            str: Многочлен в обычной записи.
        """
        if self.is_zero():
            return "0"

        parts: list[str] = []
        for power in range(self.degree, -1, -1):
            coef = self.coefficients[power]
            if coef.is_zero():
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
