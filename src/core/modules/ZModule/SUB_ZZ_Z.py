# Литвиненко Владимир 5381

from core.base.Integer import Integer
from core.modules.NModule.ADD_NN_N import ADD_NN_N
from core.modules.NModule.COM_NN_D import COM_NN_D
from core.modules.NModule.SUB_NN_N import SUB_NN_N
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.ZModule.MUL_ZM_Z import MUL_ZM_Z
from core.modules.ZModule.POZ_Z_D import POZ_Z_D


def SUB_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Вычитание целых чисел.

    Args:
        a (Integer): Уменьшаемое.
        b (Integer): Вычитаемое.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Integer: Разность чисел.
    """
    if not isinstance(a, Integer) or not isinstance(b, Integer):
        raise ValueError("Invalid value")

    neg_b = MUL_ZM_Z(b)

    sign_a = POZ_Z_D(a)
    sign_neg_b = POZ_Z_D(neg_b)
    abs_a = ABS_Z_N(a)
    abs_neg_b = ABS_Z_N(neg_b)

    if sign_a == sign_neg_b:
        res_abs = ADD_NN_N(abs_a, abs_neg_b)
        res_sign = 0 if sign_a == 2 else 1
        return Integer(res_abs, res_sign)

    cmp = COM_NN_D(abs_a, abs_neg_b)

    if cmp == 0:
        return Integer.from_int(0)

    if cmp == 2:
        res_abs = SUB_NN_N(abs_a, abs_neg_b)
        return Integer(res_abs, 0 if sign_a == 2 else 1)

    res_abs = SUB_NN_N(abs_neg_b, abs_a)
    return Integer(res_abs, 0 if sign_neg_b == 2 else 1)
