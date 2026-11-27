from core.base.Formula import FormulaTree
from core.modules.FModule._infix import render_infix

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

    return render_infix(a.root, by_precedence=True)
