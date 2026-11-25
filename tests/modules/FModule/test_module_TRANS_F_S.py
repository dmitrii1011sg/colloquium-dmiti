# Помаскин Макар 5381

import pytest
from core.base.Formula import FormulaTree
from core.modules.FModule.TRANS_F_S import TRANS_F_S


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("x", "x"),
        ("x + 3 * y", "(x + (3 * y))"),
        ("log(2, -x)", "log(2, (-x))"),
    ],
)
def test_trans_f_s(expr, expected):
    tree = FormulaTree.from_str(expr)
    assert TRANS_F_S(tree) == expected


def test_trans_f_s_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_F_S("x")
