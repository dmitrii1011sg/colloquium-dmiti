from core.base.Natural import Natural

# Лопатин Дмитрий 5381

def MUL_ND_N(a: Natural, d: int) -> Natural:
    """
    Умножение натурального числа на цифру.

    Args:
         a (Natural): Натуральное число.
         d (int): Цифра, на которую умножаем.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        если a == 0 || d == 0; 0, иначе a * d
    """

    if not isinstance(a, Natural) or not isinstance(d, int):
        raise ValueError("Invalid value")

    if d < 0 or d > 9:
        raise ValueError("Invalid value")

    carry = 0
    res = []

    if d == 0:
        return Natural([0])
    if a.length == 1 and a.digits[0] == 0:
        return Natural([0])

    for digit in a.digits:
        total = digit * d + carry
        res.append(total % 10)
        carry = total // 10
    if carry > 0:
        res.append(carry)

    return Natural(res, need_reverse=False)
