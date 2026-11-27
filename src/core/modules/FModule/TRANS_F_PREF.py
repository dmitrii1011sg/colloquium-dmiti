# Литвиненко Владимир 5381

from core.base.Formula import FormulaTree
from core.base.FormulaNotation import PrefixFormula


def TRANS_F_PREF(a: FormulaTree) -> PrefixFormula:
    """
    Построение префиксной записи формулы по дереву.

    Args:
        a (FormulaTree): Дерево формулы.
    
    Raises:
        ValueError: Параметр не соответствует типу или запись некорректна.
    
    Returns:
        PrefixFormula: Формула префиксной записи.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return PrefixFormula.from_tree(a)