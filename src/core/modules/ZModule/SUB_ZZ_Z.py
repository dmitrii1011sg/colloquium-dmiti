# Литвиненко Владимир 5381

from core.base.Integer import Integer
from core.base.Natural import Natural
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

    abs_a = ABS_Z_N(a)
    abs_b = ABS_Z_N(b)
    sign_a = POZ_Z_D(a)
    sign_b = POZ_Z_D(b)

    if sign_a == sign_b:
        cmp = COM_NN_D(abs_a, abs_b)

        if cmp == 2:
            result_num = SUB_NN_N(abs_a, abs_b)
            result_sign = 1 if sign_a == 1 else 0
            result = Integer(result_num, result_sign)
            return result
        elif cmp == 1:
            result_num = SUB_NN_N(abs_b, abs_a)
            if sign_a == 1:
                result = Integer(result_num, 0)
            else:
                result = MUL_ZM_Z(Integer(result_num, 0))
            return result
        else:
            return Integer(Natural.from_str("0"), 0)

    result_num = ADD_NN_N(abs_a, abs_b)
    if sign_a == 0 and sign_b != 0:
        result_sign = 1 if sign_b == 2 else 0
    else:
        result_sign = 1 if sign_a == 1 else 0
    result = Integer(result_num, result_sign)
    return result
