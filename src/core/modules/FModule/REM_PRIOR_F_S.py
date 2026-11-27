from core.base.Formula import FormulaTree, needs_parentheses
from core.modules.FModule.TRANS_F_S import TRANS_F_S

# Жуков Александр 5381


def REM_PRIOR_F_S(a: FormulaTree) -> str:
    """
    Вывести формулу со скобками, необходимыми для сохранения порядка операций.

    Args:
        a (FormulaTree): Дерево формулы.

    Raises:
        ValueError: Параметр не соответствует типу FormulaTree.

    Returns:
        str: Запись формулы с учётом приоритета и ассоциативности операций.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return a.rewrite_parentheses(TRANS_F_S(a), needs_parentheses)
