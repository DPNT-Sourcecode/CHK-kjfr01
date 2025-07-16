from collections import Counter

class CheckoutSolution:
    """
    Supermarket checkout supporting:
      - Unit pricing for all SKUs
      - Bulk‑purchase discounts for select SKUs
      - Cross‑SKU promotions (including self‑free offers)
    """

    # Unit prices for every SKU
    ITEM_UNIT_PRICES = {
        'A': 50, 'B': 30, 'C': 20, 'D': 15,
        'E': 40, 'F': 10, 'G': 20, 'H': 10,
        'I': 35, 'J': 60, 'K': 80, 'L': 90,
        'M': 15, 'N': 40, 'O': 10, 'P': 50,
        'Q': 30, 'R': 50, 'S': 30, 'T': 20,
        'U': 40, 'V': 50, 'W': 20, 'X': 90,
        'Y': 10, 'Z': 50,
    }

    # Only SKUs with true bulk discounts are listed here;
    # others will default to no bulk deals.
    ITEM_BULK_DISCOUNTS = {
        'A': [(5, 200), (3, 130)],
        'B': [(2, 45)],
        'H': [(10, 80), (5, 45)],
        'K': [(2, 150)],
        'P': [(5, 200)],
        'Q': [(3, 80)],
        'V': [(3, 130), (2, 90)],
    }

    # Cross‑SKU promotions:
    # (required_sku, required_qty, free_sku, free_qty)
    SKU_CROSS_PROMOTIONS = [
        ('E', 2, 'B', 1),   # 2 E → 1 B free
        ('F', 3, 'F', 1),   # 3 F → pay for 2
        ('N', 3, 'M', 1),   # 3 N → 1 M free
        ('R', 3, 'Q', 1),   # 3 R → 1 Q free
        ('U', 4, 'U', 1),   # There was a misunderstanding here if it says '3U get one U free' this means you pay for 3 and get the fourth free'
    ]

    def checkout(self, sku_string):
        """
        Calculate the total price for the basket defined by sku_string.
        Returns -1 on invalid input or unknown SKU.
        """
        if not isinstance(sku_string, str):
            return -1

        counts = Counter(sku_string)
        # Validate all SKUs
        if any(sku not in self.ITEM_UNIT_PRICES for sku in counts):
            return -1

        # 1) Apply cross‑SKU promotions first
        for req, req_qty, free, free_qty in self.SKU_CROSS_PROMOTIONS:
            applicable = counts.get(req, 0) // req_qty
            if applicable and counts.get(free, 0):
                counts[free] = max(counts[free] - applicable * free_qty, 0)

        # 2) Compute total: bulk discounts → unit prices
        total = 0
        for sku, qty in counts.items():
            # bulk tiers (if any)
            for bulk_qty, bulk_price in self.ITEM_BULK_DISCOUNTS.get(sku, []):
                num, qty = divmod(qty, bulk_qty)
                total += num * bulk_price
            # remaining at standard price
            total += qty * self.ITEM_UNIT_PRICES[sku]

        return total
