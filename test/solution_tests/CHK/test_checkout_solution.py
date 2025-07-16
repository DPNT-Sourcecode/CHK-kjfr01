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


class TestCheckoutPromotionsCHK4:
    def test_no_discounts_for_other_items(self):
        # G=20, I=35, J=60, L=90, O=10, S=30, T=20, W=20, X=90, Z=50
        assert CheckoutSolution().checkout("GIJLOSTWXZ") == 425

    def test_H_bulk_discounts(self):
        # 5H for 45
        assert CheckoutSolution().checkout("HHHHH") == 45
        # 10H for 80
        assert CheckoutSolution().checkout("H" * 10) == 80
        # 14H = 10-for-80 + 4*10 = 120
        assert CheckoutSolution().checkout("H" * 14) == 120

    def test_K_bulk_discounts(self):
        # 2K for 150
        assert CheckoutSolution().checkout("KK") == 150
        # 3K = 2-for-150 + 1*80 = 230
        assert CheckoutSolution().checkout("KKK") == 230

    def test_P_bulk_discounts(self):
        # 5P for 200
        assert CheckoutSolution().checkout("PPPPP") == 200
        # 7P = 5-for-200 + 2*50 = 300
        assert CheckoutSolution().checkout("P" * 7) == 300

    def test_Q_bulk_discounts(self):
        # 3Q for 80
        assert CheckoutSolution().checkout("QQQ") == 80
        # 4Q = 3-for-80 + 1*30 = 110
        assert CheckoutSolution().checkout("QQQQ") == 110

    def test_V_bulk_discounts(self):
        # 2V for 90
        assert CheckoutSolution().checkout("VV") == 90
        # 3V for 130
        assert CheckoutSolution().checkout("VVV") == 130
        # 4V = 3-for-130 + 1*50 = 180
        assert CheckoutSolution().checkout("VVVV") == 180
        # 5V = 3-for-130 + 2-for-90 = 220
        assert CheckoutSolution().checkout("VVVVV") == 220

    def test_N_cross_promotion(self):
        # 3N get 1 M free: NNNM → 3*40 = 120, M is free
        assert CheckoutSolution().checkout("NNNM") == 120
        # NNNMM → 3N=120 + 1 paid M = 15 → 135
        assert CheckoutSolution().checkout("NNNMM") == 135

    def test_R_cross_promotion(self):
        # 3R get 1 Q free: RRRQ → 3*50 = 150, Q is free
        assert CheckoutSolution().checkout("RRRQ") == 150
        # RRRQQ → 3R=150 + 1 paid Q = 30 → 180
        assert CheckoutSolution().checkout("RRRQQ") == 180

    def test_U_self_free_promotion(self):
        # “Buy 3 U, get 1 free” ⇒ need 4 to get 1 free
        # 3 U’s: no free yet, 3*40 = 120
        assert CheckoutSolution().checkout("UUU") == 120
        # 4 U’s: 1 free, pay for 3*40 = 120
        assert CheckoutSolution().checkout("UUUU") == 120

    def test_invalid_non_string_input(self):
        # Non-string inputs must return -1
        assert CheckoutSolution().checkout(123) == -1
        assert CheckoutSolution().checkout(None) == -1

class TestCheckoutPromotionsCHK5:
    # Updated K pricing and bulk:
    def test_single_K(self):
        # Unit price is now 70
        assert CheckoutSolution().checkout("K") == 70

    def test_two_Ks_bulk(self):
        # 2K for 120 (not 150)
        assert CheckoutSolution().checkout("KK") == 120

    def test_three_Ks(self):
        # 3K = 2-for-120 + 1*70 = 190
        assert CheckoutSolution().checkout("KKK") == 190

    # Basic group-of-3 across S,T,X,Y,Z:
    def test_exact_group_of_3(self):
        # Any three of S,T,X,Y,Z for 45
        assert CheckoutSolution().checkout("STX") == 45
        assert CheckoutSolution().checkout("XYZ") == 45
        assert CheckoutSolution().checkout("YZS") == 45

    def test_group_prefers_highest_priced(self):
        # Given Z(21), S(20), T(20), X(17), pool sorted [Z, S, T, X]
        # Group of 3 removes Z,S,T => 45 + leftover X@17 = 62
        assert CheckoutSolution().checkout("STXZ") == 62

    def test_group_with_five_items(self):
        # STXYZ → pool [Z,S,T,Y,X]; remove Z,S,T => 45 + Y@20 + X@17 = 82
        assert CheckoutSolution().checkout("STXYZ") == 82

    def test_multiple_groups(self):
        # 6-groupable items → two groups of 3 for 2*45=90
        assert CheckoutSolution().checkout("STXYST") == 90

    def test_group_and_individual_mix(self):
        # 5 S’s: one group (45) + 2*20 = 85
        assert CheckoutSolution().checkout("SSSSS") == 85

    def test_group_and_other_skus(self):
        # Include A(50) and groupable items: A + STX = 50 + 45 = 95
        assert CheckoutSolution().checkout("ASTX") == 95

    # Re–test U self‑free edge
    def test_U_self_free_edge_ck5(self):
        # 3 U’s still no free (need 4), so 3*40=120
        assert CheckoutSolution().checkout("UUU") == 120
        # 4 U’s: 1 free, pay 3*40=120
        assert CheckoutSolution().checkout("UUUU") == 120
        # 5 U’s: free 1, pay 4*40=160
        assert CheckoutSolution().checkout("UUUUU") == 160

    # Ensure non‑groupable, non‑discount SKUs remain correct
    def test_non_group_items_unchanged(self):
        assert CheckoutSolution().checkout("GIJLOWZ") == (
            20 + 35 + 60 + 90 + 20 + 20 + 21
        )



