from core.base.Rational import Rational
from core.modules.QModule.RED_Q_Q import RED_Q_Q
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z
from core.modules.ZModule.TRANS_N_Z import TRANS_N_Z

# Кацеба Андрей 5381


def DIV_QQ_Q(n: Rational, m: Rational) -> Rational:
    """
    Деление одной дроби на другую

    Args:
         n (Rational): Рациональное число (обыкновенная дробь).
         m (Rational): Рациональное число (обыкновенная дробь).

    Raises:
        ValueError: Параметр не соответствует типу.
        ZeroDivisionError: делитель равен нулю.

    Returns:
        Rational : Рациональное число (обыкновенная дробь).
    """
    if not isinstance(n, Rational):
        raise ValueError("Invalid value")

    if not isinstance(m, Rational):
        raise ValueError("Invalid value")

    n_num = n.numer
    n_dem = n.denom

    m_num = m.numer
    m_dem = m.denom

    if m_num.number.digits[0] == 0 and m_num.number.length == 1:
        raise ZeroDivisionError("invalid value")

    new_num = MUL_ZZ_Z(n_num, TRANS_N_Z(m_dem))
    new_dem = MUL_ZZ_Z(TRANS_N_Z(n_dem), m_num)

    if new_dem.sign == 1:
        new_num.sign = 1 if new_num.sign == 0 else 0

    new_dem = new_dem.number

    result = Rational(new_num, new_dem)
    result = RED_Q_Q(result)

    return result
