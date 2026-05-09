import pytest
from core.base.Natural import Natural
from core.modules.NModule.DIV_NN_Dk import DIV_NN_Dk


def test_div_nn_dk_simple():
    a = Natural.from_str("156")
    b = Natural.from_str("12")
    digit, k = DIV_NN_Dk(a, b)
    assert digit == 1
    assert k == 1


def test_div_nn_dk_less():
    a = Natural.from_str("45")
    b = Natural.from_str("100")
    digit, k = DIV_NN_Dk(a, b)
    assert digit == 0
    assert k == 0


def test_div_nn_dk_large_digit():
    a = Natural.from_str("950")
    b = Natural.from_str("10")
    digit, k = DIV_NN_Dk(a, b)
    assert digit == 9
    assert k == 1


def test_div_nn_dk_k_correction():
    a = Natural.from_str("1000")
    b = Natural.from_str("3")
    digit, k = DIV_NN_Dk(a, b)
    assert digit == 3
    assert k == 2


def test_div_nn_dk_equal():
    a = Natural.from_str("55")
    b = Natural.from_str("55")
    digit, k = DIV_NN_Dk(a, b)
    assert digit == 1
    assert k == 0


def test_div_nn_dk_zero_division():
    a = Natural.from_str("10")
    b = Natural.from_str("0")
    with pytest.raises(ValueError, match="Division by zero"):
        DIV_NN_Dk(a, b)
