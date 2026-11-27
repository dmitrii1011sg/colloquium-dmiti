# Горшков Дмитрий 5381

from __future__ import annotations

from enum import IntEnum, auto
from io import StringIO
from typing import Callable, Iterable, Union

from core.base.FormulaLexer import (
    ALL_OPERATORS,
    ALLOWED_FUNCTIONS,
    BINARY_OPERATORS,
    OPERATOR_PRECEDENCE,
    RIGHT_ASSOCIATIVE,
    UNARY_OPERATORS,
    Token,
    infix_tokens_to_postfix,
    tokenize_infix,
)
from core.base.FormulaNotation import PostfixFormula, PrefixFormula
from core.base.Rational import Rational
from core.modules.QModule.RED_Q_Q import RED_Q_Q
from core.modules.QModule.SUB_QQ_Q import SUB_QQ_Q

__all__ = [
    "ALL_OPERATORS",
    "ALLOWED_FUNCTIONS",
    "BINARY_OPERATORS",
    "OPERATOR_PRECEDENCE",
    "RIGHT_ASSOCIATIVE",
    "UNARY_OPERATORS",
    "FormulaNode",
    "FormulaTree",
    "NodeType",
    "PostfixFormula",
    "PrefixFormula",
    "Token",
    "infix_tokens_to_postfix",
    "needs_parentheses",
    "tokenize_infix",
]


def needs_parentheses(operator: str, parent: str | None, right_child: bool) -> bool:
    """Нужны ли скобки для сохранения связи двух операторов при повторном разборе."""
    if parent is None:
        return False
    precedence = OPERATOR_PRECEDENCE[operator]
    parent_precedence = OPERATOR_PRECEDENCE[parent]
    if precedence != parent_precedence:
        return precedence < parent_precedence
    return not right_child if parent in RIGHT_ASSOCIATIVE else right_child


class NodeType(IntEnum):
    """
    Перечисление типов узлов синтаксического дерева формулы.

    Attributes:
        NUMBER (int): Рациональное число (включая целые со знаменателем 1).
        VARIABLE (int): Символьная переменная.
        OPERATOR (int): Арифметический или степенной оператор.
        FUNCTION (int): Элементарная математическая функция.
    """

    NUMBER = auto()
    VARIABLE = auto()
    OPERATOR = auto()
    FUNCTION = auto()


