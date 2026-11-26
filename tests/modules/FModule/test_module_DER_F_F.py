# Литвиненко Владимир 5381

import pytest
from core.base.Formula import FormulaTree
from core.modules.FModule.DER_F_F import DER_F_F


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("x", "1"),
        ("3", "0"),
        ("y", "0"),
        ("x + x + x", "3"),
        ("x^3", "(3 * (x ^ 2))"),
        ("sin(x)", "cos(x)"),
        ("exp(x)", "exp(x)"),
        ("ln(x)", "(1 / x)"),
        ("tg(x)", "(1 / (cos(x) ^ 2))"),
        ("sqrt(x)", "(1 / (2 * sqrt(x)))"),
    ],
)
def test_der_f_f(expr, expected):
    tree = FormulaTree.from_str(expr)
    result = DER_F_F(tree)
    assert isinstance(result, FormulaTree)
    assert str(result) == expected


def test_der_f_f_var():
    tree = FormulaTree.from_str("z^2 + z")
    assert str(DER_F_F(tree, var="z")) == "((2 * (z ^ 1)) + 1)"
    assert str(DER_F_F(tree, var="x")) == "0"


def test_der_f_f_structural_equality():
    tree = FormulaTree.from_str("x^2 + 5*x")
    expected = FormulaTree.from_str("2*x^1 + 5")
    assert DER_F_F(tree) == expected


def test_der_f_f_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        DER_F_F("x")    # type: ignore