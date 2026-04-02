"""
Exercise 0: Entering the Matrix
Authorized: sys, os, site modules, print().
Objective: Demonstrate understanding of Python virtual environments.
"""

# ----------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------

import sys
import os


# ----------------------------------------------------------------------------
#  Visual Helper
# ----------------------------------------------------------------------------

def color(code: int, text: str) -> str:
    """A function making strings of text colorful."""
    # Colors
    red = "\033[1;91m"
    green = "\033[1;92m"
    yellow = "\033[1;93m"
    blue = "\033[1;94m"
    magenta = "\033[1;95m"
    cyan = "\033[1;96m"
    white = "\033[1;97m"
    reset = '\033[0m'

    # Choice
    if code == 1:
        color = red
    elif code == 2:
        color = green
    elif code == 3:
        color = yellow
    elif code == 4:
        color = blue
    elif code == 5:
        color = magenta
    elif code == 6:
        color = cyan
    else:
        color = white

    return f'{color}{text}{reset}'


# ----------------------------------------------------------------------------
#  Detect env and act accordingly
# ----------------------------------------------------------------------------

def outside_venv() -> None:
    """..."""
    print()
    print(color(3, " MATRIX STATUS: You're still plugged in"))

    print()

    print()


def inside_venv() -> None:
    """..."""
    print()
    print(color(6, " MATRIX STATUS: Welcome to the construct"))

    print()

    print()


def detect_venv() -> None:
    """Detect in which env the program is running"""
    if sys.prefix == sys.base_prefix:
        outside_venv()
    else:
        inside_venv()


if __name__ == "__main__":
    detect_venv()
