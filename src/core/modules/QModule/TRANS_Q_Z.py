from core.base.Rational import Rational
from core.base.Natural import Natural
from core.base.Integer import Integer

# Помаскин Макар 5381


def TRANS_Q_Z(n: Rational) -> Integer:
    """
    Преобразование сокращенного дробного в целое

    Args:
         n (Rational): Рациональное число (обыкновенная дробь).

    Raises:
        ValueError: Параметр не соответствует типу или знаменатель неравен 1.

    Returns:
        Integer: Целое число.
    """
    if not isinstance(n, Integer):
        raise ValueError("Invalid value")
    if n.denom != Natural.from_int(1)(1):
        raise ValueError("Invalid value")

    return n.numer
