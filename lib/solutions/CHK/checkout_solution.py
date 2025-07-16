from collections import Counter

class CheckoutSolution:
    """
    Supermarket checkout supporting:
      - Unit pricing for all SKUs
      - Bulk‑purchase discounts for select SKUs
      - Cross‑SKU promotions (including self‑free offers)
      - Group discounts across multiple SKUs
    """

    # Unit price per SKU
    ITEM_UNIT_PRICES = {
        'A': 50, 'B': 30, 'C': 20, 'D': 15,
        'E': 40, 'F': 10, 'G': 20, 'H': 10,
        'I': 35, 'J': 60, 'K': 70, 'L': 90,
        'M': 15, 'N': 40, 'O': 10, 'P': 50,
        'Q': 30, 'R': 50, 'S': 20, 'T': 20,
        'U': 40, 'V': 50, 'W': 20, 'X': 17,
        'Y': 20, 'Z': 21,
    }

    # Pure bulk‑purchase discounts for individual SKUs
    # Sorted largest‑first so the best deal applies first
    ITEM_BULK_DISCOUNTS = {
        'A': [(5, 200), (3, 130)],
        'B': [(2, 45)],
        'H': [(10, 80), (5, 45)],
        'K': [(2, 120)],
        'P': [(5, 200)],
        'Q': [(3, 80)],
        'V': [(3, 130), (2, 90)],
    }

    # Cross‑SKU promotions: (required_sku, required_qty, free_sku, free_qty)
    # Self‑free offers are just free_sku == required_sku
    SKU_CROSS_PROMOTIONS = [
        ('E', 2, 'B', 1),   # 2 E → 1 B free
        ('F', 3, 'F', 1),   # 3 F → pay for 2
        ('N', 3, 'M', 1),   # 3 N → 1 M free
        ('R', 3, 'Q', 1),   # 3 R → 1 Q free
        ('U', 4, 'U', 1),   # buy 3 U, get 1 U free (requires 4 in basket)
    ]

    # Group discounts: (eligible_skus, required_total, group_price)
    GROUP_OFFERS = [
        (['S', 'T', 'X', 'Y', 'Z'], 3, 45),  # any 3 of these for 45
    ]

    def checkout(self, sku_string):
        """
        Calculate total price for the basket defined by sku_string.
        Returns -1 on invalid input or unknown SKU.
        """
        # 1. Validate input type
        if not isinstance(sku_string, str):
            return -1

        # 2. Tally SKUs
        counts = Counter(sku_string)
        if any(sku not in self.ITEM_UNIT_PRICES for sku in counts):
            return -1

        # 3. Apply cross‑SKU promotions (including self‑free)
        for req_sku, req_qty, free_sku, free_qty in self.SKU_CROSS_PROMOTIONS:
            times = counts.get(req_sku, 0) // req_qty
            if times and counts.get(free_sku, 0):
                counts[free_sku] = max(counts[free_sku] - times * free_qty, 0)

        total = 0

        # 4. Apply group offers across multiple SKUs
        for eligible_skus, group_size, group_price in self.GROUP_OFFERS:
            # expand all eligible SKUs into a list
            pool = []
            for sku in eligible_skus:
                pool.extend([sku] * counts.get(sku, 0))
            # sort by unit price descending so the biggest‐value items go into the deal first
            pool.sort(key=lambda s: self.ITEM_UNIT_PRICES[s], reverse=True)

            groups = len(pool) // group_size
            if groups:
                # remove grouped items from counts
                for sku in pool[:groups * group_size]:
                    counts[sku] -= 1
                total += groups * group_price

        # 5. Apply individual bulk discounts then unit prices
        for sku, qty in counts.items():
            for bulk_qty, bulk_price in self.ITEM_BULK_DISCOUNTS.get(sku, []):
                num_offers, qty = divmod(qty, bulk_qty)
                total += num_offers * bulk_price
            total += qty * self.ITEM_UNIT_PRICES[sku]

        return total

