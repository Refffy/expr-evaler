import argparse

from expr_evaler import Lexer, RecursiveDescentParser, calculate


def print_tokens(expression: str) -> None:
    lexer = Lexer(expression)
    for token in lexer.produce():
        print(token)


def print_ast(expression: str) -> None:
    lexer = Lexer(expression)
    tokens = lexer.produce()
    parser = RecursiveDescentParser(tokens)
    tree = parser.parse_expr()

    print(tree)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mathematical expressions evaler",
        epilog="Example: python main.py '2 + 2 * 2' -e",
    )

    parser.add_argument("expression", type=str, help="Mathematical expression")

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-t",
        "--tokenize",
        action="store_true",
        help="Get tokenized output",
    )

    group.add_argument(
        "-p",
        "--parse",
        action="store_true",
        help="Tokenize and parse the expression and show the AST",
    )

    group.add_argument(
        "-e",
        "--evaluate",
        action="store_true",
        help="Evaluate the expression",
    )

    args = parser.parse_args()

    if args.tokenize:
        print_tokens(args.expression)
    elif args.parse:
        print_ast(args.expression)
    else:
        result = calculate(args.expression)
        print(result)


if __name__ == "__main__":
    main()
