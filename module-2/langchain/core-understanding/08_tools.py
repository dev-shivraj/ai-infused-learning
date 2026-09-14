from langchain_core.tools import tool


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b


print(add_numbers.invoke({
    "a": 10,
    "b": 20
}))

print(multiply_numbers.invoke({
    "a": 10,
    "b": 20
}))