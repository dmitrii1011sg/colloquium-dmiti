from core.base.Natural import Natural
from core.modules.COM_NN_D import COM_NN_D
from core.modules.MUL_ND_N import MUL_ND_N
from core.modules.MUL_Nk_N import MUL_Nk_N

# Дмитрий Лопатин 5381


def DIV_NN_Dk(a: Natural, b: Natural) -> tuple[int, int]:
    """
    Вычисление k-й цифры частного от деления большего натурального на меньшее.

    Args:
        a (Natural): Натуральное число (делимое).
        b (Natural): Натуральное число (делитель, b != 0).

    Raises:
        ValueError: Параметры не соответствуют типам или делитель равен нулю.

    Returns:
        tuple[int, int]: Кортеж (цифра 1-9, степень k).
                         Если a < b, возвращается (0, 0).
    """
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid Value")

    if b.length == 1 and b.digits[0] == 0:
        raise ValueError("Division by zero")

    if COM_NN_D(a, b) == 1:
        return (0, 0)

    k = a.length - b.length
    b_shifted = MUL_Nk_N(b, Natural.from_int(k))
    if COM_NN_D(a, b_shifted) == 1:
        k -= 1
        b_shifted = MUL_Nk_N(b, Natural.from_int(k))

    for digit in range(9, 0, -1):
        digit_nat = Natural([digit], need_reverse=False)

        b_mul = MUL_ND_N(b_shifted, digit_nat)

        if COM_NN_D(a, b_mul) != 1:
            return (digit, k)

    return (0, 0)
