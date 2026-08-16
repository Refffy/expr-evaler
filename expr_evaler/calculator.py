from .lexer import Lexer
from .parsers.evaler import evaluate
from .parsers.recursive_descent import RecursiveDescentParser


def calculate(expression: str) -> int | float:
    lexer = Lexer(expression)
    tokens = lexer.produce()

    parser = RecursiveDescentParser(tokens)
    tree = parser.parse()

    if tree is None:
        raise SyntaxError("Ivalid expr")

    return evaluate(tree)


if __name__ == "__main__":
    print(calculate(input()))
