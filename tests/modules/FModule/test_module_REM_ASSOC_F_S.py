import pytest
from core.base.Formula import FormulaTree
from core.base.FormulaNotation import PostfixFormula
from core.modules.FModule.REM_ASSOC_F_S import REM_ASSOC_F_S


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("a * (b * c)", "a * b * c"),
        ("(a * b) * (c * d)", "a * b * c * d"),
        ("(a + b) * (c * d)", "(a + b) * c * d"),
        ("a * (b / c)", "a * (b / c)"),
        ("a / (b * (c * d))", "(a / (b * c * d))"),
        ("sin(a * (b * c)) + d", "(sin(a * b * c) + d)"),
    ],
)
def test_rem_assoc_f_s(expression, expected):
    assert REM_ASSOC_F_S(FormulaTree.from_str(expression)) == expected


def test_rem_assoc_f_s_preserves_rational_exponent():
    tree = PostfixFormula.from_str("x 1/2 ^ a * b *").to_tree()
    assert REM_ASSOC_F_S(tree) == "(x ^ (1/2)) * a * b"


def test_rem_assoc_f_s_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        REM_ASSOC_F_S("a * b")
