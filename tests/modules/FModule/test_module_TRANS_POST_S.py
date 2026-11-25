# Помаскин Макар 5381

import pytest
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
    assert TRANS_POST_S(postfix) == expected


@pytest.mark.parametrize("postfix", ["", "x +", "x y"])
def test_trans_post_s_invalid_notation(postfix):
    with pytest.raises(ValueError):
        TRANS_POST_S(postfix)


def test_trans_post_s_invalid_input():
    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_POST_S(None)
