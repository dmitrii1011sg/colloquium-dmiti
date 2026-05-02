from core.base.Rational import Rational
from core.base.Natural import Natural
from core.base.Integer import Integer
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.NModule.GCF_NN_N import GCF_NN_N
from core.modules.NModule.COM_NN_D import COM_NN_D
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z
from core.modules.ZModule.POZ_Z_D import POZ_Z_D

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

    numer = n.numer
    denom = n.denom
    if numer == Integer.from_int(0):
        return Rational.from_str("0")

    abs_numer = ABS_Z_N(numer)
    GCD_num_denom = GCF_NN_N(abs_numer, denom)
    if COM_NN_D(GCD_num_denom, Natural.from_int(1)) == 0:
        return n

    integer_GCD = Integer(GCD_num_denom)
    integer_denom = Integer(denom)
    if POZ_Z_D(numer) == 1:
        integer_numer = Integer(abs_numer, 1)
    else:
        integer_numer = Integer(numer, 0)

    res_numer = DIV_ZZ_Z(integer_numer, integer_GCD)
    res_denom = DIV_ZZ_Z(integer_denom, integer_GCD)

    res_n = Rational(res_numer, ABS_Z_N(res_denom))
    return res_n
