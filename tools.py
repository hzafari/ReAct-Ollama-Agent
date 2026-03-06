import math
import traceback

from fileReader import FileReaderTool
from fileSearch import SearchTool

class Tool:
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func

    def run(self, input_str):
        try:
            return str(self.func(input_str))
        except Exception:
            return "ERROR:\n" + traceback.format_exc()


def calculator(expr: str):
    allowed = {
        "sqrt": math.sqrt,
        "pow": pow,
        "abs": abs
    }
    return eval(expr, {"__builtins__": {}}, allowed)



TOOLS = {
    "calculator": Tool(
        "calculator",
        "Evaluate mathematical expressions like sqrt(16) or 2+2",
        calculator
    ),

    "file_reader": FileReaderTool("docs"),

    "file_search": SearchTool("docs")
}
