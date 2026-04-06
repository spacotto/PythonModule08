"""
Exercise 1: Loading Programs
Authorized: pandas, requests, matplotlib, numpy, sys, importlib
Objective: Demonstrate understanding of package management
"""


# ----------------------------------------------------------------------------
#  Imports (lib to be installed are inside the functions)
# ----------------------------------------------------------------------------

import sys
from importlib import import_module, metadata


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


def div(to_write: str, how_many_times: int) -> None:
    """Prints a line divider."""
    print(" " + to_write * how_many_times)


# ----------------------------------------------------------------------------
#  Provide instructions to install missing dependencies
# ----------------------------------------------------------------------------

def instructions() -> None:
    """How to install missing dependencies with pip or Poetry"""
    print()
    print(color(5, ' ERROR! Some dependencies apper to be missing!'))
    print(color(7, ' Choose a package manager to install them.'))
    print()

    x = input(color(7, f' {"OPTION 1":<10}'
                       ' Would you like to use pip (y/n)? '))
    if x == 'y':
        print(f' {"":<10} python -m venv matrix_env')
        print(f' {"":<10} source matrix_env/bin/activate')
        print(f' {"":<10} pip install -r requirements.txt')
        print(f' {"":<10} python3 loading.py')
    else:
        y = input(color(7,  f' {"OPTION 2":<10}'
                            ' Would you like to use Poetry (y/n)? '))
        if y == 'y':
            print(f' {"":<10} poetry install')
            print(f' {"":<10} poetry run python loading.py')
        else:
            print(f' {"":<10} Then enjoy your missing dependencies!')
            print(f' {"":<10} Good luck working without them :)')


# ----------------------------------------------------------------------------
#  Check dependencies status
# ----------------------------------------------------------------------------

def check_dependencies() -> bool:
    """Check if required packages are installed and display versions."""

    requirements = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "requests": "Network access ready",
        "matplotlib": "Visualization ready"
    }

    all_ready = True

    print(color(3, "\n LOADING STATUS: Loading programs..."))
    print(color(3, "\n Checking dependencies:"))

    for lib, message in requirements.items():
        try:
            import_module(lib)
            version = metadata.version(lib)
            print(f" {color(6, '[OK]')} {lib} ({version}) - {message}")
        except (ImportError, metadata.PackageNotFoundError):
            print(f" {color(5, '[ERROR]')} {lib} is missing.")
            all_ready = False

    if not all_ready:
        instructions()

    return all_ready


# ----------------------------------------------------------------------------
#  Data Retrieval Methods
#  --- numpy      Numerical computation and data generation
#  --- requests   Handling HTTP protocols for external data
# ----------------------------------------------------------------------------

def api_analysis(data_points: int, url: str) -> 'np.ndarray':
    """Fetch API data. Use 'NumPy' to structure data for analysis."""

    # --- Later imports to avoid errors when lib are not installed
    import requests
    import numpy as np

    print()
    print(color(3, " Analyzing Matrix data..."))
    print(color(3, f" Processing {data_points} data points..."))

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # Extract list of temperatures
        raw_data = response.json().get("hourly", {}).get("temperature_2m", [])

        # Convert to NumPy array
        data = np.array(raw_data)
        if len(data) < data_points:
            data = np.tile(data, (data_points // len(data) + 1))[:data_points]

        return data

    except Exception as e:
        print(color(5, f" CONNECTION ERROR: {e}"))
        print(color(3, " Falling back to NumPy simulation..."))
        return sample_analysis(data_points)


def sample_analysis(data_points: int) -> 'np.ndarray':
    """Standard NumPy simulation (Default)."""
    # --- Later imports to avoid errors when lib are not installed
    import requests
    import numpy as np

    print()
    print(color(3, " Analyzing Matrix data..."))
    print(color(3, f" Processing {data_points} data points..."))
    return np.random.standard_normal(data_points)


# ----------------------------------------------------------------------------
#  Visualization Logic
# ----------------------------------------------------------------------------

def create_visualization(data: 'np.ndarray') -> None:
    """Use pandas for analysis and matplotlib for output."""

    # --- Later imports to avoid errors when lib are not installed
    import pandas as pd
    import matplotlib.pyplot as plt

    print(color(3, " Generating visualization..."))

    try:
        df = pd.DataFrame(data, columns=['Temperature'])
        df['Trend'] = df['Temperature'].rolling(window=24).mean()

        plt.figure(figsize=(10, 6))
        plt.plot(df['Temperature'], label='Le Havre Raw Data', color='black')
        plt.plot(df['Trend'], label='24h Moving Average', color='red')

        plt.title("Matrix Analysis: Le Havre Temperature Stream")
        plt.legend()

        file_name = 'matrix_analysis.png'
        plt.savefig(file_name)
        print()
        print(color(6, " Analysis complete!"))
        print(color(6, f" Results saved to: {file_name}"))

        print(color(3, " Opening visualization window..."))
        plt.show()

    except Exception as e:
        print(color(5, f" ERROR: Visualization failure: {e}"))


# ----------------------------------------------------------------------------
#  Analyze "Matrix data" and generate visualization
# ----------------------------------------------------------------------------

def loading() -> None:
    """Main execution flow for Matrix data analysis."""
    data_points: int = 1000

    try:
        # Check dependencies status
        if check_dependencies():

            # Fetch data from the Mainframe or fallback to Simulation
            data = api_analysis(data_points,
                                'https://api.open-meteo.com/v1/forecast?'
                                'latitud=49.4938&longitude=0.1077&hourly'
                                '=temperature_2m')

            # Generate the visual output
            create_visualization(data)

    except Exception as e:
        print(color(1, f' ERROR! {e}'))

    print()


if __name__ == "__main__":
    try:
        loading()
    except KeyboardInterrupt:
        print()
        print(f"{color(5, ' ERROR! Keyboard interruption detected')}")
        print()
        sys.exit(0)
