import pytest

from expr_evaler.calculator import calculate


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("42", 42),
        ("0", 0),
        ("3.14", 3.14),
    ],
)
def test_numbers(expression: str, expected: float):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("-5", -5),
        ("+5", 5),
        ("--5", 5),
        ("---5", -5),
        ("-3.14", -3.14),
    ],
)
def test_unary_operations(expression: str, expected: float):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 + 2", 3),
        ("10 - 5", 5),
        ("3 * 4", 12),
        ("8 / 2", 4.0),
    ],
)
def test_basic_arithmetic(expression: str, expected: float):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3 * 4", 14),
        ("2 * 3 + 4", 10),
        ("10 - 3 - 2", 5),
        ("8 / 4 / 2", 1.0),
    ],
)
def test_precedence_and_associativity(expression: str, expected: float):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("(2 + 3) * 4", 20),
        ("2 * (3 + 4)", 14),
        ("((1 + 2) * 3) - 4", 5),
    ],
)
def test_parentheses(expression: str, expected: float):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("-(1) + 2 % 3.0 / 1", 1.0),
        ("-2 + 3 * (4 - 1)", 7),
        ("10 / 2 * 5", 25.0),
        ("10 / (2 * 5)", 1.0),
        ("2.5 * 2 + 1.5", 6.5),
        ("12 ** (1+2)", 1728),
        ("2 ** 3 ** 1 + 2", 10),
    ],
)
def test_complex_expressions(expression: str, expected: float):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    "expression",
    [
        "1 / 0",
        "0 / 0",
        "10 / (5 - 5)",
    ],
)
def test_division_by_zero(expression: str):
    with pytest.raises(ZeroDivisionError):
        calculate(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "(1 + 2",
        "1 +",
        "1 + * 2",
        "",
    ],
)
def test_invalid_syntax(expression: str):
    with pytest.raises(SyntaxError):
        calculate(expression)
