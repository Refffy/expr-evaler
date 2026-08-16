from .ast import (
    ASTNode,
    Constant,
    UnaryOp, UAdd, USub,
    BinaryOp, Add, Sub, Mul, Div, Pow
)


def evaluate(node: ASTNode) -> int | float:
    match node:
        case Constant(value):
            return value
        case UnaryOp(UAdd(), operand):
            return evaluate(operand)
        case UnaryOp(USub(), operand):
            return -evaluate(operand)
        case BinaryOp(Add(), left, right):
            return evaluate(left) + evaluate(right)
        case BinaryOp(Sub(), left, right):
            return evaluate(left) - evaluate(right)
        case BinaryOp(Mul(), left, right):
            return evaluate(left) * evaluate(right)
        case BinaryOp(Div(), left, right):
            return evaluate(left) / evaluate(right)
        case BinaryOp(Pow(), left, right):
            return evaluate(left) ** evaluate(right)
        case _:
            raise ValueError(f"Unknown AST node: {node}")