from core.base.Rational import Rational
from core.base.Natural import Natural
from core.base.Integer import Integer

# Помаскин Макар 5381


def TRANS_Z_Q(n: Integer) -> Rational:
    """
    Преобразование целого в дробное

    Args:
         n (Integer): Целое число.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Rational: Рациональное число (обыкновенная дробь).
    """
    if not isinstance(n, Integer):
        raise ValueError("Invalid value")

    return Rational(n, Natural(1))
