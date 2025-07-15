class SumSolution:
  
    def compute(self, x, y):
        # 1. Ensure both params are integers
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Parameters must be integers")
        # 2. Ensure both are non‑negative
        if x < 0 or y < 0:
            raise ValueError("Both numbers need to be positive")
        # 3. Ensure both are within 0–100
        if x > 100 or y > 100:
            raise ValueError("Both numbers need to be between 0 and 100")
        # 4. Passes checks: return the sum
        return x + y
