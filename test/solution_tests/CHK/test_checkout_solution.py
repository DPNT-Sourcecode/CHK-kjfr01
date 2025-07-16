import pytest
from solutions.CHK.checkout_solution import CheckoutSolution

class TestCheckoutBasic:
    def test_empty_basket(self):
        # An empty basket should cost 0
        assert CheckoutSolution().checkout("") == 0

    def test_single_item_A(self):
        # One 'A' costs its unit price of 50
        assert CheckoutSolution().checkout("A") == 50

    def test_three_As_special(self):
        # Three 'A's trigger the 3-for-130 offer
        assert CheckoutSolution().checkout("AAA") == 130

    def test_mixed_items(self):
        # 'ABCD' = 50 + 30 + 20 + 15 = 115
        assert CheckoutSolution().checkout("ABCD") == 115
    
    def test_invalid_skus_returns_minus_one(self):
        # Any SKU outside A–D should return -1
        assert CheckoutSolution().checkout("sdjfhsdkfhgs") == -1
