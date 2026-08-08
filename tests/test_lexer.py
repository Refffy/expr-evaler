import pytest

from expr_evaler.lexer import Lexer, TokenType
from expr_evaler.exceptions import UnexpectedNumberError, UnknownLexemeError


def get_simplified_tokens(expr: str):
    lexer = Lexer(expr)
    return [(token.type, token.lexeme) for token in lexer.produce()]


def test_basic_arithmetic():
    tokens = get_simplified_tokens("2 + 3 * ( 4 - 1 )")
    assert tokens == [
        (TokenType.NUMBER, "2"), (TokenType.ADD_OP, "+"), (TokenType.NUMBER, "3"),
        (TokenType.MUL_OP, "*"), (TokenType.LPAREN, "("), (TokenType.NUMBER, "4"),
        (TokenType.SUB_OP, "-"), (TokenType.NUMBER, "1"), (TokenType.RPAREN, ")"),
        (TokenType.EOF, None)
    ]

def test_edge_case_fractions():
    assert get_simplified_tokens(".5") == [(TokenType.NUMBER, "0.5"), (TokenType.EOF, None)]
    assert get_simplified_tokens("42.") == [(TokenType.NUMBER, "42.0"), (TokenType.EOF, None)]

def test_ignore_whitespace():
    assert get_simplified_tokens(" \n  \t \r \n  ") == [(TokenType.EOF, None)]

def test_multiple_dots_raises_error():
    with pytest.raises(UnexpectedNumberError, match="Unexpected number"):
        Lexer("2.5.3").produce()

def test_unknown_token_raises_error():
    with pytest.raises(UnknownLexemeError, match="No such token type exist"):
        Lexer("2 + $").produce()
