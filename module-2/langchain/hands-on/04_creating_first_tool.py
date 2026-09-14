from langchain_core.tools import tool


@tool
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width


result = calculate_area.invoke({
    "length": 10,
    "width": 5,
})

print(result)