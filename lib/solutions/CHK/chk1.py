class CheckoutSolution:

    # skus: a string where each character is an item code (SKU) in the basket
    def checkout(self, skus):
        # 1. Reject non-string inputs
        if not isinstance(skus, str):
            return -1

        # 2. Define our price table and special offers
        #    SKU → (unit_price, special_offer)
        #    special_offer is either None or a tuple (quantity_for_discount, discounted_price)
        price_table = {
            'A': (50,  (3, 130)),  # 3 of item A cost 130
            'B': (30,  (2, 45)),   # 2 of item B cost 45
            'C': (20,  None),      # no specials for C
            'D': (15,  None),      # no specials for D
        }

        # 3. Count how many of each item code we have, validating codes
        item_counts = {}
        for item_code in skus:
            if item_code not in price_table:
                return -1
            item_counts[item_code] = item_counts.get(item_code, 0) + 1

        # 4. Calculate the total, applying special offers first
        total_price = 0
        for item_code, count in item_counts.items():
            unit_price, special_offer = price_table[item_code]

            if special_offer:
                offer_quantity, offer_price = special_offer
                num_offers = count // offer_quantity
                remainder = count % offer_quantity

                total_price += num_offers * offer_price
                total_price += remainder * unit_price
            else:
                total_price += count * unit_price

        return total_price
