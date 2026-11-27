import pytest
from cas import execute_function
from core.base.Formula import FormulaNode, FormulaTree
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
        ("x ^ (2/4)", "x ^ 1/2"),
        ("x / (2/4)", "x / 1/2"),
        ("log((a + b), -(c * d))", "log(a + b, -(c * d))"),
    ],
)
def test_rem_prior_f_s_preserves_tree(expression, expected):
    tree = FormulaTree.from_str(expression)

    result = REM_PRIOR_F_S(tree)

    assert result == expected
    assert FormulaTree.from_str(result) == tree


def test_rem_prior_f_s_groups_negative_numeric_base():
    tree = FormulaTree(FormulaNode.op("^", FormulaNode.number("-1/2"), FormulaNode.var("x")))
    assert REM_PRIOR_F_S(tree) == "(-1/2) ^ x"


def test_rem_prior_f_s_cli():
    assert execute_function("REM_PRIOR_F_S", ["a + (b * c)"]) == "a + b * c"


def test_rem_prior_f_s_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        REM_PRIOR_F_S("a + b")
