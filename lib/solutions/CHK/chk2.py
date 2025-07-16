class CheckoutSolution:
    # Unit price per SKU
    ITEM_UNIT_PRICES = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15,
        'E': 40,
    }

    # Bulk-purchase discounts: SKU → list of (quantity_needed, total_price), sorted highest quantity first
    ITEM_BULK_DISCOUNTS = {
        'A': [(5, 200), (3, 130)],
        'B': [(2, 45)],
        'C': [],
        'D': [],
        'E': [],
    }

    # Cross-SKU promotions: for every required_qty of required_sku you get free_qty of free_sku
    SKU_CROSS_PROMOTIONS = [
        ('E', 2, 'B', 1),
    ]

    def checkout(self, sku_string):
        """
        Calculate total price for the basket defined by sku_string.
        Returns -1 on invalid input or unknown SKU.
        """
        # 1. Validate input type
        if not isinstance(sku_string, str):
            return -1

        # 2. Tally each SKU
        counts = {}
        for sku in sku_string:
            if sku not in self.ITEM_UNIT_PRICES:
                return -1
            counts[sku] = counts.get(sku, 0) + 1

        # 3. Apply cross-SKU promotions first
        for required_sku, required_qty, free_sku, free_qty in self.SKU_CROSS_PROMOTIONS:
            times_applicable = counts.get(required_sku, 0) // required_qty
            total_free = times_applicable * free_qty
            if free_sku in counts:
                # reduce the payable count of the free SKU, but never below zero
                counts[free_sku] = max(counts[free_sku] - total_free, 0)

        # 4. Compute total with bulk discounts then unit prices
        total_price = 0
        for sku, qty in counts.items():
            # apply each bulk discount in descending order of quantity
            for discount_qty, discount_price in self.ITEM_BULK_DISCOUNTS.get(sku, []):
                num_discounts, qty = divmod(qty, discount_qty)
                total_price += num_discounts * discount_price
            # remaining items at standard unit price
            total_price += qty * self.ITEM_UNIT_PRICES[sku]

        return total_price
