# Горшков Дмитрий 5381

from __future__ import annotations

from core.base.Formula import FormulaNode, FormulaTree
from core.base.FormulaLexer import Token, parse_linear_tokens


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
        return cls(parse_linear_tokens(text))

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

    @classmethod
    def from_tree(cls, tree: FormulaTree) -> PostfixFormula:
        """
        Построение постфиксной записи формулы по дереву.

        Args:
            a (FormulaTree): Дерево формулы.

        Raises:
            ValueError: Параметр не соответствует типу FormulaTree.

        Returns:
            PostfixFormula: Формула в постфиксной записи.
        """
        if not isinstance(tree, FormulaTree):
            raise ValueError("Invalid value")

        tokens: list[Token] = []

        def visit(node: FormulaNode) -> None:
            for child in node.children:
                visit(child)
            tokens.append(
                Token(kind=node.node_type.name, value=node.value, arity=len(node.children))
            )

        visit(tree.root)
        return cls(tokens)

    def to_tree(self) -> FormulaTree:
        """
        Построение дерева формулы по постфиксной записи.

        Returns:
            FormulaTree: Синтаксическое дерево формулы.
        """
        from core.base.Formula import FormulaTree

        return FormulaTree.from_postfix_tokens(self.tokens)


class PrefixFormula(_Notation):
    """Модель формулы в префиксной (польской) записи."""

    @classmethod
    def from_tree(cls, tree: FormulaTree) -> PrefixFormula:
        if not isinstance(tree, FormulaTree):
            raise ValueError("Invalid value")

        tokens: list[Token] = []

        def visit(node: FormulaNode) -> None:
            tokens.append(
                Token(kind=node.node_type.name, value=node.value, arity=len(node.children))
            )
            for child in node.children:
                visit(child)

        visit(tree.root)
        return cls(tokens)
