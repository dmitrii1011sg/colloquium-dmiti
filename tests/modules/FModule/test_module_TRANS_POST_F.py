# Литвиненко Владимир 5381

import pytest
from core.base.Formula import FormulaTree
from core.base.FormulaNotation import PostfixFormula
from core.modules.FModule.TRANS_POST_F import TRANS_POST_F


@pytest.mark.parametrize(
    ("postfix", "expected"),
    [
        ("7", "7"),
        ("x y z + *", "(x * (y + z))"),
        ("x 2 ^ 1 +", "((x ^ 2) + 1)"),
        ("x y sin + 3 *", "((x + sin(y)) * 3)"),
        ("x u- 2 ^", "((-x) ^ 2)"),
    ],
)
def test_trans_post_f(postfix, expected):
    pf = PostfixFormula.from_str(postfix)
    result = TRANS_POST_F(pf)
    assert isinstance(result, FormulaTree)
    assert str(result) == expected


def test_trans_post_f_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_POST_F(["x", "+"]) # type: ignore