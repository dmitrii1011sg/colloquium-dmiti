import pytest
from core.base.Rational import Rational
from core.modules.QModule.TRANS_Q_Z import TRANS_Q_Z


def test_trans_q_z_positive():
    r = Rational.from_str("42/1")
    result = TRANS_Q_Z(r)
    assert str(result) == "42"


def test_trans_q_z_negative():
    r = Rational.from_str("-7/1")
    result = TRANS_Q_Z(r)
    assert str(result) == "-7"


def test_trans_q_z_zero():
    r = Rational.from_str("0/1")
    result = TRANS_Q_Z(r)
    assert str(result) == "0"


def test_trans_q_z_invalid_denominator():
    r = Rational.from_str("3/2")
    with pytest.raises(ValueError):
        TRANS_Q_Z(r)


def test_trans_q_z_reducible():
    r = Rational.from_str("4/2")
    with pytest.raises(ValueError):
        TRANS_Q_Z(r)
