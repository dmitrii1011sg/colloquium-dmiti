from core.base.Rational import Rational
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.NModule.GCF_NN_N import GCF_NN_N
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z

# Помаскин Макар 5381


def RED_Q_Q(n: Rational) -> Rational:
    """
    Получение несократимой обыкновенной дроби

    Args:
         n (Rational): Рациональное число (обыкновенная дробь).

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Rational : Рациональное числ.
    """
    if not isinstance(n, Rational):
        raise ValueError("Invalid value")

    num = n.number
    denom = n.denom

    abs_num = ABS_Z_N(num)
    GCD_num_denom = GCF_NN_N(abs_num, denom)

    future_num = DIV_ZZ_Z(num, GCD_num_denom)
    future_denom = DIV_ZZ_Z(denom, GCD_num_denom)
    future_n = Rational(future_num, future_denom)

    return future_n
