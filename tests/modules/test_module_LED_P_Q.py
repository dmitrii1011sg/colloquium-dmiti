import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.LED_P_Q import LED_P_Q


def test_led_p_q_simple():
    p = Polynom(
        [Rational.from_str("3"), Rational.from_str("0"), Rational.from_str("5")]
    )
    result = LED_P_Q(p)
    assert str(result) == "5"


def test_led_p_q_negative():
    p = Polynom(
        [Rational.from_str("1/2"), Rational.from_str("-7/1"), Rational.from_str("0")]
    )
    result = LED_P_Q(p)
    assert str(result) == "-7"


def test_led_p_q_constant():
    p = Polynom([Rational.from_str("42/1")])
    result = LED_P_Q(p)
    assert str(result) == "42"


def test_led_p_q_linear():
    p = Polynom([Rational.from_str("-3/4"), Rational.from_str("2/1")])
    result = LED_P_Q(p)
    assert str(result) == "2"


def test_led_p_q_high_degree():
    p = Polynom(
        [Rational.from_str("1/1")]
        + [Rational.from_str("0")] * 9
        + [Rational.from_str("5/2")]
    )
    result = LED_P_Q(p)
    assert str(result) == "5/2"


def test_led_p_q_fraction():
    p = Polynom([Rational.from_str("1/3"), Rational.from_str("5/7")])
    result = LED_P_Q(p)
    assert str(result) == "5/7"


def test_led_p_q_invalid_input():
    with pytest.raises(ValueError):
        LED_P_Q("not a polynom")  # type: ignore

    with pytest.raises(ValueError):
        LED_P_Q(123)  # type: ignore

    with pytest.raises(ValueError):
        LED_P_Q(None)  # type: ignore
