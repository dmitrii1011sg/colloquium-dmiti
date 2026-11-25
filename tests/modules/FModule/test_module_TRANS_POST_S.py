# Помаскин Макар 5381

import pytest
from core.base.FormulaNotation import PostfixFormula
from core.modules.FModule.TRANS_POST_S import TRANS_POST_S


@pytest.mark.parametrize(
    ("postfix", "expected"),
    [
        ("x 2/4 ^", "(x ^ 1/2)"),
        ("a b c * -", "(a - (b * c))"),
        ("2 x u- log", "log(2, (-x))"),
    ],
)
def test_trans_post_s(postfix, expected):
    formula = PostfixFormula.from_str(postfix)
    assert TRANS_POST_S(formula) == expected


@pytest.mark.parametrize("postfix", ["x +", "x y"])
def test_trans_post_s_invalid_notation(postfix):
    formula = PostfixFormula.from_str(postfix)
    with pytest.raises(ValueError):
        TRANS_POST_S(formula)


@pytest.mark.parametrize("value", [None, "x"])
def test_trans_post_s_invalid_input(value):
    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_POST_S(value)
