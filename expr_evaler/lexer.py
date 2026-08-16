from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from expr_evaler.exceptions import UnexpectedNumberError, UnknownLexemeError


class TokenType(Enum):
    ADD_OP = "+"
    SUB_OP = "-"
    MUL_OP = "*"
    DIV_OP = "/"

    LPAREN = "("
    RPAREN = ")"

    NUMBER = "NUMBER"
    EOF = "EOF"


@dataclass(frozen=True, slots=True)
class Token:
    type: TokenType
    lexeme: str | None
    pos: int


class Lexer:
    TOKENS: ClassVar[dict[str, TokenType]] = {
        "+": TokenType.ADD_OP,
        "-": TokenType.SUB_OP,
        "*": TokenType.MUL_OP,
        "/": TokenType.DIV_OP,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
    }

    def __init__(self, expr: str) -> None:
        self.expr = expr
        self.pos = 0

    def peek(self, offset: int = 0) -> str | None:
        pos = self.pos + offset

        if pos >= len(self.expr):
            return None

        return self.expr[pos]

    def advance(self) -> str:
        lexeme = self.expr[self.pos]
        self.pos += 1
        return lexeme

    def read_number(self) -> Token:
        start = self.pos
        number = ""
        dot_seen = False

        if self.peek() == ".":
            if not (maybe_number := self.peek(1)) or not maybe_number.isdigit():
                raise UnexpectedNumberError(f"Expected digit after '.' at position {start}")

            number = "0"

        while (lexeme := self.peek()) is not None:
            if lexeme.isascii() and lexeme.isdigit():
                number += self.advance()
                continue

            if lexeme == ".":
                if dot_seen:
                    raise UnexpectedNumberError(f"Unexpected second '.' at position {self.pos}")

                dot_seen = True
                number += self.advance()
                continue

            break

        if number.endswith("."):
            number += "0"

        return Token(
            type=TokenType.NUMBER,
            lexeme=number,
            pos=start,
        )

    def produce(self) -> list[Token]:
        self.pos = 0
        tokens: list[Token] = []

        while (lexeme := self.peek()) is not None:
            if lexeme.isspace():
                self.advance()
                continue

            if (lexeme.isascii() and lexeme.isdigit()) or lexeme == ".":
                tokens.append(self.read_number())
                continue

            token_type = self.TOKENS.get(lexeme)

            if token_type is None:
                raise UnknownLexemeError(f"Unknown lexeme {lexeme} at position {self.pos}")

            start = self.pos
            tokens.append(
                Token(
                    type=token_type,
                    lexeme=self.advance(),
                    pos=start,
                )
            )

        tokens.append(
            Token(
                type=TokenType.EOF,
                lexeme=None,
                pos=self.pos,
            )
        )

        return tokens
