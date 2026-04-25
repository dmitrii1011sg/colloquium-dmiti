from core.base.Natural import Natural
from core.modules.COM_NN_D import COM_NN_D
from core.modules.MOD_NN_N import MOD_NN_N
from core.modules.NZER_N_B import NZER_N_B

# Жулин Максим 5381


def GCF_NN_N(a: Natural, b: Natural) -> Natural:
    """
    Алгоритм нахождения НОД для натуральных чисел

    Args:
        a (Natural) - Первое натуральное число
        b (Natural) - Второе натуральное число

    Raises:
        ValueError: Параметры не соответствуют типам или одно из чисел равно нулю.

    Returns:
        Natural: Натуральное число, равное НОД(a, b).
    """
    if not (isinstance(a, Natural) and isinstance(b, Natural)):
        raise ValueError("Invalid value")

    if not (NZER_N_B(a) and NZER_N_B(b)):
        raise ValueError("Invalid value")

    # техдолг: разобраться с равенствами

    if COM_NN_D(a, b) == 0:
        return a

    if COM_NN_D(a, b) == 1:
        a, b = b, a

    n1, n2 = a, b

    while NZER_N_B(n2):
        n1, n2 = n2, MOD_NN_N(n1, n2)

    return n1
