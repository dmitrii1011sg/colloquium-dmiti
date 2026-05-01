import pytest
from core.base.Rational import Rational
from core.base.Natural import Natural
from core.modules.QModule.INT_Q_B import INT_Q_B


def test_int_q_b_positive():
    r = Rational.from_str("4/1")
    result = INT_Q_B(r)
    assert result is True


def test_int_q_b_negative():
    r = Rational.from_str("-5/1")
    result = INT_Q_B(r)
    assert result is True


def test_int_q_b_zero():
    r = Rational.from_str("0/1")
    result = INT_Q_B(r)
    assert result is True


def test_int_q_b_simple():
    r = Rational.from_str("3/2")
    result = INT_Q_B(r)
    assert result is False


def test_int_q_b_large():
    r = Rational.from_str("1000000/1")
    result = INT_Q_B(r)
    assert result is True


def test_int_q_b_large_non():
    r = Rational.from_str("1234567/2")
    result = INT_Q_B(r)
    assert result is False


def test_int_q_b_denominator_minus_one():
    r = Rational.from_str("42/1")
    result = INT_Q_B(r)
    assert result is True


def test_int_q_b_invalid_input():
    with pytest.raises(ValueError):
        INT_Q_B("not a rational")

    with pytest.raises(ValueError):
        INT_Q_B(42)

    with pytest.raises(ValueError):
        INT_Q_B(None)


def test_int_q_b_unsimplified_throws():
    r = Rational.from_str("4/2")
    with pytest.raises(ValueError) as exc_info:
        INT_Q_B(r)
    assert str(exc_info.value) == "Invalid value"


def test_int_q_b_no_mutation_input():
    original = Rational.from_str("8/4")
    orig_str = str(original)
    _ = INT_Q_B(original)
    assert str(original) == orig_str
