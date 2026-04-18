# Дмитрий Лопатин 5381

from core.base.Natural import Natural

def MUL_Nk_N(a: Natural, k: Natural) -> Natural:
    """
    Умножение натурального числа на 10^k.

    Args:
        a (Natural): Натуральное число (множимое).
        k (Natural): Натуральное число (показатель степени для 10^k).

    Returns:
        Natural: Результат умножения a * 10^k.
            - Если a = 0, возвращает 0.
            - Если k = 0, возвращает a (так как 10^0 = 1).
            - Иначе возвращает a с добавленными k нулями в конце.

    Raises:
        ValueError: Если один из аргументов не является экземпляром класса Natural.
    """
    if not isinstance(a, Natural) or not isinstance(k, Natural):
        raise ValueError("Invalid Value")

    res = []
    zeros = int(str(k))

    if (a.length == 1 and a.digits[0] == 0) or zeros == 0:
        res = a.digits.copy()
        return Natural(res, need_reverse=False)
    else:
        res = [0] * zeros + a.digits.copy()

    return Natural(res, need_reverse=False)