from core.base.Integer import Integer
from core.base.Rational import Rational
from core.modules.NModule.DIV_NN_N import DIV_NN_N
from core.modules.NModule.LCM_NN_N import LCM_NN_N
from core.modules.QModule.RED_Q_Q import RED_Q_Q
from core.modules.ZModule.ADD_ZZ_Z import ADD_ZZ_Z
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z

# Кацеба Андрей 5381


def ADD_QQ_Q(n: Rational, m: Rational) -> Rational:
    """
    Сложение двух дробей между собой

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

    n_num = n.numer
    n_dem = n.denom

    m_num = m.numer
    m_dem = m.denom

    new_dem = LCM_NN_N(n_dem, m_dem)

    mp_n = Integer(DIV_NN_N(new_dem, n_dem))
    mp_m = Integer(DIV_NN_N(new_dem, m_dem))
    new_num = ADD_ZZ_Z(MUL_ZZ_Z(n_num, mp_n), MUL_ZZ_Z(m_num, mp_m))

    result = Rational(new_num, new_dem)
    result = RED_Q_Q(result)
    return result
