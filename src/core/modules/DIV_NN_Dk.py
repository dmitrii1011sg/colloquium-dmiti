# Дмитрий Лопатин 5381
from core.base.Natural import Natural
from core.modules.COM_NN_D import COM_NN_D
from core.modules.MUL_Nk_N import MUL_Nk_N
from core.modules.MUL_ND_N import MUL_ND_N
from core.modules.SUB_NN_N import SUB_NN_N


def DIV_NN_Dk(a: Natural, b: Natural, k: int) -> int:
    """
    Вычисление k-й цифры частного от деления большего натурального на меньшее.

    Args:
        a (Natural): Натуральное число (делимое).
        b (Natural): Натуральное число (делитель, b != 0).
        k (int): Номер цифры частного (0 - первая, 1 - вторая, ...).

    Raises:
        ValueError: Параметры не соответствуют типам или делитель равен нулю.

    Returns:
        int: k-я цифра частного (0-9).
    """    
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid Value")

    if b.length == 1 and b.digits[0] == 0:
        raise ValueError("Division by zero")

    if COM_NN_D(a, b) == 1: 
        dividend = b
        divisor = a
    else: 
        dividend = a
        divisor = b

    remainder = dividend
    max_shift = dividend.length - divisor.length

    for step in range(k + 1):
        shift = max_shift - step

        while shift > 0:
            b_shifted = MUL_Nk_N(divisor, Natural.from_int(shift))
            if COM_NN_D(remainder, b_shifted) != 1:
                break
            shift -= 1

        if shift < 0:
            return 0

        b_shifted = MUL_Nk_N(divisor, Natural.from_int(shift))

        digit = 0
        for d in range(9, 0, -1):
            b_mul = MUL_ND_N(b_shifted, Natural.from_int(d))
            if COM_NN_D(remainder, b_mul) != 1:
                digit = d
                break

        if step == k:
            return digit

        b_mul = MUL_ND_N(b_shifted, Natural.from_int(digit))
        remainder = SUB_NN_N(remainder, b_mul)

    return 0