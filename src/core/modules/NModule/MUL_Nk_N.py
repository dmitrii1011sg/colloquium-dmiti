from core.base.Natural import Natural

# Лопатин Дмитрий 5381


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

    zeros = int(k)

    if a.is_zero() or zeros == 0:
        return Natural(a.digits.copy(), need_reverse=False)

    return Natural([0] * zeros + a.digits.copy(), need_reverse=False)
