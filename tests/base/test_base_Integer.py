import pytest
from core.base.Integer import Integer
from core.base.Natural import Natural


def test_integer_creation():
    n = Natural([1, 2], need_reverse=False)
    i = Integer(n, sign=0)
    assert i.sign == 0
    assert str(i) == "21"

    i_neg = Integer(n, sign=1)
    assert i_neg.sign == 1
    assert str(i_neg) == "-21"


def test_integer_zero_logic():
    zero_nat = Natural([0])
    i_zero = Integer(zero_nat, sign=1)
    assert i_zero.sign == 0
    assert str(i_zero) == "0"


def test_integer_from_str():
    assert str(Integer.from_str("123")) == "123"
    assert str(Integer.from_str("-50")) == "-50"
    assert str(Integer.from_str("+42")) == "42"
    assert Integer.from_str("-0").sign == 0


def test_integer_from_int():
    i = Integer.from_int(-100)
    assert i.sign == 1
    assert int(i) == -100

    i2 = Integer.from_int(5)
    assert i2.sign == 0
    assert int(i2) == 5


def test_integer_invalid_data():
    with pytest.raises(ValueError):
        Integer.from_str("12-3")
    with pytest.raises(ValueError):
        Integer.from_str("-")
    with pytest.raises(ValueError):
        Integer.from_str("abc")

    with pytest.raises(ValueError):
        Integer(Natural([1]), sign=2)


def test_integer_to_int_conversion():
    i = Integer.from_str("-123")
    assert int(i) == -123
    assert isinstance(int(i), int)
