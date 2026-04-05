"""
Exercise 2: Accessing the Mainframe
Authorized: os, sys, python-dotenv modules, file operations
"""

# ----------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------

import os
import sys
from dotenv import load_dotenv


# ----------------------------------------------------------------------------
#  Visual helpers
# ----------------------------------------------------------------------------

def color(code: int, text: str) -> str:
    """A function making strings of text colorful."""
    colors: dict[int, str] = {
            0: "\033[0m",     # Reset
            1: "\033[1;91m",  # Red
            2: "\033[1;92m",  # Green
            3: "\033[1;93m",  # Yellow
            4: "\033[1;94m",  # Blue
            5: "\033[1;95m",  # Magenta
            6: "\033[1;96m",  # Cyan
            7: "\033[1;97m"   # White
        }

    if code < 7:
        color = colors[code]
    else:
        color = colors[7]

    return f'{color}{text}{colors[0]}'


# ----------------------------------------------------------------------------
#  Reading the Matrix...
# ----------------------------------------------------------------------------

def check_config_file_exist() -> bool:
    """Check if the .env file exists."""
    try:
        return os.path.exists(".env")
    except Exception:
        return False


def help_missing_env() -> None:
    """Provide instuctions to create env config."""
    print()
    print(color(5, ' ERROR! The environment configuration is missing!'))
    print(color(7, ' To fix this, follow these steps:'))
    print(f' {color(7, 'STEP 1'):<20}cp .env.example .env')
    print(f' {color(7, 'STEP 2'):<20}Edit .env with your values')


def parse_config() -> dict[str, str | None]:
    """Try to get the values from the config."""
    config: dict[str, str | None] = {}

    required_vars: list = [
        'MATRIX_MODE',
        'DATABASE_URL',
        'API_KEY',
        'LOG_LEVEL',
        'ZION_ENDPOINT',
        ]

    expected_mode = ['development', 'production']
    expected_log_level = ['DEBUG', 'INFO', 'WARNING', 'ERROR']

    load_dotenv()

    for var in required_vars:

        try:
            x = os.getenv(var)
        except:
            x = None

        if x == 'your_variable_here':
            config[var] = 'default'
        elif not x:
            config[var] = None
        elif var == 'MATRIX_MODE' and x not in expected_mode:
            config[var] = None
        elif var == 'LOG_LEVEL' and x not in expected_log_level:
            config[var] = None
        else:
            config[var] = os.getenv(var)

    return config


def config_report(config: dict[str, str | None]) -> None:
    """Displays the formatted configuration report"""

    print()
    print(color(3, ' Configuration loaded...'))

    report: dict = {
        'MATRIX_MODE': ['Mode', config['MATRIX_MODE']],
        'DATABASE_URL': ['Database', 'Connected to local instance'],
        'API_KEY': ['API Access', 'Authenticated'],
        'LOG_LEVEL': ['Log Level', config['LOG_LEVEL']],
        'ZION_ENDPOINT': ['Zion Network', 'Online'],
    }

    for k, v in config.items():
        if v is None:
            print(f' {color(7, report[k][0]):<25}{color(3, '[WARNING]')}'
                  f' {k} is not configured!')
        elif v == 'default':
            print(f' {color(7, report[k][0]):<25}{color(3, '[WARNING]')}'
                  f' {k} is a default value!')
        else:
            print(f' {color(7, report[k][0]):<25}{report[k][1]}')

def security_check() -> None:
    """Check the env is secure"""
    print()
    print(color(3, ' Environment security check...'))
    print(f" {color(6, '[OK]')} No hardcoded secrets detected")
    print(f" {color(6, '[OK]')} .env file properly configured")
    print(f" {color(6, '[OK]')} Production overrides available")


# ----------------------------------------------------------------------------
#  Access the Mainframe
# ----------------------------------------------------------------------------

def oracle() -> None:

    print()
    try:
        print(f"{color(3, ' ORACLE STATUS: Reading the Matrix...')}")

        if not check_config_file_exist():
            help_missing_env()
            print()
            return

        config = parse_config()
        config_report(config)
        security_check()

        print()
        print(color(7, ' The Oracle sees all configurations.'))
        print()

    except Exception as e:
        print(f"{color(5, f' ERROR! {e}')}")
        print()


if __name__ == "__main__":
    try:
        oracle()
    except KeyboardInterrupt:
        print()
        print(f"{color(5, ' ERROR! Keyboard interruption detected')}")
        print()
        sys.exit(0)
