# Горшков Дмитрий 5381

import pytest
from core.base.Formula import (
    FormulaNode,
    FormulaTree,
    NodeType,
    PostfixFormula,
    PrefixFormula,
    Token,
    infix_tokens_to_postfix,
    tokenize_infix,
)
from core.base.Rational import Rational

# --- Тесты Token и лексера (tokenize_infix) ---


def test_token_equality_and_str():
    t1 = Token("NUMBER", Rational.from_str("2/4"))
    t2 = Token("NUMBER", Rational.from_str("1/2"))
    t3 = Token("NUMBER", Rational.from_str("1/3"))
    t_var = Token("VARIABLE", "x")

    assert t1 == t2
    assert t1 != t3
    assert t1 != t_var
    assert str(t2) == "1/2"
    assert str(t_var) == "x"


def test_tokenize_basic_and_functions():
    tokens = tokenize_infix("3*x + sin(y) - log(2, z)")
    kinds_vals = [(t.kind, str(t.value), t.arity) for t in tokens]

    assert kinds_vals == [
        ("NUMBER", "3", 0),
        ("OPERATOR", "*", 2),
        ("VARIABLE", "x", 0),
        ("OPERATOR", "+", 2),
        ("FUNCTION", "sin", 1),
        ("LPAREN", "(", 0),
        ("VARIABLE", "y", 0),
        ("RPAREN", ")", 0),
        ("OPERATOR", "-", 2),
        ("FUNCTION", "log", 2),
        ("LPAREN", "(", 0),
        ("NUMBER", "2", 0),
        ("COMMA", ",", 0),
        ("VARIABLE", "z", 0),
        ("RPAREN", ")", 0),
    ]


def test_tokenize_unary_minus_and_plus():
    tokens = tokenize_infix("-x + (-3) * sin(-y) + +5")
    ops = [(t.kind, str(t.value), t.arity) for t in tokens if t.kind == "OPERATOR"]

    assert ops == [
        ("OPERATOR", "u-", 1),
        ("OPERATOR", "+", 2),
        ("OPERATOR", "u-", 1),
        ("OPERATOR", "*", 2),
        ("OPERATOR", "u-", 1),
        ("OPERATOR", "+", 2),
    ]


def test_tokenize_fraction_literal():
    tokens = tokenize_infix("3/4 * x")
    assert [(t.kind, str(t.value)) for t in tokens] == [
        ("NUMBER", "3"),
        ("OPERATOR", "/"),
        ("NUMBER", "4"),
        ("OPERATOR", "*"),
        ("VARIABLE", "x"),
    ]


@pytest.mark.parametrize("bad_expr", ["", "   ", "2 @ x", "x $ 1"])
def test_tokenize_invalid_input(bad_expr):
    with pytest.raises(ValueError):
        tokenize_infix(bad_expr)


# --- Тесты сортировочной станции (infix_tokens_to_postfix) ---


def test_infix_to_postfix_precedence_and_associativity():
    # Правоассоциативность степени: 2 ^ 3 ^ 2 -> 2 3 2 ^ ^
    pf_pow = infix_tokens_to_postfix(tokenize_infix("2 ^ 3 ^ 2"))
    assert [str(t) for t in pf_pow] == ["2", "3", "2", "^", "^"]

    # Левоассоциативность вычитания и приоритет умножения: a - b * c + d -> a b c * - d +
    pf_arith = infix_tokens_to_postfix(tokenize_infix("a - b * c + d"))
    assert [str(t) for t in pf_arith] == ["a", "b", "c", "*", "-", "d", "+"]


def test_infix_to_postfix_functions_and_brackets():
    pf = infix_tokens_to_postfix(tokenize_infix("log(2 + 1, sqrt(x))"))
    assert [str(t) for t in pf] == ["2", "1", "+", "x", "sqrt", "log"]


@pytest.mark.parametrize("bad_expr", ["(x + 1", "x + 1)", "log(2, 3", "2, 3"])
def test_infix_to_postfix_unbalanced_brackets(bad_expr):
    with pytest.raises(ValueError):
        infix_tokens_to_postfix(tokenize_infix(bad_expr))


# --- Тесты FormulaNode ---


