# Литвиненко Владимир 5381

from core.base.FormulaNotation import PostfixFormula
from core.base.Formula import FormulaTree


def TRANS_POST_F(a: PostfixFormula) -> FormulaTree:
    """
    Построение дерева формулы по постфиксной записи.

    Args:
        a (PostfixFormula): Формула в постфиксной записи.

    Raises:
        ValueError: Параметр не соответствует типу или запись некорректна.

    Returns:
        FormulaTree: Синтаксическое дерево формулы.
    """
    if not isinstance(a, PostfixFormula):
        raise ValueError("Invalid value")

    return a.to_tree()