class FormulaNode:
    """
    Узел синтаксического дерева символьной формулы.

    Attributes:
        node_type (NodeType): Тип узла.
        value (Rational | str): Значение узла.
        children (list[FormulaNode]): Дочерние узлы.
    """

    __slots__ = ("node_type", "value", "children")

    def __init__(
        self,
        node_type: NodeType,
        value: Union[Rational, str],
        children: list[FormulaNode] | None = None,
    ) -> None:
        """
        Инициализация узла дерева с проверкой арности и типов.

        Args:
            node_type (NodeType): Тип узла.
            value (Rational | str): Значение узла.
            children (list[FormulaNode] | None): Список потомков.

        Raises:
            ValueError: При несоответствии типа, значения или числа потомков.
        """
        if not isinstance(node_type, NodeType):
            raise ValueError("Invalid node_type")

        self.children: list[FormulaNode] = list(children) if children else []
        self.node_type: NodeType = node_type

        if node_type == NodeType.NUMBER:
            if not isinstance(value, Rational) or self.children:
                raise ValueError("NUMBER требует Rational без потомков")
            self.value: Union[Rational, str] = RED_Q_Q(value)
        elif node_type == NodeType.VARIABLE:
            if not isinstance(value, str) or not value.isidentifier() or self.children:
                raise ValueError(f"Некорректная переменная: {value!r}")
            self.value = value
        elif node_type == NodeType.OPERATOR:
            arity = 1 if value in UNARY_OPERATORS else 2
            if value not in ALL_OPERATORS or len(self.children) != arity:
                raise ValueError(f"Некорректный оператор '{value}' или число операндов")
            self.value = str(value)
        elif node_type == NodeType.FUNCTION:
            if (
                value not in ALLOWED_FUNCTIONS
                or len(self.children) != ALLOWED_FUNCTIONS[str(value)]
            ):
                raise ValueError(f"Некорректная функция '{value}' или число аргументов")
            self.value = str(value)

    def copy(self) -> FormulaNode:
        """
        Создание глубокой копии поддерева с корнем в текущем узле.

        Returns:
            FormulaNode: Независимая копия поддерева.
        """
        return FormulaNode(self.node_type, self.value, [c.copy() for c in self.children])

    def node_count(self) -> int:
        """
        Подсчёт общего количества узлов в поддереве.

        Returns:
            int: Количество узлов, включая текущий узел.
        """
        return 1 + sum(c.node_count() for c in self.children)

    def to_ascii_tree(self, prefix: str = "", is_last: bool = True, is_root: bool = True) -> str:
        """
        Формирование псевдографического представления поддерева.

        Args:
            prefix (str): Строковый отступ текущего уровня.
            is_last (bool): Флаг последнего потомка у родительского узла.
            is_root (bool): Флаг корневого узла.

        Returns:
            str: Многострочное дерево с символами ветвления.
        """
        conn = "" if is_root else ("└── " if is_last else "├── ")
        lines = [f"{prefix}{conn}{self.value}"]
        next_prefix = "" if is_root else prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            lines.append(child.to_ascii_tree(next_prefix, i == len(self.children) - 1, False))
        return "\n".join(lines)

    def __eq__(self, other: object) -> bool:
        """
        Структурное сравнение двух поддеревьев.

        Args:
            other (object): Объект для сравнения.

        Returns:
            bool: True, если типы, значения и все потомки узлов совпадают; иначе False.
        """
        if not isinstance(other, FormulaNode) or self.node_type != other.node_type:
            return False if isinstance(other, FormulaNode) else NotImplemented
        if isinstance(self.value, Rational) and isinstance(other.value, Rational):
            same_val = SUB_QQ_Q(self.value, other.value).is_zero()
        else:
            same_val = self.value == other.value
        return same_val and self.children == other.children

    def __str__(self) -> str:
        """
        Формирование строковой записи поддерева с полной расстановкой скобок.

        Returns:
            str: Полная скобочная запись поддерева.
        """
        if self.node_type in (NodeType.NUMBER, NodeType.VARIABLE):
            return str(self.value)
        if self.node_type == NodeType.OPERATOR:
            if self.value == "u-":
                return f"(-{self.children[0]})"
            return f"({self.children[0]} {self.value} {self.children[1]})"
        return f"{self.value}({', '.join(str(c) for c in self.children)})"

    def __repr__(self) -> str:
        """
        Отладочное представление узла дерева.

        Returns:
            str: Строка вида "FormulaNode(OPERATOR, '+', children=[...])".
        """
        return f"FormulaNode({self.node_type.name}, {self.value!r}, children={self.children!r})"


