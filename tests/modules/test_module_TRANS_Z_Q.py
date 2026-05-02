import pytest
from core.base.Integer import Integer
from core.base.Rational import Rational
from core.modules.QModule.TRANS_Z_Q import TRANS_Z_Q


def test_trans_z_q_positive():
    n = Integer.from_str("42")
    result = TRANS_Z_Q(n)
    assert str(result) == "42"


def test_trans_z_q_negative():
    n = Integer.from_str("-7")
    result = TRANS_Z_Q(n)
    assert str(result) == "-7"


def test_trans_z_q_zero():
    n = Integer.from_str("0")
    result = TRANS_Z_Q(n)
    assert str(result) == "0"


def test_trans_z_q_large():
    n = Integer.from_str("123456789")
    result = TRANS_Z_Q(n)
    assert str(result) == "123456789"


def test_trans_z_q_invalid():
    with pytest.raises(ValueError):
        TRANS_Z_Q("not an integer")  # type: ignore

    with pytest.raises(ValueError):
        TRANS_Z_Q(None)  # type: ignore


def test_trans_z_q_return_type():
    n = Integer.from_str("10")
    result = TRANS_Z_Q(n)
    assert isinstance(result, Rational)
