import pytest

from expr_evaler import Lexer, RecursiveDescentParser
from expr_evaler.parsers.ast import (
    ASTNode,
    Constant,
    BinaryOp, Add, Sub,Mul, Div,
    UnaryOp, UAdd, USub,
)


def parse(expr: str) -> ASTNode:
    tokens = Lexer(expr).tokenize()
    return RecursiveDescentParser(tokens).parse()


@pytest.mark.parametrize(
    ("expression", "expected_ast"),
    [
        ("42", Constant(value=42)),
        ("3.14", Constant(value=3.14)),
    ],
)
def test_constants(expression: str, expected_ast: ASTNode):
    assert parse(expression) == expected_ast


@pytest.mark.parametrize(
    ("expression", "expected_ast"),
    [
        ("-5", UnaryOp(op=USub(), operand=Constant(value=5))),
        ("+5", UnaryOp(op=UAdd(), operand=Constant(value=5))),
        ("--5", UnaryOp(op=USub(), operand=UnaryOp(op=USub(), operand=Constant(value=5)))),
    ],
)
def test_unary_operations(expression: str, expected_ast: ASTNode):
    assert parse(expression) == expected_ast


@pytest.mark.parametrize(
    ("expression", "expected_ast"),
    [
        ("1 + 2", BinaryOp(op=Add(), left=Constant(value=1), right=Constant(value=2))),
        ("10 - 5", BinaryOp(op=Sub(), left=Constant(value=10), right=Constant(value=5))),
        ("3 * 4", BinaryOp(op=Mul(), left=Constant(value=3), right=Constant(value=4))),
        ("8 / 2", BinaryOp(op=Div(), left=Constant(value=8), right=Constant(value=2))),
    ],
)
def test_binary_operations(expression: str, expected_ast: ASTNode):
    assert parse(expression) == expected_ast


@pytest.mark.parametrize(
    ("expression", "expected_ast"),
    [
        (
            "1 + 2 * 3",
            BinaryOp(
                op=Add(),
                left=Constant(value=1),
                right=BinaryOp(op=Mul(), left=Constant(value=2), right=Constant(value=3)),
            ),
        ),
        (
            "1 * 2 + 3",
            BinaryOp(
                op=Add(),
                left=BinaryOp(op=Mul(), left=Constant(value=1), right=Constant(value=2)),
                right=Constant(value=3),
            ),
        ),
        (
            "1 - 2 - 3",
            BinaryOp(
                op=Sub(),
                left=BinaryOp(op=Sub(), left=Constant(value=1), right=Constant(value=2)),
                right=Constant(value=3),
            ),
        ),
        (
            "8 / 4 / 2",
            BinaryOp(
                op=Div(),
                left=BinaryOp(op=Div(), left=Constant(value=8), right=Constant(value=4)),
                right=Constant(value=2),
            ),
        ),
    ],
)
def test_precedence_and_associativity(expression: str, expected_ast: ASTNode):
    assert parse(expression) == expected_ast


@pytest.mark.parametrize(
    ("expression", "expected_ast"),
    [
        (
            "(1 + 2) * 3",
            BinaryOp(
                op=Mul(),
                left=BinaryOp(op=Add(), left=Constant(value=1), right=Constant(value=2)),
                right=Constant(value=3),
            ),
        ),
        ("((1 + 2))", BinaryOp(op=Add(), left=Constant(value=1), right=Constant(value=2))),
    ],
)
def test_parentheses(expression: str, expected_ast: ASTNode):
    assert parse(expression) == expected_ast


@pytest.mark.parametrize(
    ("expression", "error_match"),
    [
        ("(1 + 2", "Closing parenthesis expected"),
        ("1 +", "Unexpected token type: TokenType.EOF"),
        ("1 + * 2", "Unexpected token type: TokenType.MUL_OP"),
        ("", "Unexpected token type: TokenType.EOF"),
    ],
)
def test_parser_syntax_errors(expression: str, error_match: str):
    with pytest.raises(SyntaxError, match=error_match):
        parse(expression)
