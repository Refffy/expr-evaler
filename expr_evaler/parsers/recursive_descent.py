from expr_evaler.lexer import Token, TokenType

from .ast import (
    ASTNode,
    Constant,
    UnaryOp, USub, UAdd,
    BinaryOp, Sub, Add, Mod, Div, Mul, Pow
)


class RecursiveDescentParser:
    def __init__(self, tokens: list[Token]) -> None:
        self.pos = 0
        self.tokens = tokens

    def peek(self, offset: int = 0) -> Token | None:
        pos = self.pos + offset

        if pos >= len(self.tokens):
            return None

        return self.tokens[pos]

    def advance(self) -> Token:
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")

        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse(self) -> ASTNode:
        ast = self.parse_expr()

        current_token = self.peek()
        if current_token is not None and current_token.type is not TokenType.EOF:
            raise SyntaxError(
                f"Unexpected token at position {current_token.pos}: '{current_token.lexeme}'"
            )

        return ast

    def parse_expr(self) -> ASTNode:
        left = self.parse_term()

        while (next_token := self.peek()) is not None and (
            next_token.type in (TokenType.ADD_OP, TokenType.SUB_OP)
        ):
            self.advance()
            right = self.parse_term()

            if next_token.type is TokenType.ADD_OP:
                left = BinaryOp(op=Add(), left=left, right=right)
            elif next_token.type is TokenType.SUB_OP:
                left = BinaryOp(op=Sub(), left=left, right=right)

        return left

    def parse_term(self) -> ASTNode:
        left = self.parse_factor()

        while (next_token := self.peek()) is not None and (
            next_token.type in {TokenType.MUL_OP, TokenType.DIV_OP, TokenType.MODULO_OP}
        ):
            self.advance()
            right = self.parse_factor()

            if next_token.type is TokenType.MUL_OP:
                left = BinaryOp(op=Mul(), left=left, right=right)
            elif next_token.type is TokenType.DIV_OP:
                left = BinaryOp(op=Div(), left=left, right=right)
            elif next_token.type is TokenType.MODULO_OP:
                left = BinaryOp(Mod(), left=left, right=right)

        return left

    def parse_atom(self) -> ASTNode:
        token = self.peek()

        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token.type is TokenType.NUMBER:
            if not token.lexeme:
                raise SyntaxError("Invalid number token: empty lexeme")

            self.advance()

            try:
                if "." in token.lexeme:
                    return Constant(value=float(token.lexeme))
                return Constant(value=int(token.lexeme))
            except ValueError:
                raise SyntaxError(f"Invalid number format: '{token.lexeme}'")

        if token.type is TokenType.LPAREN:
            self.advance()
            expr_node = self.parse_expr()
            closing_paren = self.advance()
            if closing_paren is None or closing_paren.type is not TokenType.RPAREN:
                raise SyntaxError("Closing parenthesis expected")                
            return expr_node

        raise SyntaxError(f"Unexpected token type: {token.type}")

    def parse_factor(self) -> ASTNode:
        token = self.peek()

        if token is not None and token.type is TokenType.SUB_OP:
            self.advance()
            return UnaryOp(op=USub(), operand=self.parse_factor())
        elif token is not None and token.type is TokenType.ADD_OP:
            self.advance()
            return UnaryOp(op=UAdd(), operand=self.parse_factor())
        else:
            left = self.parse_atom()
            if (next_token := self.peek()) is not None and next_token.type is TokenType.POW_OP:
                self.advance()
                right = self.parse_factor()
                if left is not None and right is not None:
                    return BinaryOp(op=Pow(), left=left, right=right)
            return left
