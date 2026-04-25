from core.base.Natural import Natural
from core.modules.ADD_NN_N import ADD_NN_N
from core.modules.MUL_ND_N import MUL_ND_N
from core.modules.MUL_Nk_N import MUL_Nk_N

# Дмитрий Лопатин 5381


def MUL_NN_N(a: Natural, b: Natural) -> Natural:
    """
    Умножение двух натуральных чисел.

    Args:
        a (Natural): Первый множитель.
        b (Natural): Второй множитель.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Natural: Произведение a * b.
    """
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid Value")

    if (a.digits[0] == 0 and a.length == 1) or (b.digits[0] == 0 and b.length == 1):
        return Natural([0])

    res = Natural([0])

    for i, digit in enumerate(b.digits):
        if digit == 0:
            continue
        natural_digit = Natural.from_int(digit)
        tmp = MUL_Nk_N(MUL_ND_N(a, natural_digit), Natural.from_int(i))
        res = ADD_NN_N(res, tmp)

    return res
