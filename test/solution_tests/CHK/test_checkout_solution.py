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
        # Any SKU outside A–D (and E) should return -1
        assert CheckoutSolution().checkout("sdjfhsdkfhgs") == -1


class TestCheckoutPromotionsCHK2:
    def test_five_As_special(self):
        # Five 'A's trigger the 5-for-200 offer
        assert CheckoutSolution().checkout("AAAAA") == 200

    def test_six_As_5plus_one(self):
        # Six 'A's = 5-for-200 + 1*50 = 250
        assert CheckoutSolution().checkout("AAAAAA") == 250

    def test_two_Es_without_B(self):
        # Two 'E's cost 2*40 = 80 (free-B offer applies but there's no B in basket)
        assert CheckoutSolution().checkout("EE") == 80

    def test_two_Es_and_one_B(self):
        # 'EEB': 2E = 80, gives 1 B free so B costs 0
        assert CheckoutSolution().checkout("EEB") == 80

    def test_two_Es_and_two_Bs(self):
        # 'EEBB': 2E=80 gives 1 B free, so of the 2 B's one is free and one is paid at 30 => 110
        assert CheckoutSolution().checkout("EEBB") == 110

    def test_mixed_promotions_and_units(self):
        # Combined A- and E-promotions: 'AAAAAEEBB'
        #   AAAAA = 200
        #   EE  = 80 gives 1 B free
        #   BB  = 2 B's, but one free => 1*30
        # Total = 200 + 80 + 30 = 310
        assert CheckoutSolution().checkout("AAAAAEEBB") == 310


class TestCheckoutPromotionsCHK3:
    def test_single_F(self):
        assert CheckoutSolution().checkout("F") == 10

    def test_two_Fs_no_free(self):
        assert CheckoutSolution().checkout("FF") == 20

    def test_three_Fs_one_free(self):
        # 3 F’s → pay for 2*10 = 20
        assert CheckoutSolution().checkout("FFF") == 20

    def test_four_Fs(self):
        # 4 F’s → 3 qualifies: pay 2 + 1 full: 2*10 + 1*10 = 30
        assert CheckoutSolution().checkout("FFFF") == 30

    def test_six_Fs_two_free(self):
        # 6 F’s → two “3-for-2” groups → pay 4*10 = 40
        assert CheckoutSolution().checkout("FFFFFF") == 40

    def test_mixed_F_and_A(self):
        # AAA=130 (3-for-130), plus FFF=20 → total 150
        assert CheckoutSolution().checkout("AAAFFF") == 150

