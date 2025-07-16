import pytest
from solutions.CHK.checkout_solution import CheckoutSolution

class TestUnitPricesCHK5:
    @pytest.mark.parametrize("sku,expected", [
        ("A", 50), ("B", 30), ("C", 20), ("D", 15),
        ("E", 40), ("F", 10), ("G", 20), ("H", 10),
        ("I", 35), ("J", 60), ("K", 70), ("L", 90),
        ("M", 15), ("N", 40), ("O", 10), ("P", 50),
        ("Q", 30), ("R", 50), ("S", 20), ("T", 20),
        ("U", 40), ("V", 50), ("W", 20), ("X", 17),
        ("Y", 20), ("Z", 21),
    ])
    def test_updated_unit_prices(self, sku, expected):
        assert CheckoutSolution().checkout(sku) == expected

class TestBulkAndCrossPromotionsCHK5:
    @pytest.mark.parametrize("skus,expected", [
        # CHK2 bulk A
        ("AAA", 130),
        ("AAAAA", 200),
        ("AAAAAA", 250),

        # CHK2 cross E→B
        ("EE", 80),
        ("EEB", 80),
        ("EEBB", 110),

        # CHK3 self‑free F
        ("FFF", 20),
        ("FFFF", 30),
        ("FFFFFF", 40),

        # CHK4 bulk H, K, P, Q, V
        ("HHHHH", 45),
        ("H" * 10, 80),
        ("KK", 120),
        ("PPPPP", 200),
        ("QQQ", 80),
        ("VVV", 130),

        # CHK4 cross N→M, R→Q, U→U
        ("NNNM", 120),
        ("RRRQ", 150),
        ("UUUU", 120),

        # Mixed
        ("AAAAAEEBB", 310),
        ("AAAFFF", 150),
        ("NNNMM", 135),
        ("RRRQQ", 180),
        ("UUUUU", 160),
    ])
    def test_bulk_and_cross(self, skus, expected):
        assert CheckoutSolution().checkout(skus) == expected

class TestGroupOffersCHK5:
    def test_exact_group_of_3(self):
        assert CheckoutSolution().checkout("STX") == 45
        assert CheckoutSolution().checkout("XYZ") == 45
        assert CheckoutSolution().checkout("YZS") == 45

    def test_group_prefers_highest_priced(self):
        # Pool [Z=21, S=20, T=20, X=17] → group Z,S,T =45 + X@17 =62
        assert CheckoutSolution().checkout("STXZ") == 62

    def test_group_with_five_items(self):
        # Pool [Z,S,T,Y,X] → group Z,S,T=45 + Y@20 + X@17 =82
        assert CheckoutSolution().checkout("STXYZ") == 82

    def test_multiple_groups(self):
        # Two full groups of 3 → 2*45 = 90
        assert CheckoutSolution().checkout("STXYST") == 90

    def test_group_and_individual_mix(self):
        # 5×S → one group(45) + 2*20 = 85
        assert CheckoutSolution().checkout("SSSSS") == 85

    def test_group_and_other_skus(self):
        # 'ASTX' = A@50 + group(STX)=45 → 95
        assert CheckoutSolution().checkout("ASTX") == 95

class TestInvalidInputsCHK5:
    def test_non_string(self):
        assert CheckoutSolution().checkout(123) is -1
        assert CheckoutSolution().checkout(None) is -1

    def test_unknown_sku(self):
        assert CheckoutSolution().checkout("a") == -1
        assert CheckoutSolution().checkout("-") == -1
        assert CheckoutSolution().checkout("ABCa") == -1
