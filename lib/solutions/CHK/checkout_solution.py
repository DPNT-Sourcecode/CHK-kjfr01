from collections import Counter

class CheckoutSolution:
    """
    Supermarket checkout supporting:
      - Unit pricing for all SKUs
      - Bulk‑purchase discounts for select SKUs
      - Cross‑SKU promotions (including self‑free offers)
      - Group discounts across multiple SKUs
    """

    # Updated unit price per SKU (CHK_R5)
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
    ITEM_BULK_DISCOUNTS = {
        'A': [(5, 200), (3, 130)],
        'B': [(2, 45)],
        'H': [(10, 80), (5, 45)],
        'K': [(2, 120)],        # updated from 150 to 120
        'P': [(5, 200)],
        'Q': [(3, 80)],
        'V': [(3, 130), (2, 90)],
    }

    # Cross‑SKU promotions: (required_sku, required_qty, free_sku, free_qty)
    SKU_CROSS_PROMOTIONS = [
        ('E', 2, 'B', 1),
        ('F', 3, 'F', 1),
        ('N', 3, 'M', 1),
        ('R', 3, 'Q', 1),
        ('U', 4, 'U', 1),
    ]

    # Group discounts: any `group_size` items from `eligible_skus` for `group_price`
    GROUP_OFFERS = [
        (['S', 'T', 'X', 'Y', 'Z'], 3, 45),
    ]

    def checkout(self, sku_string):
        if not isinstance(sku_string, str):
            return -1

        counts = Counter(sku_string)
        if any(sku not in self.ITEM_UNIT_PRICES for sku in counts):
            return -1

        # 1) Cross‑SKU promotions
        for req, req_qty, free, free_qty in self.SKU_CROSS_PROMOTIONS:
            times = counts.get(req, 0) // req_qty
            if times and counts.get(free, 0):
                counts[free] = max(counts[free] - times * free_qty, 0)

        total = 0

        # 2) Group offers
        for eligible_skus, group_size, group_price in self.GROUP_OFFERS:
            # build a pool of all items in the group
            pool = []
            for sku in eligible_skus:
                pool.extend([sku] * counts.get(sku, 0))
            # sort descending by unit price to maximize savings
            pool.sort(key=lambda s: self.ITEM_UNIT_PRICES[s], reverse=True)

            groups = len(pool) // group_size
            if groups:
                # remove grouped items from counts
                for sku in pool[:groups * group_size]:
                    counts[sku] -= 1
                total += groups * group_price

        # 3) Bulk discounts + unit pricing
        for sku, qty in counts.items():
            for bulk_qty, bulk_price in self.ITEM_BULK_DISCOUNTS.get(sku, []):
                num_offers, qty = divmod(qty, bulk_qty)
                total += num_offers * bulk_price
            total += qty * self.ITEM_UNIT_PRICES[sku]

        return total
