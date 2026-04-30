import pytest
from core.base.Integer import Integer
from core.base.Natural import Natural
from core.base.Rational import Rational


def test_rational_creation():
    numer = Integer.from_int(3)
    denom = Natural.from_int(4)
    r = Rational(numer, denom)
    assert str(r) == "3/4"

    numer_neg = Integer.from_int(-3)
    r_neg = Rational(numer_neg, denom)
    assert str(r_neg) == "-3/4"


def test_rational_zero_numerator():
    zero = Integer.from_int(0)
    denom = Natural.from_int(7)
    r = Rational(zero, denom)
    assert str(r) == "0/7"


def test_rational_denom_one():
    numer = Integer.from_int(5)
    denom = Natural.from_int(1)
    r = Rational(numer, denom)
    assert str(r) == "5"

    numer_neg = Integer.from_int(-5)
    r_neg = Rational(numer_neg, denom)
    assert str(r_neg) == "-5"


def test_rational_from_str():
    assert str(Rational.from_str("3/4")) == "3/4"
    assert str(Rational.from_str("-7/12")) == "-7/12"
    assert str(Rational.from_str("+5/2")) == "5/2"
    assert str(Rational.from_str("5")) == "5"
    assert str(Rational.from_str("-5")) == "-5"
    assert str(Rational.from_str("0/100")) == "0/100"


def test_rational_invalid_data():
    with pytest.raises(ValueError):
        Rational.from_str("3/0")
    with pytest.raises(ValueError):
        Rational.from_str("3/")
    with pytest.raises(ValueError):
        Rational.from_str("/4")
    with pytest.raises(ValueError):
        Rational.from_str("abc")
    with pytest.raises(ValueError):
        Rational.from_str("3/4/5")
    with pytest.raises(ValueError):
        Rational.from_str("")
    with pytest.raises(ValueError):
        Rational(Integer.from_int(1), Natural.from_int(0))


def test_rational_repr():
    r = Rational.from_str("3/4")
    assert repr(r) == "Rational(3/4)"


def test_rational_fields_types():
    r = Rational.from_str("-7/12")
    assert isinstance(r.numer, Integer)
    assert isinstance(r.denom, Natural)
    assert str(r.numer) == "-7"
    assert str(r.denom) == "12"


def test_rational_huge_numbers():
    big_str = "1" + "0" * 100
    r = Rational.from_str(f"{big_str}/{big_str}")
    assert str(r) == f"{big_str}/{big_str}"
