# Помаскин Макар 5381

import pytest
from core.base.Formula import FormulaTree
from core.modules.FModule.TRANS_F_POST import TRANS_F_POST


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("42", "42"),
        ("a - b * c", "a b c * -"),
        ("log(2, -x)", "2 x u- log"),
    ],
)
def test_trans_f_post(expr, expected):
    tree = FormulaTree.from_str(expr)
    assert TRANS_F_POST(tree) == expected


def test_trans_f_post_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_F_POST("x")
