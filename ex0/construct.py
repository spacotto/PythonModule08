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
import site
from typing import Tuple


# ----------------------------------------------------------------------------
#  Toolkit to detect Python environment and act accodingly
# ----------------------------------------------------------------------------

class EnvironmentDetector:
    """
    A class to detect and display Python environment status.
    Ensures data streams are protected from corruption.
    """

    def __init__(self) -> None:
        """Initialize the detector with standard ANSI escape codes."""
        self.colors: dict[int, str] = {
            0: "\033[0m",     # Reset
            1: "\033[1;91m",  # Red
            2: "\033[1;92m",  # Green
            3: "\033[1;93m",  # Yellow
            4: "\033[1;94m",  # Blue
            5: "\033[1;95m",  # Magenta
            6: "\033[1;96m",  # Cyan
            7: "\033[1;97m"   # White
        }

    # ----------------------------------------------------------------------------
    #  Visual Helper for colors
    # ----------------------------------------------------------------------------

    def _color(self, code: int, text: str) -> str:
        """A function making strings of text colorful."""
        if code < 7:
            color = self.colors[code]
        else:
            color = self.colors[7]

        return f'{color}{text}{self.colors[0]}'

    # ----------------------------------------------------------------------------
    #  Behaviour outside venv
    # ----------------------------------------------------------------------------

    def _outside_venv(self) -> None:
        """Displays status when run in the global environment."""
        venv_name: str = 'matrix_env'

        print()
        print(self._color(3, ' MATRIX STATUS: You are still plugged in'))

        print()
        print(f' Current Python: {sys.executable}')
        print(' Virtual Environment: None detected')

        print()
        print(self._color(3, ' WARNING! You are in the global environment!'))
        print(' The machines can see everything you install.')

        print()
        print(self._color(3, ' Follow these steps to enter the construct:'))

        print()
        print(self._color(7, f'{" Step 1":<10}To create the venv, run:'))
        print(f'{" ":<10}python3 -m venv {venv_name}')

        print()
        print(self._color(7, f'{" Step 2":<10}If you are on Unix, run:'))
        print(f'{" ":<10}source {venv_name}/bin/activate')

        print()
        print(self._color(7, f'{" ":<10}If you are on Windows, run:'))
        print(f'{" ":<10}{venv_name}\\Scripts\\activate')

        print()
        print(self._color(7, f'{" Step 3":<10}Run this program again'))
        print()

    # ----------------------------------------------------------------------------
    #  Behaviour inside venv
    # ----------------------------------------------------------------------------

    def _get_env_info(self) -> Tuple[str, str]:
        """Extracts the environment name and absolute path."""
        try:
            env_path: str = sys.prefix
            env_name: str = os.path.basename(env_path)
            return env_name, env_path
        except Exception:
            return "Unknown", "Unknown"

    def _get_package_path(self) -> str:
        """Retrieves the primary package installation path."""
        try:
            paths: list[str] = site.getsitepackages()
            return paths[0]
        except Exception:
            return "Unknown"

    def _inside_venv(self) -> None:
        """Displays status when run in a virtual environment."""
        name, path = self._get_env_info()
        pkg_path = self._get_package_path()

        print()
        print(self._color(6, " MATRIX STATUS: Welcome to the construct"))

        print()
        print(f' {self._color(7, "Current Python:")} {sys.executable}')
        print(f' {self._color(7, "Virtual Environment:")} {name}')
        print(f' {self._color(7, "Environment Path:")} {path}')

        print()
        print(self._color(6, ' SUCCESS!') +
              ' You are in an isolated environment!')
        print(' Safe to install packages without affecting\n'
              ' the global system.')

        print()
        print(self._color(7, ' Package installation path:'))
        print(f' {pkg_path}')

        print()
        print(self._color(7, ' Run "deactivate" to return to the global'
                             ' environment.'))
        print()

    # ----------------------------------------------------------------------------
    #  Display information about the current Python environment
    # ----------------------------------------------------------------------------

    def detect_env(self) -> None:
        """Detect the environment and provide the appropriate report."""
        if sys.prefix == sys.base_prefix:
            self._outside_venv()
        else:
            self._inside_venv()


# ----------------------------------------------------------------------------
#  How to use
# ----------------------------------------------------------------------------

def main() -> None:
    """Demo"""
    ed = EnvironmentDetector()
    ed.detect_env()


if __name__ == "__main__":
    main()
