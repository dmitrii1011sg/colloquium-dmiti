import pytest
from core.base.Formula import FormulaTree
from core.base.FormulaNotation import PostfixFormula
from core.modules.FModule.SIMP_01_F_F import SIMP_01_F_F


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("0 + (x + 0)", "x"),
        ("1 * (x * 1)", "x"),
        ("(1 + 0) * (x + 0)", "x"),
        ("log(1 * x, sin(0 + y * 1))", "log(x, sin(y))"),
        ("0 + 0", "0"),
        ("1 * 1", "1"),
        ("0 * x + (x ^ 1)", "0 * x + (x ^ 1)"),
    ],
)
def test_simp_01_f_f(expression, expected):
    tree = FormulaTree.from_str(expression)
    original = tree.copy()

    result = SIMP_01_F_F(tree)

    assert result == FormulaTree.from_str(expected)
    assert tree == original


def test_simp_01_f_f_normalized_rational_identity():
    tree = PostfixFormula.from_str("0/5 x 3/3 * +").to_tree()
    assert SIMP_01_F_F(tree) == FormulaTree.from_str("x")


def test_simp_01_f_f_returns_independent_tree():
    tree = FormulaTree.from_str("0 + (x + y)")

    result = SIMP_01_F_F(tree)
    result.root.children[0].value = "z"

    assert tree == FormulaTree.from_str("0 + (x + y)")


def test_simp_01_f_f_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        SIMP_01_F_F("0 + x")
