from core.base.Formula import FormulaTree, PostfixFormula

# Помаскин Макар 5381


def TRANS_F_POST(a: FormulaTree) -> str:
    """
    Построение постфиксной записи формулы по дереву.

    Args:
        a (FormulaTree): Дерево формулы.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        str: Постфиксная запись формулы с пробелами между элементами.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return str(PostfixFormula.from_tree(a))
