from core.base.Natural import Natural
from core.modules.NModule.COM_NN_D import COM_NN_D
from core.modules.NModule.MUL_ND_N import MUL_ND_N
from core.modules.NModule.SUB_NN_N import SUB_NN_N


# Жулин Максим 5381

def SUB_NDN_N(a: Natural, b: Natural, d: int):
    """
    Вычитание из одного натурального числа другого натурального числа,
    умноженного на цифру для случая с неотрицательным результатом.

    Первое число должно быть больше или равно второму числу, умноженному
    на цифру.

    Args:
        a (Natural): Уменьшаемое
        b (Natural): Неполное вычитаемое
        d (int): Цифра, на которую умножаем

    Raises:
        ValueError: Параметры не соответствуют типам или a < b * d

    Returns:
        Natural: Неотрицательное число, равное a - (b * d)
    """
    if not (
        isinstance(a, Natural) and isinstance(b, Natural) and isinstance(d, int)
    ):
        raise ValueError("Invalid Value")

    if d < 0 or d > 9:
        raise ValueError("Invalid Value")

    composition = MUL_ND_N(b, d)

    if COM_NN_D(a, composition) == 1:
        raise ValueError("Invalid Value")

    return SUB_NN_N(a, composition)
