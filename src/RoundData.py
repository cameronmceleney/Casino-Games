#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Track key attributes from a single game of Keno.

Struct-like container.

Notes:
    File version
        0.1.0
    Project
        Keno-Game
    Path
        /RoundData.py
    Author
        Cameron Aidan McEleney 
    Created
        17 Sept 2025
    IDE
        PyCharm
"""

from pydantic import BaseModel, Field

__all__ = ['RoundData']


class RoundData(BaseModel):
    draw: list[int] = Field(default_factory=list)
    matches: list[int] = Field(default_factory=list)
    num_matches: int = 0
    payout: float = 0.0
