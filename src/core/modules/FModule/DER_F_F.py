# Литвиненко Владимир 5381

from core.base.Formula import FormulaNode, FormulaTree, NodeType
from core.base.Rational import Rational
from core.modules.QModule.SUB_QQ_Q import SUB_QQ_Q
from core.modules.QModule.MUL_QQ_Q import MUL_QQ_Q
from core.modules.QModule.DIV_QQ_Q import DIV_QQ_Q

Q0 = Rational.from_str("0")
Q1 = Rational.from_str("1")
ZERO = FormulaNode(NodeType.NUMBER, Q0)
ONE = FormulaNode(NodeType.NUMBER, Q1)
TWO = FormulaNode(NodeType.NUMBER, Rational.from_str("2"))


def _num(q: Rational) -> FormulaNode:
    """
    Создание узла-числа

    Args:
        q (Rational): рациональное число (числитель и знаменатель)

    Returns:
        FormulaNode: узел типа NUMBER с нормализованным значением
    """
    return FormulaNode(NodeType.NUMBER, q)


def _op(o: str, *c: FormulaNode) -> FormulaNode:
    """
    Создание узла-оператора

    Args:
        o (str): символ оператора (+, -, *, /, ^, u-)
        c (FormulaNode): один ребёнок для унарного оператора или два — для бинарного

    Returns:
        FormulaNode: узел типа OPERATOR
    """
    return FormulaNode(NodeType.OPERATOR, o, list(c))


def _fn(f: str, *c: FormulaNode) -> FormulaNode:
    """
    Создание узла-функции

    Args:
        f (str): имя функции (sin, cos, tg, ctg, sqrt, exp, ln, log)
        c (FormulaNode): один или два аргумента функции согласно её арности

    Returns:
        FormulaNode: узел типа FUNCTION
    """
    return FormulaNode(NodeType.FUNCTION, f, list(c))


def _zero(n: FormulaNode) -> bool:
    """
    Проверка, является ли узел числовым нулём

    Args:
        n (FormulaNode): проверяемый узел

    Returns:
        bool: True, если узел — NUMBER и его значение равно нулю
    """
    return (
        n.node_type == NodeType.NUMBER
        and isinstance(n.value, Rational)
        and n.value.is_zero()
    )


def _diff(n: FormulaNode, var: str) -> FormulaNode:
    """
    Символьное дифференцирование поддерева по заданной переменной

    Args:
        n (FormulaNode): корень поддерева, которое дифференцируется
        var (str): имя переменной, по которой идёт дифференцирование

    Raises:
        ValueError: встретился неподдерживаемый оператор, функция или тип узла

    Returns:
        FormulaNode: корень дерева-производной (без упрощения)
    """
    if n.node_type == NodeType.NUMBER:
        return ZERO
    if n.node_type == NodeType.VARIABLE:
        return ONE if n.value == var else ZERO

    if n.node_type == NodeType.OPERATOR:
        op = str(n.value)
        if op == "u-":
            return _op("u-", _diff(n.children[0], var))
        u, v = n.children
        if op == "+":
            return _op("+", _diff(u, var), _diff(v, var))
        if op == "-":
            return _op("-", _diff(u, var), _diff(v, var))
        if op == "*":
            return _op("+", _op("*", _diff(u, var), v), _op("*", u, _diff(v, var)))
        if op == "/":
            return _op(
                "/",
                _op("-", _op("*", _diff(u, var), v), _op("*", u, _diff(v, var))),
                _op("^", v, TWO),
            )
        if op == "^":
            if v.node_type == NodeType.NUMBER and isinstance(v.value, Rational):
                return _op(
                    "*",
                    _op("*", _num(v.value), _op("^", u, _num(SUB_QQ_Q(v.value, Q1)))),
                    _diff(u, var),
                )
            else:
                return _op(
                    "*",
                    _op("^", u, v),
                    _op(
                        "+",
                        _op("*", _diff(v, var), _fn("ln", u)),
                        _op("*", v, _op("/", _diff(u, var), u))
                    )
                )
        raise ValueError(f"Неподдерживаемый оператор: {op!r}")

    if n.node_type == NodeType.FUNCTION:
        f = str(n.value)
        if f == "log":
            u, v = n.children
            du, dv = _diff(u, var), _diff(v, var)
            num = _op(
                "-",
                _op("*", _op("/", dv, v), _fn("ln", u)),
                _op("*", _fn("ln", v), _op("/", du, u))
            )
            den = _op("^", _fn("ln", u), TWO)
            return _op("/", num, den)
        u = n.children[0]
        du = _diff(u, var)
        if f == "sin":  return _op("*", _fn("cos", u), du)
        if f == "cos":  return _op("u-", _op("*", _fn("sin", u), du))
        if f == "tg":   return _op("/", du, _op("^", _fn("cos", u), TWO))
        if f == "ctg":  return _op("u-", _op("/", du, _op("^", _fn("sin", u), TWO)))
        if f == "sqrt": return _op("/", du, _op("*", TWO, _fn("sqrt", u)))
        if f == "exp":  return _op("*", _fn("exp", u), du)
        if f == "ln":   return _op("/", du, u)
        raise ValueError(f"Неподдерживаемая функция: {f!r}")

    raise ValueError(f"Неподдерживаемый тип узла: {n.node_type!r}")


