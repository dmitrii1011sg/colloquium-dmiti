# Горшков Дмитрий 5381

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Iterable, Union

from core.base.Rational import Rational
from core.modules.QModule.RED_Q_Q import RED_Q_Q
from core.modules.QModule.SUB_QQ_Q import SUB_QQ_Q


class NodeType(IntEnum):
    NUMBER = auto()
    VARIABLE = auto()
    OPERATOR = auto()
    FUNCTION = auto()


ALLOWED_FUNCTIONS: dict[str, int] = {
    "sin": 1,
    "cos": 1,
    "tg": 1,
    "ctg": 1,
    "sqrt": 1,
    "exp": 1,
    "ln": 1,
    "log": 2,
}

BINARY_OPERATORS = {"+", "-", "*", "/", "^"}
UNARY_OPERATORS = {"u-"}
ALL_OPERATORS = BINARY_OPERATORS | UNARY_OPERATORS

OPERATOR_PRECEDENCE: dict[str, int] = {"+": 1, "-": 1, "*": 2, "/": 2, "u-": 3, "^": 4}
RIGHT_ASSOCIATIVE = {"^", "u-"}

_TOKEN_RE = re.compile(
    r"\s*(?:(?P<NUMBER>\d+(?:/\d+)?)|(?P<IDENT>[A-Za-z_]\w*)|"
    r"(?P<OP>u-|[\+\-\*/\^])|(?P<LPAREN>\()|(?P<RPAREN>\))|(?P<COMMA>,))"
)


@dataclass(frozen=True, slots=True)
class Token:
    """
    Атомарный токен символьной формулы.

    Attributes:
        kind (str): Категория токена ("NUMBER", "VARIABLE", "OPERATOR",
            "FUNCTION", "LPAREN", "RPAREN", "COMMA").
        value (Rational | str): Значение токена.
        arity (int): Арность операции или функции.
    """

    kind: str
    value: Union[Rational, str]
    arity: int = 0

    def __eq__(self, other: object) -> bool:
        """
        Сравнение двух токенов с учётом равенства рациональных чисел

        Args:
            other (object): Токен с которым сравниваем.

        Returns:
            bool: Результат сравнения.
        """
        if not isinstance(other, Token) or self.kind != other.kind or self.arity != other.arity:
            return False if isinstance(other, Token) else NotImplemented

        if isinstance(self.value, Rational) and isinstance(other.value, Rational):
            return SUB_QQ_Q(self.value, other.value).is_zero()

        return self.value == other.value

    def __str__(self) -> str:
        """
        Строковое представление токена.

        Returns:
            str: Представление токена.
        """
        return str(self.value)


def tokenize_infix(expr: str) -> list[Token]:
    """
    Разбиение инфиксной строки формулы на список токенов с выделением унарного минуса.

    Args:
        expr (str): Строка формулы в инфиксной записи.

    Raises:
        ValueError: Если строка пуста или содержит неизвестные символы.

    Returns:
        list[Token]: Список токенов формулы.
    """
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("Пустая строка формулы")

    raw: list[Token] = []
    pos = 0
    while pos < len(expr):
        if expr[pos].isspace():
            pos += 1
            continue

        match = _TOKEN_RE.match(expr, pos)
        if not match:
            raise ValueError(f"Неожиданный символ на позиции {pos}: '{expr[pos:]}'")

        pos = match.end()
        group, text = match.lastgroup, match.group(match.lastgroup)  # type: ignore[arg-type]

        if group == "NUMBER":
            if "/" in text:
                num_s, den_s = text.split("/", 1)
                raw.extend(
                    [
                        Token("NUMBER", RED_Q_Q(Rational.from_str(num_s))),
                        Token("OPERATOR", "/", arity=2),
                        Token("NUMBER", RED_Q_Q(Rational.from_str(den_s))),
                    ]
                )
            else:
                raw.append(Token("NUMBER", RED_Q_Q(Rational.from_str(text))))
        elif group == "IDENT":
            if text in ALLOWED_FUNCTIONS:
                raw.append(Token("FUNCTION", text, arity=ALLOWED_FUNCTIONS[text]))
            else:
                raw.append(Token("VARIABLE", text))
        elif group == "OP":
            raw.append(Token("OPERATOR", text, arity=1 if text == "u-" else 2))
        else:
            raw.append(Token(group, text))  # type: ignore[arg-type]

    tokens: list[Token] = []
    for tok in raw:
        prev = tokens[-1] if tokens else None
        unary_ctx = prev is None or prev.kind in ("OPERATOR", "LPAREN", "COMMA")
        if tok.kind == "OPERATOR" and tok.value == "-" and unary_ctx:
            tokens.append(Token("OPERATOR", "u-", arity=1))
        elif not (tok.kind == "OPERATOR" and tok.value == "+" and unary_ctx):
            tokens.append(tok)
    return tokens


