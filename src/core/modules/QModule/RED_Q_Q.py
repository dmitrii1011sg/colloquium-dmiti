from core.base.Integer import Integer
from core.base.Rational import Rational
from core.modules.NModule.GCF_NN_N import GCF_NN_N
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
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

    numer = n.numer
    denom = n.denom
    if numer.is_zero():
        return Rational.from_str("0")

    abs_numer = ABS_Z_N(numer)
    GCD_num_denom = GCF_NN_N(abs_numer, denom)

    if GCD_num_denom.length == 1 and GCD_num_denom.digits[0] == 1:
        return n

    integer_GCD = Integer(GCD_num_denom)
    integer_denom = Integer(denom)

    res_numer = DIV_ZZ_Z(numer, integer_GCD)
    res_denom = DIV_ZZ_Z(integer_denom, integer_GCD)

    return Rational(res_numer, ABS_Z_N(res_denom))
