#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""(One liner introducing this file main.py)

(
Leading paragraphs explaining file in more detail.
)

Attributes:
    (Here, place any module-scope constants users will import.)

(
Trailing paragraphs summarising final details.
)

Todo:
    * (Optional section for module-wide tasks).
    * (Use format: 'YYMMDD/task_identifier - one-liner task description'
    
References:
    Style guide: `Google Python Style Guide`_

Notes:
    File version
        0.1.0
    Project
        Keno-Game
    Path
        /main.py
    Author
        Cameron Aidan McEleney < c.mceleney.1@research.gla.ac.uk >
    Created
        06 Oct 2025
    IDE
        PyCharm
        
.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html
"""

# Local application imports
from src.casino import Casino


if __name__ == "__main__":
    casino = Casino(game="keno", slip_name="keno-slip.yml")
    casino.play()
