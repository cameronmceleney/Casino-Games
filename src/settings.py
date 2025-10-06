#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration settings for a game of Keno.

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

# Standard libraries
from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    'BoardSettings',
    'GameSettings',
    'HouseSettings',
    'PlayerSettings', ]


class BoardSettings(BaseModel):
    """Configure the number board.

    Attributes:
        min_number: Smallest selectable integer.
        max_number: Largest selectable integer.
    """
    model_config = ConfigDict(frozen=True, validate_default=True)
    min_number: int = 1
    max_number: int = 80


class PlayerSettings(BaseModel):
    """Change what the player can select on their ticket.

    Attributes:
        max_spots: Largest number of spots player can request.
        max_stake: Largest accepted wager (per game).
    """
    model_config = ConfigDict(frozen=True, validate_default=True)
    max_spots: int = 10
    max_stake: int = 1000


class HouseSettings(BaseModel):
    """Customise the house-rules.

    Attributes:
        draw_count: Total draw numbers for the player to match their against; increase this to improve player's odds of winning.
        payout_count: Minimum (threshold) number of matched numbers required to
        permit a payout; overrides zeroes placed in PAYOUT_TABLE entries.

    """
    model_config = ConfigDict(frozen=True, validate_default=True)
    draw_count: int = 20
    payout_count: int = 5


class GameSettings(BaseModel):
    """Container for all game settings."""
    Board: BoardSettings = Field(default_factory=BoardSettings)
    Player: PlayerSettings = Field(default_factory=PlayerSettings)
    House: HouseSettings = Field(default_factory=HouseSettings)
