from langchain_core.tools import tool


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def subtract_numbers(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


print(add_numbers.invoke({
    "a": 10,
    "b": 5,
}))

print(subtract_numbers.invoke({
    "a": 10,
    "b": 5,
}))

print(multiply_numbers.invoke({
    "a": 10,
    "b": 5,
}))