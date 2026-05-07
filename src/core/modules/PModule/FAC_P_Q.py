from core.base.Natural import Natural
from core.base.Integer import Integer
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.NModule.LCM_NN_N import LCM_NN_N
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.ZModule.TRANS_Z_N import TRANS_Z_N
from core.modules.ZModule.TRANS_N_Z import TRANS_N_Z
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z
from core.modules.NModule.GCF_NN_N import GCF_NN_N
# Чугунников Валерий 5382

def FAC_P_Q(a:Polynom) -> Rational:
    """
    Вынесение из многочлена НОК знаменателей коэффицентов и НОД числителей

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Rational : Рациональное число, где числитель - НОД числителей, знаменатель - НОК знаменателей
    """

    if not isinstance(a, Polynom):
        raise ValueError("Invalid value")

    coefficients = a.coefficients
    numer = []
    denom = []
    for i in coefficients:
        if not i.is_zero():
            numer.append(i.numer)
            denom.append(i.denom)

    if not numer:
        return Rational(Integer.from_int(0), Natural.from_int(1))

    gcf_num = ABS_Z_N(numer[0])
    for i in numer[1:]:
        if not i.is_zero():
            new_num = ABS_Z_N(i)
            gcf_num = GCF_NN_N(gcf_num, new_num)

    lcm_den = denom[0]
    for i in denom[1:]:
        lcm_den = LCM_NN_N(lcm_den, i)

    gcf_num_as_int = TRANS_N_Z(gcf_num)
    return Rational(gcf_num_as_int, lcm_den)