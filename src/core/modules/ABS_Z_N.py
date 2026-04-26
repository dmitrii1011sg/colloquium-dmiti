from core.base.Integer import Integer
from core.base.Natural import Natural

# Чугунников Валерий 5382


def ABS_Z_N(n : Integer) -> Natural:
    """
    Нахождение абсолютной величины числа

    Args:
         n (Integer): Целое число

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Natural : натуральное число, равное абсолютной величине n
    """

    if not isinstance(n, Integer):
        raise ValueError("Invalid value")

    return n.number