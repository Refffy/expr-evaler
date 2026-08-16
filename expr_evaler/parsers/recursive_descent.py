from expr_evaler.lexer import Token, TokenType

from .ast import (
    ASTNode,
    Constant,
    UnaryOp, USub, UAdd,
    BinaryOp, Sub, Add, Div, Mul
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
            next_token.type in (TokenType.MUL_OP, TokenType.DIV_OP)
        ):
            self.advance()
            right = self.parse_factor()

            if next_token.type is TokenType.MUL_OP:
                left = BinaryOp(op=Mul(), left=left, right=right)
            elif next_token.type is TokenType.DIV_OP:
                left = BinaryOp(op=Div(), left=left, right=right)

        return left

    def parse_factor(self) -> ASTNode:
        token = self.advance()

        match token.type:
            case TokenType.SUB_OP:
                return UnaryOp(op=USub(), operand=self.parse_factor())
            case TokenType.ADD_OP:
                return UnaryOp(op=UAdd(), operand=self.parse_factor())
            case TokenType.NUMBER:
                if not token.lexeme:
                    raise SyntaxError("Invalid number token: empty lexeme")
                if "." in token.lexeme:
                    return Constant(value=float(token.lexeme))
                return Constant(value=int(token.lexeme))
            case TokenType.LPAREN:
                expr_node = self.parse_expr()
                if self.advance().type is not TokenType.RPAREN:
                    raise SyntaxError("Closing parenthesis expected")
                return expr_node
            case _:
                raise SyntaxError(f"Unexpected token type: {token.type}")