class FormulaTree:
    """
    Синтаксическое дерево символьной формулы.

    Attributes:
        root (FormulaNode): Корневой узел дерева.
    """

    __slots__ = ("root",)

    def __init__(self, root: FormulaNode) -> None:
        """
        Инициализация дерева формулы.

        Args:
            root (FormulaNode): Корневой узел.

        Raises:
            ValueError: Если root не является экземпляром FormulaNode.
        """
        if not isinstance(root, FormulaNode):
            raise ValueError("root должен быть экземпляром FormulaNode")
        self.root: FormulaNode = root

    @classmethod
    def from_str(cls, expr: str) -> FormulaTree:
        """
        Построение дерева формулы из инфиксной строки.

        Args:
            expr (str): Строка символьного выражения в инфиксной записи.

        Raises:
            ValueError: Если строка пуста или синтаксически некорректна.

        Returns:
            FormulaTree: Построенное синтаксическое дерево формулы.
        """
        return cls.from_postfix_tokens(infix_tokens_to_postfix(tokenize_infix(expr)))

    @classmethod
    def from_postfix_tokens(cls, tokens: Iterable[Token]) -> FormulaTree:
        """
        Построение дерева формулы из последовательности постфиксных токенов.

        Args:
            tokens (Iterable[Token]): Токены в обратной польской записи.

        Raises:
            ValueError: При некорректной постфиксной последовательности.

        Returns:
            FormulaTree: Построенное дерево.
        """
        stack: list[FormulaNode] = []
        for tok in tokens:
            if tok.kind == "NUMBER":
                stack.append(FormulaNode(NodeType.NUMBER, tok.value))
            elif tok.kind == "VARIABLE":
                stack.append(FormulaNode(NodeType.VARIABLE, str(tok.value)))
            elif tok.kind in ("OPERATOR", "FUNCTION"):
                arity = (
                    1
                    if tok.value in UNARY_OPERATORS
                    else (2 if tok.kind == "OPERATOR" else ALLOWED_FUNCTIONS[str(tok.value)])
                )
                if len(stack) < arity:
                    raise ValueError(f"Недостаточно операндов для '{tok.value}'")
                args = [stack.pop() for _ in range(arity)][::-1]
                ntype = NodeType.OPERATOR if tok.kind == "OPERATOR" else NodeType.FUNCTION
                stack.append(FormulaNode(ntype, str(tok.value), args))
            else:
                raise ValueError(f"Недопустимый токен: {tok}")

        if len(stack) != 1:
            raise ValueError("Некорректная постфиксная запись")
        return cls(stack[0])

    def copy(self) -> FormulaTree:
        """
        Создание глубокой копии дерева формулы.

        Returns:
            FormulaTree: Независимая копия дерева.
        """
        return FormulaTree(self.root.copy())

    def node_count(self) -> int:
        """
        Подсчёт общего количества узлов в дереве.

        Returns:
            int: Количество узлов в дереве.
        """
        return self.root.node_count()

    def to_ascii_tree(self) -> str:
        """
        Получение псевдографического представления дерева.

        Returns:
            str: Строковое дерево с отступами и ветвлением.
        """
        return self.root.to_ascii_tree()

    def rewrite_parentheses(
        self,
        text: str,
        keep_operator: Callable[[str, str | None, bool], bool],
    ) -> str:
        """Изменить скобки в полной скобочной записи этого дерева по заданному правилу."""
        source = StringIO(text)
        parts: list[str] = []

        def visit(node: FormulaNode, parent: str | None = None, right_child: bool = False) -> None:
            """Прочитать из исходной записи фрагмент, соответствующий текущему узлу."""
            if node.node_type in (NodeType.NUMBER, NodeType.VARIABLE):
                value = source.read(len(str(node.value)))
                if node.node_type == NodeType.NUMBER:
                    # При повторном разборе дробь и знак минуса становятся операциями.
                    operator = None
                    if "/" in value:
                        operator = "/"
                    elif value.startswith("-"):
                        operator = "u-"
                    if operator is not None and needs_parentheses(operator, parent, right_child):
                        value = f"({value})"
                parts.append(value)
                return

            if node.node_type == NodeType.FUNCTION:
                parts.append(source.read(len(str(node.value)) + 1))
                for index, child in enumerate(node.children):
                    if index:
                        parts.append(source.read(2))  # Запятая и пробел.
                    visit(child)
                parts.append(source.read(1))
                return

            operator = str(node.value)
            keep = keep_operator(operator, parent, right_child)
            opening = source.read(1)
            if keep:
                parts.append(opening)

            if operator == "u-":
                parts.append(source.read(1))
                visit(node.children[0], operator, right_child=True)
            else:
                visit(node.children[0], operator)
                parts.append(source.read(len(operator) + 2))  # Оператор с пробелами.
                visit(node.children[1], operator, right_child=True)

            closing = source.read(1)
            if keep:
                parts.append(closing)

        visit(self.root)
        return "".join(parts)

    def __eq__(self, other: object) -> bool:
        """
        Сравнение двух деревьев формул на структурное равенство.

        Args:
            other (object): Объект для сравнения.

        Returns:
            bool: True, если деревья идентичны по структуре и значениям; иначе False.
        """
        return self.root == other.root if isinstance(other, FormulaTree) else NotImplemented

    def __str__(self) -> str:
        """
        Строковое представление дерева в полной скобочной записи.

        Returns:
            str: Полная скобочная запись формулы.
        """
        return str(self.root)

    def __repr__(self) -> str:
        """
        Отладочное представление дерева формулы.

        Returns:
            str: Строка вида "FormulaTree((x + 1))".
        """
        return f"FormulaTree({self})"
