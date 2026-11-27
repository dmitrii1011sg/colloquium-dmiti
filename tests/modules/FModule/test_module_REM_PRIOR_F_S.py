import pytest
from core.base.Formula import FormulaTree
from core.base.FormulaNotation import PostfixFormula
from core.modules.FModule.REM_PRIOR_F_S import REM_PRIOR_F_S


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("a + (b * c)", "a + b * c"),
        ("(a + b) * c", "(a + b) * c"),
        ("(a - b) - c", "a - b - c"),
        ("a - (b - c)", "a - (b - c)"),
        ("a / (b * c)", "a / (b * c)"),
        ("(a ^ b) ^ c", "(a ^ b) ^ c"),
        ("a ^ (b ^ c)", "a ^ b ^ c"),
        ("a ^ (-b)", "a ^ (-b)"),
        ("-(a ^ b)", "-a ^ b"),
        ("log((a + b), -(c * d))", "log(a + b, -(c * d))"),
    ],
)
def test_rem_prior_f_s_preserves_tree(expression, expected):
    tree = FormulaTree.from_str(expression)

    result = REM_PRIOR_F_S(tree)

    assert result == expected
    assert FormulaTree.from_str(result) == tree


@pytest.mark.parametrize(
    ("postfix", "expected"),
    [
        ("x 2/4 ^", "x ^ (1/2)"),
        ("-2 x ^", "(-2) ^ x"),
        ("x 2/4 /", "x / (1/2)"),
    ],
)
def test_rem_prior_f_s_groups_numeric_tokens(postfix, expected):
    tree = PostfixFormula.from_str(postfix).to_tree()
    assert REM_PRIOR_F_S(tree) == expected


def test_rem_prior_f_s_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        REM_PRIOR_F_S("a + b")