def _fold(n: FormulaNode) -> FormulaNode:
    """
    Свёртка числовых поддеревьев и тривиальных алгебраических тождеств

    Args:
        n (FormulaNode): корень поддерева, которое упрощается

    Returns:
        FormulaNode: корень эквивалентного, но более простого поддерева
    """
    if n.node_type == NodeType.FUNCTION:
        return _fn(str(n.value), *[_fold(c) for c in n.children])
    
    if n.node_type != NodeType.OPERATOR:
        return n
    k = [_fold(c) for c in n.children]
    op = str(n.value)

    if op == "u-":
        u = k[0]
        if u.node_type == NodeType.NUMBER and isinstance(u.value, Rational):
            return _num(SUB_QQ_Q(Q0, u.value))
        if u.node_type == NodeType.OPERATOR and u.value == "u-":
            return u.children[0]
        return _op("u-", u)

    u, v = k
    if (
        u.node_type == NodeType.NUMBER
        and v.node_type == NodeType.NUMBER
        and isinstance(u.value, Rational)
        and isinstance(v.value, Rational)
    ):
        if op == "+": return _num(SUB_QQ_Q(u.value, SUB_QQ_Q(Q0, v.value)))
        if op == "-": return _num(SUB_QQ_Q(u.value, v.value))
        if op == "*": return _num(MUL_QQ_Q(u.value, v.value))
        if op == "/" and not v.value.is_zero(): return _num(DIV_QQ_Q(u.value, v.value))

    if op == "+":
        if _zero(u): return v
        if _zero(v): return u
    elif op == "-":
        if _zero(u): return _op("u-", v)
        if _zero(v): return u
    elif op == "*":
        if _zero(u) or _zero(v): return ZERO
        if u == ONE: return v
        if v == ONE: return u
    elif op == "/":
        if _zero(u): return ZERO
        if v == ONE: return u
    elif op == "^":
        if v == ONE: return u
        if _zero(v): return ONE
        if _zero(u): return ZERO
        if u == ONE: return ONE

    return _op(op, u, v)


def DER_F_F(tree: FormulaTree, var: str = "x", simplify: bool = True) -> FormulaTree:
    """
    Символьное дифференцирование дерева формулы по заданной переменной

    Args:
        tree (FormulaTree): дерево исходной формулы
        var (str): имя переменной дифференцирования (по умолчанию 'x')
        simplify (bool): применять ли свёртку констант к результату

    Raises:
        ValueError: параметр tree не является FormulaTree,
                    параметр var не является корректным идентификатором

    Returns:
        FormulaTree: дерево производной (со свёрткой или без — по флагу simplify)
    """
    if not isinstance(tree, FormulaTree) or not isinstance(var, str) or not var.isidentifier():
        raise ValueError("Invalid value")
    root = _diff(tree.root, var)
    return FormulaTree(_fold(root) if simplify else root)