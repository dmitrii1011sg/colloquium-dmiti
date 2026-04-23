import random
import pytest
from core.base.Natural import Natural
from core.modules.DIV_NN_Dk import DIV_NN_Dk


def test_DIV_NN_Dk():
    # Базовые тесты
    n1 = Natural.from_str("4567")
    n2 = Natural.from_str("12")
    assert DIV_NN_Dk(n1, n2, 0) == 3
    assert DIV_NN_Dk(n1, n2, 1) == 8
    assert DIV_NN_Dk(n1, n2, 2) == 0
    
    # Равные числа
    n3 = Natural.from_str("100")
    n4 = Natural.from_str("100")
    assert DIV_NN_Dk(n3, n4, 0) == 1
    assert DIV_NN_Dk(n3, n4, 1) == 0
    
    # Деление на 1
    n5 = Natural.from_str("12345")
    n6 = Natural.from_str("1")
    assert DIV_NN_Dk(n5, n6, 0) == 1
    assert DIV_NN_Dk(n5, n6, 1) == 2
    assert DIV_NN_Dk(n5, n6, 2) == 3
    
    # Число меньше делителя
    n7 = Natural.from_str("10")
    n8 = Natural.from_str("100")
    assert DIV_NN_Dk(n7, n8, 0) == 1


@pytest.mark.parametrize("iteration", range(5))
def test_DIV_NN_Dk_random(iteration):
    val1 = random.randint(1, 10**50)
    val2 = random.randint(1, 10**50)
    
    if val1 < val2:
        val1, val2 = val2, val1
    
    n1 = Natural.from_int(val1)
    n2 = Natural.from_int(val2)
    
    quotient = val1 // val2
    quotient_str = str(quotient)
    
    for k in range(min(5, len(quotient_str))):
        expected = int(quotient_str[k])
        assert DIV_NN_Dk(n1, n2, k) == expected


def test_DIV_NN_Dk_huge_numbers():
    # 999...9 / 1 = 999...9
    size = 1000
    base_str = "9" * size
    n1 = Natural.from_str(base_str)
    n2 = Natural.from_str("1")
    
    assert DIV_NN_Dk(n1, n2, 0) == 9
    assert DIV_NN_Dk(n1, n2, size - 1) == 9
    assert DIV_NN_Dk(n1, n2, size) == 0


def test_DIV_NN_Dk_zero_division():
    n1 = Natural.from_str("100")
    n2 = Natural.from_str("0")
    
    with pytest.raises(ValueError):
        DIV_NN_Dk(n1, n2, 0)


def test_DIV_NN_Dk_edge_cases():
    # 1000000 / 1 = 1000000
    n1 = Natural.from_str("1" + "0" * 6)
    n2 = Natural.from_str("1")
    assert DIV_NN_Dk(n1, n2, 0) == 1
    assert DIV_NN_Dk(n1, n2, 1) == 0
    assert DIV_NN_Dk(n1, n2, 6) == 0
    
    # 100 / 33 = 3 (остаток 1)
    n3 = Natural.from_str("100")
    n4 = Natural.from_str("33")
    assert DIV_NN_Dk(n3, n4, 0) == 3
    assert DIV_NN_Dk(n3, n4, 1) == 0


def test_DIV_NN_Dk_no_mutation():
    n1 = Natural.from_str("4567")
    n2 = Natural.from_str("12")
    orig1_digits = list(n1.digits)
    orig2_digits = list(n2.digits)
    orig1_length = n1.length
    orig2_length = n2.length
    
    _ = DIV_NN_Dk(n1, n2, 1)
    
    assert n1.digits == orig1_digits
    assert n2.digits == orig2_digits
    assert n1.length == orig1_length
    assert n2.length == orig2_length