from core.base.Formula import FormulaTree
from core.modules.FModule._infix import render_infix

# Жуков Александр 5381


def REM_ASSOC_F_S(a: FormulaTree) -> str:
    """
    Вывести формулу без скобок между соседними операциями умножения.

    Args:
        a (FormulaTree): Дерево формулы.

    Raises:
        ValueError: Параметр не соответствует типу FormulaTree.

    Returns:
        str: Скобочная запись формулы с раскрытыми цепочками множителей.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return render_infix(a.root, by_precedence=False)
