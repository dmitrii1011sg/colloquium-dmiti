from core.base.Integer import Integer
from core.modules.NModule.ADD_NN_N import ADD_NN_N
from core.modules.NModule.COM_NN_D import COM_NN_D
from core.modules.NModule.SUB_NN_N import SUB_NN_N
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.ZModule.MUL_ZM_Z import MUL_ZM_Z
from core.modules.ZModule.POZ_Z_D import POZ_Z_D

# Лопатин Дмитрий 5381


def ADD_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Абсолютная величина числа, результат - натуральное

    Args:
        a (Integer): Целое число
        b (Integer): Целое число
    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Integer: Целое число, равное a + b
    """

    if not isinstance(a, Integer) or not isinstance(b, Integer):
        raise ValueError("Invalid Value")

    sign_a = POZ_Z_D(a)
    sign_b = POZ_Z_D(b)
    N_a = ABS_Z_N(a)
    N_b = ABS_Z_N(b)

    if sign_a == sign_b:
        res = ADD_NN_N(N_a, N_b)
        res = Integer(res, sign=0)
        res = MUL_ZM_Z(res) if sign_a == 1 else res
        return res

    com = COM_NN_D(N_a, N_b)

    if com == 0:
        return Integer.from_int(0)

    if com == 2:
        res = SUB_NN_N(N_a, N_b)
        return Integer(res, sign=a.sign)

    res = SUB_NN_N(N_b, N_a)
    return Integer(res, sign=b.sign)
