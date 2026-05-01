from core.base.Rational import Rational
from core.base.Natural import Natural

# Помаскин Макар 5381


def INT_Q_B(n: Rational) -> bool:
    """
    Проверка сокращенного дробного на целое

    Args:
         n (Rational): Рациональное число (обыкновенная дробь).

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        bool: True, если число целое; False, если нет.
    """
    if not isinstance(n, Rational):
        raise ValueError("Invalid value")

    return n.denom == Natural.from_int(1)
