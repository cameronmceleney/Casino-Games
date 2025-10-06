#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main executable file for playing a game of Keno.

Notes:
    File version
        0.1.0
    Project
        Keno-Game
    Path
        /keno.py
    Author
        Cameron Aidan McEleney 
    Created
        17 Sept 2025
    IDE
        PyCharm
"""

# Standard libraries
from __future__ import annotations

from random import Random
from typing import Optional, Literal
from unittest import case

# Local imports
from src.keno import Keno
from src.parser import parse_yaml
from src.payouts import CURRENCY, PAYOUT_TABLE

__all__ = ['Casino']


class Casino:
    """Submit your betting slip and play games of Keno!

    Attributes:
        payouts: Table detailing payouts per total matched numbers per game.
        rng: Random number generator (rng) seed used for all games.
        slip: User's betting slip.
        total_payout: Cumulative payout across all games.
        total_stake: Cumulative stake (bet) across all games.
        wins: Total number of wins.
    """
    _justify_text: int = 10

    def __init__(
            self,
            game: Literal["keno"],
            slip_name: str,
            *,
            payout_rate: Optional[str] = None,
            seed: Optional[int] = None,
            show_details: bool = False
    ):
        """Initialise Keno.

        Args:
            game: The game to play.
            slip_name: Filename (including extension) of the betting slip.
            payout_rate: Keyword specifies payout rates for game.
            seed: Specify RNG seed to rerun a specific game.
            show_details: Force full print-outs (to console) of simulated games.
        """

        self.slip = self.load(slip_name, "yaml")
        self.payouts = PAYOUT_TABLE[payout_rate] if payout_rate else PAYOUT_TABLE["default"]

        self._seed = seed
        self.rng = Random(self._seed if self._seed is not None else None)

        match game:
            case "keno":
                self._game = Keno(self.slip, self.rng, payouts=self.payouts, quick_play=False)

        self._show_details = show_details

        self.total_stake: float = 0.0
        self.total_payout: float = 0.0
        self.wins: int = 0

    @staticmethod
    def _format_currency(key: str, amount: float | int) -> str:
        currencies = ['stake', 'payout', 'earnings']

        if key not in currencies:
            return str(amount)

        return f"{CURRENCY}{amount:,.2f}"

    def load(
            self,
            slip_name: str,
            parser: Literal["yaml"] = "yaml",
            show_slip: bool = True,
    ):
        """Load user's betting slip from the configuration file.

        Note:
            Doesn't automatically detect required parser.

        Args:
             slip_name: Filename (including extension)
             parser: Parser to extract user's inputs.
             show_slip: If true, show the slip's information.

        TODO:
            - Move this method into parser.py as a dedicated method of a managing class.
        """
        match parser:
            case "yaml":
                slip = parse_yaml(slip_name)
            case _:
                raise AttributeError(f"No supported parser for '{parser}'.")

        # Print left-justified contents of the slip
        if show_slip:
            print(f"\n{'-'*8}\nSlip\n{'-'*8}")

            for item in slip:
                print(f"{item[0].title():<{self._justify_text}}", end="")
                print(self._format_currency(item[0], item[1]))

        return slip

    def update_seed(self, seed: Optional[int]):
        """Change the seed of the game.

        Can be used to override the existing seed between games.

        Parameters:
            seed: Integer with which to seed the pseudo-random number generator.
        """
        if seed is not None:
            self._seed = int(seed)
        else:
            self._seed = self.rng.randrange(0, 2**16 - 1)

        return self._seed

    def play(self) -> None:
        """Play the chosen game!

        Iteratively play a single round of a game, like Keno, until all games
        have been played.
        """

        for i in range(self.slip.games):
            self._game.auto_play()
            self.total_stake += self.slip.stake
            if self._game.outcomes.payout > 0:
                self.wins += 1
                self.total_payout += self._game.outcomes.payout

            if self._show_details:
                print(f"Game {i}: {self._game.outcomes}")

        self.results()

    def results(self, show_results: bool = True) -> dict[str, int | str]:
        """Collate and optionally print overall results of the played game(s).

        Args:
            show_results: Print results to console.
        """
        earnings = self.total_payout - self.total_stake
        earnings_sign = '-' if earnings < 0.0 else ''

        outcomes = dict(rounds=self.slip.games,
                        wins=f"{self.wins}",
                        stake=f"{self._format_currency('stake', self.total_stake)}",
                        payout=f"{self._format_currency('payout', self.total_payout)}",
                        earnings=f"{earnings_sign}{self._format_currency('earnings', abs(earnings))}")

        if show_results:
            print(f"\n{'-'*8}\nResults\n{'-'*8}")

            # Only 'earnings' are bold-face to draw immediate attention to them.
            for item in outcomes:
                if item == 'earnings': print("\033[1m", end="")
                print(f"{item.title():<{self._justify_text}}{outcomes[item]}")
                if item == 'earnings': print("\033[0m")

        return outcomes

    def reset_counters(self) -> None:
        """Reset all counters.

        Normally used after resetting the seed but not reloading the slip.

        """
        self.total_stake = 0.0
        self.total_payout = 0.0
        self.wins = 0
