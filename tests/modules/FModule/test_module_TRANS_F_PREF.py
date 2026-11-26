# Литвиненко Владимир 5381

import pytest
from core.base.Formula import FormulaTree
from core.base.FormulaNotation import PrefixFormula
from core.modules.FModule.TRANS_F_PREF import TRANS_F_PREF


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("7", "7"),
        ("x * y + z", "+ * x y z"),
        ("sin(x) + cos(y)", "+ sin x cos y"),
        ("x^2 + 1", "+ ^ x 2 1"),
        ("log(x, y) * 3", "* log x y 3"),
    ],
)
def test_trans_f_pref(expr, expected):
    tree = FormulaTree.from_str(expr)
    result = TRANS_F_PREF(tree)
    assert isinstance(result, PrefixFormula)
    assert str(result) == expected


def test_trans_f_pref_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_F_PREF(123) # type: ignore