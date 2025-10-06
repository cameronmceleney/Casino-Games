#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""(One liner introducing this file parser.py)\
Notes:
    File version
        0.1.0
    Project
        Keno-Game
    Path
        /parser.py
    Author
        Cameron Aidan McEleney 
    Created
        17 Sept 2025
    IDE
        PyCharm
"""

from pathlib import Path
import yaml

# Local imports
from src.settings import GameSettings
from src.slip import Slip


__all__ = ['load_yaml', 'parse_yaml']


def load_yaml(
        filename: str,
        *,
        safe_mode: bool = True,
) -> dict:
    filepath = Path(filename).resolve()
    loader = yaml.SafeLoader if safe_mode else yaml.FullLoader
    contents = yaml.load(filepath.read_text(), Loader=loader)
    return contents


def parse_yaml(
        filename: str = "keno-slip.yml",
        cfg: GameSettings | None = None
) -> Slip:
    cfg = cfg or GameSettings()

    data = load_yaml(filename)

    clean = {k: v for k, v in data.items() if not str(k).startswith("$")}
    slip = Slip.model_validate(clean)
    return slip.validate(cfg)
