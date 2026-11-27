# Горшков Дмитрий 5381

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union

from core.base.Rational import Rational
from core.modules.QModule.RED_Q_Q import RED_Q_Q
from core.modules.QModule.SUB_QQ_Q import SUB_QQ_Q

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

_INFIX_TOKEN_RE = re.compile(
    r"\s*(?:(?P<NUMBER>\d+(?:/\d+)?)|(?P<IDENT>[A-Za-z_]\w*)|"
    r"(?P<OP>[\+\-\*/\^])|(?P<LPAREN>\()|(?P<RPAREN>\))|(?P<COMMA>,))"
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
        if not isinstance(other, Token) or self.kind != other.kind or self.arity != other.arity:
            return False if isinstance(other, Token) else NotImplemented

        if isinstance(self.value, Rational) and isinstance(other.value, Rational):
            return SUB_QQ_Q(self.value, other.value).is_zero()

        return self.value == other.value

    def __str__(self) -> str:
        return str(self.value)


def tokenize_infix(expr: str) -> list[Token]:
    """
    Разбиение инфиксной строки формулы на список токенов с выделением унарного минуса.

    Args:
        expr (str): Строка формулы в инфиксной записи.

    Raises:
        ValueError: Если строка пуста, не является строкой или содержит неизвестные символы.

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

        match = _INFIX_TOKEN_RE.match(expr, pos)
        if not match:
            raise ValueError(f"Неожиданный символ на позиции {pos}: '{expr[pos:]}'")

        pos = match.end()
        group, text = match.lastgroup, match.group(match.lastgroup)  # type: ignore[arg-type]

        if group == "NUMBER":
            raw.append(Token("NUMBER", RED_Q_Q(Rational.from_str(text))))
        elif group == "IDENT":
            if text in ALLOWED_FUNCTIONS:
                raw.append(Token("FUNCTION", text, arity=ALLOWED_FUNCTIONS[text]))
            else:
                raw.append(Token("VARIABLE", text))
        elif group == "OP":
            raw.append(Token("OPERATOR", text, arity=2))
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


def parse_linear_tokens(text: str) -> list[Token]:
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
    return tokens


def infix_tokens_to_postfix(tokens: list[Token]) -> list[Token]:
    """
    Перевод инфиксных токенов в обратную польскую запись (алгоритм сортировочной станции).

    Args:
        tokens (list[Token]): Список токенов в инфиксном порядке.

    Raises:
        ValueError: При нарушении баланса скобок или синтаксиса вызова функций.

    Returns:
        list[Token]: Список токенов в постфиксном порядке.
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
