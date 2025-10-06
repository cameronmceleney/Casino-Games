#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""(One liner introducing this file game.py)

Notes:
    File version
        0.1.0
    Project
        Keno-Game
    Path
        /game.py
    Author
        Cameron Aidan McEleney
    Created
        17 Sept 2025
    IDE
        PyCharm
"""


# Standard  imports
from __future__ import annotations
from typing import Optional
from random import Random

# Local imports
from src.settings import GameSettings
from src.slip import Slip
from src.RoundData import RoundData
from src.payouts import PAYOUT_TABLE

SETTINGS = GameSettings()

__all__ = ['Keno']


class Keno:
    """Play a single game of Keno.

    Attributes:
        slip: Current slip.
        rng: Initialised rng instance.
        payouts: Payouts table that dictates reward conditions.
        settings: GameSettings instance.
        outcomes: Results of this single game.
    """
    def __init__(
            self,
            slip: Slip,
            rng: Random,
            *,
            payouts: Optional[dict[int, float]],
            settings: GameSettings = SETTINGS,
            quick_play: bool = True):
        """

        Args:
            slip: The slip/ticket to play.
            rng: The initialised instance of the rng seed. This is used to draw the house's numbers.
            payouts: Payouts table.
            quick_play: If True, automatically play this game by calling all required methods.
        """
        self.slip = slip
        self.rng = rng
        self.payouts = payouts if payouts is not None else PAYOUT_TABLE["default"]
        self.settings = settings
        self.outcomes = RoundData()

        if quick_play:
            self.auto_play()

    def draw_house_numbers(self) -> list[int]:
        """Randomly draw house numbers.

        Store the drawn numbers within Outcomes.
        """
        board = range(self.settings.Board.min_number, self.settings.Board.max_number + 1)
        draws = self.rng.sample(board, self.settings.House.draw_count)
        draws = sorted(draws)
        self.outcomes.draw = draws
        return draws

    def find_matches(self) -> list[int]:
        """Identify matches between user's slip's numbers and the house's draw.

        Store the drawn numbers within Outcomes.
        """
        overlap = set(self.outcomes.draw) & set(self.slip.numbers)
        matches = sorted(list(overlap))

        self.outcomes.matches = matches
        self.outcomes.num_matches = len(matches)
        return matches

    def update_payout(self, n: int, b: int) -> float:
        """Check for winnings and update total payout."""
        # Check losing first; more likely cases.
        if n < self.settings.House.payout_count:
            payout = 0.0  # Better luck next time!
        else:
            rate: float = self.payouts.get(n, 0.0)
            payout = b * rate  # Winning!

        self.outcomes.payout = payout
        return payout

    def auto_play(self):
        """Play a single game of Keno."""
        self.draw_house_numbers()
        self.find_matches()
        self.update_payout(self.outcomes.num_matches, self.slip.stake)
        return self.outcomes




