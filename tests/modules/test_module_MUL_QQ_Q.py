import random
from fractions import Fraction

import pytest
from core.base.Rational import Rational
from core.modules.QModule.MUL_QQ_Q import MUL_QQ_Q


def test_mul_qq_q_both_positive():
    a = Rational.from_str("1/2")
    b = Rational.from_str("1/3")
    result = MUL_QQ_Q(a, b)
    assert str(result) == "1/6"


def test_mul_qq_q_both_negative():
    a = Rational.from_str("-1/2")
    b = Rational.from_str("-1/3")
    result = MUL_QQ_Q(a, b)
    assert str(result) == "1/6"


def test_mul_qq_q_positive_and_negative():
    a = Rational.from_str("3/4")
    b = Rational.from_str("-1/4")
    result = MUL_QQ_Q(a, b)
    assert str(result) == "-3/16"


def test_mul_qq_q_result_is_zero():
    a = Rational.from_str("5/7")
    b = Rational.from_str("0/1")
    result = MUL_QQ_Q(a, b)
    assert str(result) == "0"


def test_mul_qq_q_multiply_by_one():
    a = Rational.from_str("2/3")
    b = Rational.from_str("1/1")
    result = MUL_QQ_Q(a, b)
    assert str(result) == "2/3"


@pytest.mark.parametrize("iteration", range(10))
def test_mul_qq_q_random_with_negative(iteration):
    n1 = random.randint(-(10**30), 10**30)
    d1 = random.randint(1, 10**30)  # Знаменатель всегда > 0
    n2 = random.randint(-(10**30), 10**30)
    d2 = random.randint(1, 10**30)

    a = Rational.from_str(f"{n1}/{d1}")
    b = Rational.from_str(f"{n2}/{d2}")
    result = MUL_QQ_Q(a, b)

    expected = Fraction(n1, d1) * Fraction(n2, d2)
    assert str(result) == f"{expected.numerator}/{expected.denominator}"


def test_mul_qq_q_huge_numbers():
    base_num = "9" * 50
    base_den = "7" * 50
    a = Rational.from_str(f"{base_num}/{base_den}")
    b = Rational.from_str(f"{base_num}/{base_den}")
    expected = Fraction(int(base_num), int(base_den)) * Fraction(
        int(base_num), int(base_den)
    )
    result = MUL_QQ_Q(a, b)
    assert str(result) == f"{expected.numerator}/{expected.denominator}"


def test_mul_qq_q_huge_numbers_opposite_signs():
    big_num = "9" * 60
    small_num = "1" + "0" * 59
    common_den = "3" * 60

    a = Rational.from_str(f"{big_num}/{common_den}")
    b = Rational.from_str(f"-{small_num}/{common_den}")
    expected = Fraction(int(big_num), int(common_den)) * Fraction(
        -int(small_num), int(common_den)
    )
    result = MUL_QQ_Q(a, b)
    assert str(result) == f"{expected.numerator}/{expected.denominator}"


def test_mul_qq_q_no_mutation():
    a = Rational.from_str("-14/88")
    b = Rational.from_str("11/61")
    _ = MUL_QQ_Q(a, b)
    assert str(a) == "-14/88"
    assert str(b) == "11/61"


def test_mul_qq_q_invalid_input():
    with pytest.raises(ValueError):
        MUL_QQ_Q("not rational", Rational.from_str("1/2"))  # type: ignore

    with pytest.raises(ValueError):
        MUL_QQ_Q(Rational.from_str("1/2"), "not rational")  # type: ignore

    with pytest.raises(ValueError):
        MUL_QQ_Q(None, Rational.from_str("1/2"))  # type: ignore


def test_mul_qq_q_commutative():
    a = Rational.from_str("13/37")
    b = Rational.from_str("42/67")
    result1 = MUL_QQ_Q(a, b)
    result2 = MUL_QQ_Q(b, a)
    assert str(result1) == str(result2)


def test_mul_qq_q_associative():
    a = Rational.from_str("5/2")
    b = Rational.from_str("11/61")
    c = Rational.from_str("4/20")

    ab = MUL_QQ_Q(a, b)
    result1 = MUL_QQ_Q(ab, c)

    bc = MUL_QQ_Q(b, c)
    result2 = MUL_QQ_Q(a, bc)

    assert str(result1) == str(result2)


def test_mul_qq_q_edge_cases():
    max_r = Rational.from_str(f"{'9' * 50}/1")
    one_r = Rational.from_str("1/1")
    result = MUL_QQ_Q(max_r, one_r)
    assert str(result) == f"{'9' * 50}"

    zero_r = Rational.from_str("0/1")
    assert str(MUL_QQ_Q(zero_r, Rational.from_str("1/1"))) == "0"

    neg_r = Rational.from_str("-1/2")
    two_r = Rational.from_str("2/1")
    assert str(MUL_QQ_Q(neg_r, two_r)) == "-1"

    assert str(MUL_QQ_Q(Rational.from_str("-1/3"), Rational.from_str("3/1"))) == "-1"
