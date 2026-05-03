from core.base.Rational import Rational
from core.modules.NModule.MUL_NN_N import MUL_NN_N
from core.modules.QModule.RED_Q_Q import RED_Q_Q
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z

# Кацеба Андрей 5381


def MUL_QQ_Q(n: Rational, m: Rational) -> Rational:
    """
    Перемножение двух дробей между собой

    Args:
         n (Rational): Рациональное число (обыкновенная дробь).
         m (Rational): Рациональное число (обыкновенная дробь).

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Rational : Рациональное число (обыкновенная дробь).
    """
    if not isinstance(n, Rational):
        raise ValueError("Invalid value")

    if not isinstance(m, Rational):
        raise ValueError("Invalid value")

    result = Rational(MUL_ZZ_Z(n.numer, m.numer), MUL_NN_N(n.denom, m.denom))
    result = RED_Q_Q(result)

    return result
