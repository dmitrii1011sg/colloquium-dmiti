from core.base.Formula import FormulaTree
from core.base.FormulaNotation import PostfixFormula

# Помаскин Макар 5381


def TRANS_F_POST(a: FormulaTree) -> PostfixFormula:
    """
    Построение постфиксной записи формулы по дереву.

    Args:
        a (FormulaTree): Дерево формулы.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        PostfixFormula: Формула в постфиксной записи.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return PostfixFormula.from_tree(a)
