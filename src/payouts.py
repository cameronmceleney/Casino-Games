CURRENCY: str = "£"
"""
Currency symbol for placed bets.
"""

PAYOUT_TABLE: dict[str, dict[int, float]] = (dict(
    # Number of matches: pay-out value
    default={0: 0.0,
             1: 0.0,
             2: 0.0,
             3: 0.0,
             4: 0.0,
             5: 3.0,
             6: 15.00,
             7: 100.00,
             8: 1_000.00,
             9: 25_000.00,
             10: 2_500_000.00}
))
"""
"""
