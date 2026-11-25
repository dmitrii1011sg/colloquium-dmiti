# Горшков Дмитрий 5381

from __future__ import annotations

import re

from core.base.FormulaLexer import (
    ALL_OPERATORS,
    ALLOWED_FUNCTIONS,
    UNARY_OPERATORS,
    Token,
)
from core.base.Rational import Rational
from core.modules.QModule.RED_Q_Q import RED_Q_Q


class _Notation:
    """
    Базовый класс для линейных бесскобочных записей формулы (префиксной и постфиксной).

    Attributes:
        tokens (list[Token]): Упорядоченный список токенов формулы.
    """

    __slots__ = ("tokens",)

    def __init__(self, tokens: list[Token]) -> None:
        """
        Инициализация последовательности токенов.

        Args:
            tokens (list[Token]): Непустой список токенов.

        Raises:
            ValueError: Если список пуст или содержит элементы, не являющиеся Token.
        """
        if (
            not isinstance(tokens, list)
            or not tokens
            or not all(isinstance(t, Token) for t in tokens)
        ):
            raise ValueError("Требуется непустой список Token")
        self.tokens: list[Token] = list(tokens)

    @classmethod
    def from_str(cls, text: str):
        """
        Создание линейной записи формулы из строки с токенами, разделёнными пробелами.

        Args:
            text (str): Строка токенов через пробел (например, "x 2 ^ 3 x * +").

        Raises:
            ValueError: Если строка пуста или содержит неизвестный токен.

        Returns:
            _Notation: Экземпляр соответствующего класса нотации.
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Пустая строка записи")
        tokens: list[Token] = []
        for part in text.strip().split():
            if part in ALL_OPERATORS:
                tokens.append(Token("OPERATOR", part, arity=1 if part in UNARY_OPERATORS else 2))
            elif part in ALLOWED_FUNCTIONS:
                tokens.append(Token("FUNCTION", part, arity=ALLOWED_FUNCTIONS[part]))
            elif re.fullmatch(r"[+-]?\d+(?:/\d+)?", part):
                tokens.append(Token("NUMBER", RED_Q_Q(Rational.from_str(part))))
            elif part.isidentifier():
                tokens.append(Token("VARIABLE", part))
            else:
                raise ValueError(f"Неизвестный токен: '{part}'")
        return cls(tokens)

    def __eq__(self, other: object) -> bool:
        """
        Проверка равенства двух записей одного типа.

        Args:
            other (object): Объект для сравнения.

        Returns:
            bool: True, если типы и последовательности токенов совпадают; иначе False.
        """
        return self.tokens == other.tokens if type(other) is type(self) else NotImplemented

    def __str__(self) -> str:
        """
        Строковое представление записи (токены через пробел).

        Returns:
            str: Строка токенов, разделённых пробелами.
        """
        return " ".join(str(t) for t in self.tokens)

    def __repr__(self) -> str:
        """
        Отладочное представление записи.

        Returns:
            str: Строка вида "PostfixFormula('x 2 ^')".
        """
        return f"{type(self).__name__}({str(self)!r})"


class PostfixFormula(_Notation):
    """Модель формулы в постфиксной (обратной польской) записи."""


class PrefixFormula(_Notation):
    """Модель формулы в префиксной (польской) записи."""
