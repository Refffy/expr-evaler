import pytest

from expr_evaler import Lexer, TokenType
from expr_evaler.exceptions import UnexpectedNumberError, UnknownLexemeError


def get_simplified_tokens(
    expr: str,
) -> list[tuple[TokenType, str | None]]:
    return [(token.type, token.lexeme) for token in Lexer(expr).produce()]


def test_basic_arithmetic():
    assert get_simplified_tokens("2 + 3 * (4 - 1)") == [
        (TokenType.NUMBER, "2"),
        (TokenType.ADD_OP, "+"),
        (TokenType.NUMBER, "3"),
        (TokenType.MUL_OP, "*"),
        (TokenType.LPAREN, "("),
        (TokenType.NUMBER, "4"),
        (TokenType.SUB_OP, "-"),
        (TokenType.NUMBER, "1"),
        (TokenType.RPAREN, ")"),
        (TokenType.EOF, None),
    ]


@pytest.mark.parametrize(
    ("expression", "expected_lexeme"),
    [
        ("0", "0"),
        ("42", "42"),
        ("0.5", "0.5"),
        (".5", "0.5"),
        ("0.", "0.0"),
        ("42.", "42.0"),
    ],
)
def test_numbers(expression: str, expected_lexeme: str):
    assert get_simplified_tokens(expression) == [
        (TokenType.NUMBER, expected_lexeme),
        (TokenType.EOF, None),
    ]


@pytest.mark.parametrize(
    "whitespace",
    [
        "",
        " ",
        "\n",
        "\t",
        "\r",
        " \n\t\r ",
    ],
)
def test_ignore_whitespace(whitespace: str):
    assert get_simplified_tokens(whitespace) == [
        (TokenType.EOF, None),
    ]


@pytest.mark.parametrize(
    "expression",
    [
        ".",
        "2.5.3",
        "1..2",
        "..2",
    ],
)
def test_invalid_numbers_raise_error(expression: str):
    with pytest.raises(UnexpectedNumberError):
        Lexer(expression).produce()


@pytest.mark.parametrize(
    "expression",
    [
        "$",
        "2 + $",
        "2 & 3",
        "abc",
    ],
)
def test_unknown_lexeme_raises_error(expression: str):
    with pytest.raises(UnknownLexemeError, match="Unknown lexeme"):
        Lexer(expression).produce()
