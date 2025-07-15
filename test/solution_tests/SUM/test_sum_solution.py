import pytest
from solutions.SUM.sum_solution import SumSolution

class TestSum:
    def test_sum(self):
        assert SumSolution().compute(1, 2) == 3

    def test_non_int_input_raises(self):
        # Passing a non-integer should raise a TypeError
        with pytest.raises(TypeError) as exc:
            SumSolution().compute(1.5, 2)
        assert "integers" in str(exc.value).lower()

    def test_negative_input_raises(self):
        # Negative inputs should be rejected
        with pytest.raises(ValueError) as exc:
            SumSolution().compute(-1, 0)
        assert "positive" in str(exc.value).lower()

    def test_overflow_input_raises(self):
        # Inputs above 100 should be rejected
        with pytest.raises(ValueError) as exc:
            SumSolution().compute(0, 101)
        assert "between 0 and 100" in str(exc.value).lower()

