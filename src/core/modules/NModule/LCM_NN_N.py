from core.base.Natural import Natural
from core.modules.NModule.DIV_NN_N import DIV_NN_N
from core.modules.NModule.GCF_NN_N import GCF_NN_N
from core.modules.NModule.MUL_NN_N import MUL_NN_N
from core.modules.NModule.NZER_N_B import NZER_N_B

# Жулин Максим 5381


def LCM_NN_N(a: Natural, b: Natural):
    """
    Алгоритм нахождения НОК для натуральных чисел

    Args:
        a (Natural) - Первое натуральное число
        b (Natural) - Второе натуральное число

    Raises:
        ValueError: Параметры не соответствуют типам или среди чисел есть ноль.

    Returns:
        Natural: Натуральное число, равное НОК(a, b).
    """

    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid Value")

    if not (NZER_N_B(a) and NZER_N_B(b)):
        raise ValueError("Invalid value")

    return DIV_NN_N(MUL_NN_N(a, b), GCF_NN_N(a, b))
