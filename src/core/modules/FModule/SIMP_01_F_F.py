from core.base.Formula import FormulaNode, FormulaTree, NodeType
from core.base.Rational import Rational

# Жуков Александр 5381

_ZERO = FormulaNode(NodeType.NUMBER, Rational.from_str("0"))
_ONE = FormulaNode(NodeType.NUMBER, Rational.from_str("1"))


def _simplify(node: FormulaNode) -> FormulaNode:
    """Упростить потомков перед проверкой нейтральных элементов в текущем узле."""
    children = [_simplify(child) for child in node.children]
    if node.node_type == NodeType.OPERATOR and node.value in ("+", "*"):
        left, right = children
        identity = _ZERO if node.value == "+" else _ONE
        if left == identity:
            return right
        if right == identity:
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
