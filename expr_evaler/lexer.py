from enum import Enum
from dataclasses import dataclass

from .exceptions import UnexpectedNumberError, UnknownLexemeError


class TokenType(Enum):
    ADD_OP = '+'
    SUB_OP = '-'
    MUL_OP = '*'
    DIV_OP = '/'

    LPAREN = '('
    RPAREN = ')'

    NUMBER = 'NUMBER'

    EOF = None


@dataclass
class Token:
    type: TokenType
    lexeme: str | None
    pos: int


class Lexer:
    def __init__(self, expr: str) -> None:
        # self.line = 0
        self.tokenlookup = {
            "+": TokenType.ADD_OP,
            "-": TokenType.SUB_OP,
            "*": TokenType.MUL_OP,
            "/": TokenType.DIV_OP,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN
        }
        self.pos = 0
        self.expr = expr
        self.tokens: list[Token] = []

    def advance(self) -> str | None:
        try:
            curr_lexeme = self.expr[self.pos]
            self.pos += 1
            return curr_lexeme
        except IndexError:
            return None

    def peek(self, offset: int = 0) -> str | None:
        try:
            return self.expr[self.pos + offset]
        except IndexError: return None

    def produce(self) -> list[Token]:
        expr_len = len(self.expr)

        while self.pos < expr_len:
            token = None
            lexeme = self.advance()

            if lexeme.isnumeric():
                fractions_passed = 0
                number = ""
                number += lexeme

                while (peeked := self.peek()) is not None and peeked.isnumeric() or (peeked == "." and fractions_passed == 0):
                        if peeked == ".":
                            fractions_passed += 1

                        if (possible_number := self.advance()) is not None:
                            if self.peek() == "." and fractions_passed == 1:
                                raise UnexpectedNumberError("Unexpected number")
                            if possible_number == ".":
                                number += ".0"
                            else:
                                number += possible_number

                token = Token(type=TokenType.NUMBER, lexeme=number, pos=self.pos)
            elif lexeme == ".":
                fractions_passed = 1
                number = "0."

                while (peeked := self.peek()) is not None and peeked.isnumeric() or (peeked == "." and fractions_passed == 1):
                        if peeked == ".":
                            fractions_passed += 1

                        if fractions_passed > 1:
                            raise UnexpectedNumberError("Unexpected number")

                        if (possible_number := self.advance()) is not None: 
                            number += possible_number

                token = Token(type=TokenType.NUMBER, lexeme=number, pos=self.pos)
            elif lexeme in {" ", "\r", "\n", "\t"}:
                continue
            else:
                token_type = self.tokenlookup.get(lexeme)
                if token_type is None:
                    raise UnknownLexemeError(f"No such token type exist: {lexeme} on pos {self.pos}")
                token = Token(type=token_type, lexeme=lexeme, pos=self.pos)

            self.tokens.append(token)

        self.tokens.append(Token(type=TokenType.EOF, lexeme=None, pos=self.pos+1))
        return self.tokens


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("expr", type=str)
    args = parser.parse_args()

    tokens = Lexer(args.expr).produce()
    for token in tokens:
        print(token)
