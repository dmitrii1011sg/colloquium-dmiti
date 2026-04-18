from core.base.Natural import Natural


def COM_NN_D(a: Natural, b: Natural) -> int:
    """
    Сравнение двух натуральных чисел.

    Args:
        a (Natural): Первое число.
        b (Natural): Второе число.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        int: 2, если a > b; 1, если a < b; 0, если равны.
    """
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid value")

    if a.length > b.length:
        return 2
    if a.length < b.length:
        return 1

    for i in range(a.length - 1, -1, -1):
        if a.digits[i] > b.digits[i]:
            return 2
        if a.digits[i] < b.digits[i]:
            return 1

    return 0
