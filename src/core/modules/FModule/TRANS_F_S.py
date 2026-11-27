from core.base.Formula import FormulaTree

# Помаскин Макар 5381


def TRANS_F_S(a: FormulaTree) -> str:
    """
    Построение полной скобочной записи формулы по дереву.

    Args:
        a (FormulaTree): Дерево формулы.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        str: Полная скобочная запись формулы.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return str(a)
