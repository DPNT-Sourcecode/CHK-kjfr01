import pytest
from solutions.HLO.hello_solution import HelloSolution

def test_hello_returns_formatted_string():
    # Expect a greeting with comma and exclamation
    assert HelloSolution().hello("Alice") == "Hello, Alice!"