def infix_tokens_to_postfix(tokens: list[Token]) -> list[Token]:
    """
    Перевод инфиксных токенов в обратную польскую запись (алгоритм сортировочной станции).

    Args:
        tokens (list[Token]): Токены в инфиксном порядке.

    Raises:
        ValueError: При нарушении баланса скобок или синтаксиса вызова функций.

    Returns:
        list[Token]: Токены в постфиксном порядке.
    """
    output: list[Token] = []
    stack: list[Token] = []

    for tok in tokens:
        if tok.kind in ("NUMBER", "VARIABLE"):
            output.append(tok)
        elif tok.kind in ("FUNCTION", "LPAREN"):
            stack.append(tok)
        elif tok.kind == "COMMA":
            while stack and stack[-1].kind != "LPAREN":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Некорректная расстановка скобок или запятой")
        elif tok.kind == "OPERATOR":
            op1 = str(tok.value)
            p1 = OPERATOR_PRECEDENCE[op1]
            while stack and stack[-1].kind in ("OPERATOR", "FUNCTION"):
                top = stack[-1]
                if top.kind == "FUNCTION":
                    output.append(stack.pop())
                else:
                    p2 = OPERATOR_PRECEDENCE[str(top.value)]
                    if (op1 not in RIGHT_ASSOCIATIVE and p1 <= p2) or (
                        op1 in RIGHT_ASSOCIATIVE and p1 < p2
                    ):
                        output.append(stack.pop())
                    else:
                        break
            stack.append(tok)
        elif tok.kind == "RPAREN":
            while stack and stack[-1].kind != "LPAREN":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Лишняя закрывающая скобка ')'")
            stack.pop()
            if stack and stack[-1].kind == "FUNCTION":
                output.append(stack.pop())

    while stack:
        top = stack.pop()
        if top.kind in ("LPAREN", "RPAREN"):
            raise ValueError("Незакрытая скобка '('")
        output.append(top)

    return output


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
        return FormulaNode(self.node_type, self.value, [c.copy() for c in self.children])

    def node_count(self) -> int:
        return 1 + sum(c.node_count() for c in self.children)

    def to_ascii_tree(self, prefix: str = "", is_last: bool = True, is_root: bool = True) -> str:
        conn = "" if is_root else ("└── " if is_last else "├── ")
        lines = [f"{prefix}{conn}{self.value}"]
        next_prefix = "" if is_root else prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            lines.append(child.to_ascii_tree(next_prefix, i == len(self.children) - 1, False))
        return "\n".join(lines)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FormulaNode) or self.node_type != other.node_type:
            return False if isinstance(other, FormulaNode) else NotImplemented
        if isinstance(self.value, Rational) and isinstance(other.value, Rational):
            same_val = SUB_QQ_Q(self.value, other.value).is_zero()
        else:
            same_val = self.value == other.value
        return same_val and self.children == other.children

    def __str__(self) -> str:
        if self.node_type in (NodeType.NUMBER, NodeType.VARIABLE):
            return str(self.value)
        if self.node_type == NodeType.OPERATOR:
            if self.value == "u-":
                return f"(-{self.children[0]})"
            return f"({self.children[0]} {self.value} {self.children[1]})"
        return f"{self.value}({', '.join(str(c) for c in self.children)})"

    def __repr__(self) -> str:
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
        """Построение дерева формулы из инфиксной строки."""
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
        """Глубокое копирование дерева."""
        return FormulaTree(self.root.copy())

    def node_count(self) -> int:
        """Количество узлов в дереве."""
        return self.root.node_count()

    def to_ascii_tree(self) -> str:
        """Псевдографическое представление дерева."""
        return self.root.to_ascii_tree()

    def __eq__(self, other: object) -> bool:
        """Сравнение двух деревьев формул."""
        return self.root == other.root if isinstance(other, FormulaTree) else NotImplemented

    def __str__(self) -> str:
        """Полная скобочная запись формулы."""
        return str(self.root)

    def __repr__(self) -> str:
        """Отладочное представление дерева."""
        return f"FormulaTree({self})"


class _Notation:
    """Базовый класс для линейных бесскобочных записей формулы (префиксной и постфиксной)."""

    __slots__ = ("tokens",)

    def __init__(self, tokens: list[Token]) -> None:
        """
        Инициализация последовательности токенов.

        Args:
            tokens (list[Token]): Непустой список токенов.

        Raises:
            ValueError: Если список пуст или содержит некорректные элементы.
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
        """Парсинг строки с токенами, разделёнными пробелами."""
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
        """Сравнение двух записей одного типа."""
        return self.tokens == other.tokens if type(other) is type(self) else NotImplemented

    def __str__(self) -> str:
        """Строковое представление (токены через пробел)."""
        return " ".join(str(t) for t in self.tokens)

    def __repr__(self) -> str:
        """Отладочное представление."""
        return f"{type(self).__name__}({str(self)!r})"


class PostfixFormula(_Notation):
    """Формула в постфиксной (обратной польской) записи."""

    @classmethod
    def from_tree(cls, a: FormulaTree) -> PostfixFormula:
        """
        Построение постфиксной записи формулы по дереву.

        Args:
            a (FormulaTree): Дерево формулы.

        Raises:
            ValueError: Параметр не соответствует типу.

        Returns:
            PostfixFormula: Формула в постфиксной записи.
        """
        if not isinstance(a, FormulaTree):
            raise ValueError("Invalid value")

        stack_tokens: list[Token] = []

        def visit(node: FormulaNode) -> None:
            for child in node.children:
                visit(child)

            kind = node.node_type.name
            arity = len(node.children)
            token = Token(kind=kind, value=node.value, arity=arity)
            stack_tokens.append(token)

        visit(a.root)
        return cls(stack_tokens)

    def to_tree(self) -> FormulaTree:
        """Построение дерева формулы по постфиксной записи."""
        return FormulaTree.from_postfix_tokens(self.tokens)


class PrefixFormula(_Notation):
    """Формула в префиксной (польской) записи."""
