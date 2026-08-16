from abc import ABC
from dataclasses import dataclass


class ASTNode(ABC):
    pass


class UnaryOpType(ASTNode, ABC):
    pass


class BinaryOpType(ASTNode, ABC):
    pass


@dataclass(frozen=True)
class UAdd(UnaryOpType):
    pass


@dataclass(frozen=True)
class USub(UnaryOpType):
    pass


@dataclass(frozen=True)
class Add(BinaryOpType):
    pass


@dataclass(frozen=True)
class Sub(BinaryOpType):
    pass


@dataclass(frozen=True)
class Mul(BinaryOpType):
    pass


@dataclass(frozen=True)
class Div(BinaryOpType):
    pass


@dataclass(frozen=True)
class Pow(BinaryOpType):
    pass


@dataclass(frozen=True)
class Constant(ASTNode):
    value: int | float


@dataclass(frozen=True)
class UnaryOp(ASTNode):
    op: UnaryOpType
    operand: ASTNode


@dataclass(frozen=True)
class BinaryOp(ASTNode):
    op: BinaryOpType
    left: ASTNode
    right: ASTNode
