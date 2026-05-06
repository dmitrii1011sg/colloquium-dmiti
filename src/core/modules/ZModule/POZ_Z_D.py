from core.base.Integer import Integer

# Чугунников Валерий 5382


def POZ_Z_D(n: Integer) -> int:
    """
    Определение положительности числа

    Args:
         n (Integer): Целое число

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        int: 2 если число положительное, 1 - если отрицательное, 0 - если равное нулю
    """

    if not isinstance(n, Integer):
        raise ValueError("Invalid value")

    if n.is_zero():
        return 0

    return 1 if n.sign == 1 else 2
