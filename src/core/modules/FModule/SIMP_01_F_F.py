from core.base.Formula import FormulaNode, FormulaTree

# Жуков Александр 5381


def _simplify(node: FormulaNode) -> FormulaNode:
    """Упростить потомков перед проверкой нейтральных элементов в текущем узле."""
    children = [_simplify(child) for child in node.children]
    if node.is_op and node.value in ("+", "*"):
        left, right = children
        is_neutral = FormulaNode.is_zero if node.value == "+" else FormulaNode.is_one
        if is_neutral(left):
            return right
        if is_neutral(right):
            return left

    return FormulaNode(node.node_type, node.value, children)


def SIMP_01_F_F(a: FormulaTree) -> FormulaTree:
    """
    Убрать числовые нули из сложения и единицы из умножения на любой глубине.

    Args:
        a (FormulaTree): Дерево формулы.

    Raises:
        ValueError: Параметр не соответствует типу FormulaTree.

    Returns:
        FormulaTree: Новое дерево с упрощёнными подвыражениями.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return FormulaTree(_simplify(a.root))