def test_formula_node_validation():
    num = FormulaNode(NodeType.NUMBER, Rational.from_str("2/4"))
    assert str(num) == "1/2"  # автоматически сокращено через RED_Q_Q

    var = FormulaNode(NodeType.VARIABLE, "x_1")
    assert str(var) == "x_1"

    # Ошибки валидации узлов
    with pytest.raises(ValueError):
        FormulaNode(NodeType.NUMBER, "5")  # не Rational
    with pytest.raises(ValueError):
        FormulaNode(NodeType.NUMBER, Rational.from_str("1"), [var])  # потомки у листа
    with pytest.raises(ValueError):
        FormulaNode(NodeType.VARIABLE, "123bad")  # некорректный идентификатор
    with pytest.raises(ValueError):
        FormulaNode(NodeType.OPERATOR, "+", [var])  # мало операндов для бинарного +
    with pytest.raises(ValueError):
        FormulaNode(NodeType.OPERATOR, "u-", [var, var])  # много операндов для u-
    with pytest.raises(ValueError):
        FormulaNode(NodeType.FUNCTION, "unknown_fn", [var])
    with pytest.raises(ValueError):
        FormulaNode(NodeType.FUNCTION, "log", [var])  # log требует 2 аргумента


def test_formula_node_copy_eq_and_ascii():
    tree1 = FormulaTree.from_str("sin(x) + 1")
    tree2 = tree1.copy()

    assert tree1 == tree2
    assert tree1.root is not tree2.root
    assert tree1.root.children[0] is not tree2.root.children[0]
    assert tree1.node_count() == 4

    ascii_repr = tree1.to_ascii_tree()
    assert "+" in ascii_repr
    assert "sin" in ascii_repr
    assert "x" in ascii_repr


# --- Тесты FormulaTree ---


def test_formula_tree_from_str_and_brackets():
    tree = FormulaTree.from_str("-x + 3 * cos(y)")
    assert str(tree) == "((-x) + (3 * cos(y)))"


def test_formula_tree_all_elementary_functions():
    expr = "sin(x) + cos(x) + tg(x) + ctg(x) + sqrt(x) + exp(x) + ln(x) + log(2, x)"
    tree = FormulaTree.from_str(expr)
    assert tree.node_count() == 24


def test_formula_tree_from_postfix_errors():
    # Недостаточно операндов
    with pytest.raises(ValueError):
        FormulaTree.from_postfix_tokens([Token("OPERATOR", "+", arity=2)])

    # Лишние операнды в стеке
    with pytest.raises(ValueError):
        FormulaTree.from_postfix_tokens(
            [
                Token("VARIABLE", "x"),
                Token("VARIABLE", "y"),
            ]
        )

    # Недопустимый токен (скобка в ОПН)
    with pytest.raises(ValueError):
        FormulaTree.from_postfix_tokens([Token("LPAREN", "(")])


# --- Тесты PostfixFormula и PrefixFormula ---


def test_postfix_and_prefix_notation_roundtrip():
    pf = PostfixFormula.from_str("x 2/4 ^ 3 x * + sin")
    assert str(pf) == "x 1/2 ^ 3 x * + sin"

    tree = FormulaTree.from_postfix_tokens(pf.tokens)
    assert str(tree) == "sin(((x ^ 1/2) + (3 * x)))"

    pref = PrefixFormula.from_str("+ ^ x 2 * 3 x")
    assert str(pref) == "+ ^ x 2 * 3 x"
    assert pref != pf  # разные типы нотаций не равны даже при одинаковых токенах


def test_postfix_formula_tree_roundtrip():
    tree = FormulaTree.from_str("log(2, -x)")
    postfix = PostfixFormula.from_tree(tree)

    assert postfix.tokens == [
        Token("NUMBER", Rational.from_str("2")),
        Token("VARIABLE", "x"),
        Token("OPERATOR", "u-", arity=1),
        Token("FUNCTION", "log", arity=2),
    ]
    assert postfix.to_tree() == tree


def test_postfix_formula_from_tree_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        PostfixFormula.from_tree("x")


@pytest.mark.parametrize("cls", [PostfixFormula, PrefixFormula])
def test_notation_invalid_inputs(cls):
    with pytest.raises(ValueError):
        cls([])
    with pytest.raises(ValueError):
        cls(["not_a_token"])
    with pytest.raises(ValueError):
        cls.from_str("   ")
    with pytest.raises(ValueError):
        cls.from_str("x 2 @")
