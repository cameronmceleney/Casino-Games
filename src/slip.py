#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Player's betting slip / ticket.

Notes:
    File version
        0.1.0
    Project
        Keno-Game
    Path
        /settings.py
    Author
        Cameron Aidan McEleney 
    Created
        17 Sept 2025
    IDE
        PyCharm
"""

# Standard  imports
from __future__ import annotations
from pydantic import AliasChoices, BaseModel, Field, field_validator

from src.settings import GameSettings

__all__ = ['Slip']


class Slip(BaseModel):
    """Players betting slip / ticket.

    Required parameters to play game Keno. Created as a model, instead of a
    dataclass, to simplify data imports from the (configuration) YAML file.

    Attributes:
        spots: Total numbers (spots) selected.
        stake: Amount of money wagered by the player.
        games: Total number of games to be played.
        numbers: Numbers the player will try to match againgst the draw.
    """
    spots: int
    stake: int = Field(validation_alias=AliasChoices("stake", "bet"))
    games: int
    numbers: list[int]

    @field_validator("spots")
    @classmethod
    def _validate_spots(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Spots must be positive.")
        return v

    @field_validator("stake")
    @classmethod
    def _validate_stake(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("stake must be positive.")
        return v

    @field_validator("games")
    @classmethod
    def _validate_games(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Games must be positive.")
        return v

    @field_validator("numbers")
    @classmethod
    def _validate_numbers(cls, v: list[int]) -> list[int]:
        if not v:
            raise ValueError("Numbers cannot be empty.")
        return v

    def validate(self, cfg: GameSettings):

        if self.spots > cfg.Player.max_spots:
            raise ValueError(f"Spots {self.spots} is too big. Limit is {cfg.Player.max_spots}")

        if self.spots != len(self.numbers):
            raise ValueError(f"Spots {self.spots} must be equal to number of unique numbers {len(self.numbers)}.")

        if self.stake > cfg.Player.max_stake:
            raise ValueError(f"stake {self.stake} too much! Limit is {cfg.Player.max_stake}")

        if len(set(self.numbers)) != len(self.numbers):
            raise ValueError(f"Numbers {self.numbers} must be unique.")

        lower, upper = cfg.Board.min_number, cfg.Board.max_number
        out_of_range = [n for n in self.numbers if not (lower <= n <= upper)]

        if out_of_range:
            raise ValueError(f"Numbers {self.numbers} must be stakeween {lower} and {upper}.")

        self.numbers = sorted(self.numbers)

        return self
