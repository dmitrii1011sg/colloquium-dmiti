import random
from math import gcd

import pytest
from core.base.Rational import Rational
from core.modules.QModule.RED_Q_Q import RED_Q_Q


def test_red_q_q_reduced():
    r = Rational.from_str("3/7")
    result = RED_Q_Q(r)
    assert str(result) == "3/7"


def test_red_q_q_simple():
    r = Rational.from_str("4/8")
    result = RED_Q_Q(r)
    assert str(result) == "1/2"


def test_red_q_q_with_common_divisor():
    r = Rational.from_str("12/18")
    result = RED_Q_Q(r)
    assert str(result) == "2/3"


def test_red_q_q_negative_numerator():
    r = Rational.from_str("-4/6")
    result = RED_Q_Q(r)
    assert str(result) == "-2/3"


def test_red_q_q_numerator_zero():
    r = Rational.from_str("0/5")
    result = RED_Q_Q(r)
    assert str(result) == "0"


def test_red_q_q_denominator_one():
    r = Rational.from_str("7/1")
    result = RED_Q_Q(r)
    assert str(result) == "7"


def test_red_q_q_large_numbers():
    r = Rational.from_str("12345678/24681357")
    result = RED_Q_Q(r)
    assert str(result) == "1371742/2742373"


def test_red_q_q_gcd_equals_numerator():
    r = Rational.from_str("10/5")
    result = RED_Q_Q(r)
    assert str(result) == "2"


def test_red_q_q_no_mutation_input():
    original = Rational.from_str("8/12")
    orig_str = str(original)
    _ = RED_Q_Q(original)
    assert str(original) == orig_str
    assert original.numer.sign == 0
    assert int(original.numer.number) == 8
    assert int(original.denom) == 12


@pytest.mark.parametrize(
    "numerator,denominator,expected",
    [
        ("2", "4", "1/2"),
        ("6", "9", "2/3"),
        ("15", "25", "3/5"),
        ("100", "250", "2/5"),
        ("81", "27", "3"),
        ("-8", "12", "-2/3"),
        ("-9", "3", "-3"),
        ("0", "100", "0"),
        ("30", "42", "5/7"),
        ("18", "30", "3/5"),
    ],
)
def test_red_q_q_parametrized(numerator, denominator, expected):
    r = Rational.from_str(f"{numerator}/{denominator}")
    result = RED_Q_Q(r)
    assert str(result) == expected


@pytest.mark.parametrize("iteration", range(20))
def test_red_q_q_random(iteration):
    num = random.randint(1, 10**6)
    den = random.randint(1, 10**6)

    if random.choice([True, False]):
        num = -num

    r = Rational.from_str(f"{num}/{den}")
    result = RED_Q_Q(r)

    g = gcd(abs(num), den)
    expected_num = num // g
    expected_den = den // g

    if expected_den == 1:
        expected = str(expected_num)
    else:
        expected = f"{expected_num}/{expected_den}"

    assert str(result) == expected


def test_red_q_q_identity():
    r = Rational.from_str("100/250")
    first = RED_Q_Q(r)
    second = RED_Q_Q(first)
    assert str(first) == str(second) == "2/5"


def test_red_q_q_invalid_input():
    with pytest.raises(ValueError):
        RED_Q_Q("not a rational")  # type: ignore

    with pytest.raises(ValueError):
        RED_Q_Q(42)  # type: ignore

    with pytest.raises(ValueError):
        RED_Q_Q(None)  # type: ignore


def test_red_q_q_preserves_sign():
    test_cases = [
        ("5/10", "1/2"),
        ("-5/10", "-1/2"),
        ("5/-10", None),
        ("-5/-10", None),
    ]

    for num_str, expected in test_cases:
        if expected is None:
            continue
        r = Rational.from_str(num_str)
        result = RED_Q_Q(r)
        assert str(result) == expected
