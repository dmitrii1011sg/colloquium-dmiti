from core.base.Integer import Integer
from core.base.Rational import Rational

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
    if n.denom.digits[0] != 1 or n.denom.length != 1:
        raise ValueError("Invalid value")

    return n.numer
