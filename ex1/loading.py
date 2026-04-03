"""
Exercise 1: Loading Programs
Authorized: pandas, requests, matplotlib, numpy, sys, importlib
Objective: Demonstrate understanding of package management
"""


# ----------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import importlib


# ----------------------------------------------------------------------------
#  Visual helper for colors
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

    print()
    print(color(3, " LOADING STATUS: Loading programs...\n"))
    print(color(3, " Checking dependencies:"))

    for lib, message in requirements.items():
        try:
            importlib.import_module(lib)
            version = importlib.metadata.version(lib)
            print(f" {color(6, '[OK]')} {lib} ({version}) - {message}")
        except (ImportError, importlib.metadata.PackageNotFoundError):
            print(f" {color(5, '[ERROR]')} {lib} is missing.")
            all_ready = False

    if not all_ready:
        print()
        print(color(7, ' Run one of these two commands:'))
        print(' pip install -r requirements.txt')
        print(' poetry install')

    return all_ready


# ----------------------------------------------------------------------------
#  Data Retrieval Methods
#  --- numpy      Numerical computation and data generation
#  --- requests   Handling HTTP protocols for external data
# ----------------------------------------------------------------------------

def sample_analysis(data_points: int) -> np.ndarray:
    """Standard NumPy simulation (Default)."""
    print()
    print(color(3, " Analyzing Matrix data..."))
    print(color(3, f" Processing {data_points} data points..."))
    return np.random.standard_normal(data_points)


def api_analysis(data_points: int, url: str) -> np.ndarray:
    """
    REQUESTS METHOD: External Mainframe Access.
    Fetches real-time temperature data from Le Havre.
    'Requests' handles the HTTP handshake, while 'NumPy'
    is used to structure the resulting data for analysis.
    """

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


# ----------------------------------------------------------------------------
#  Visualization Logic
# ----------------------------------------------------------------------------

def create_visualization(data: np.ndarray) -> None:
    """Use pandas for analysis and matplotlib for output."""

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
        print(color(6, f" Results saved to: {file_name}"))

        print(color(3, " Opening visualization window..."))
        plt.show()

    except Exception as e:
        print(color(5, f" ERROR: Visualization failure: {e}"))


# ----------------------------------------------------------------------------
#  Analyze "Matrix data" and generate visualization
# ----------------------------------------------------------------------------

def loading() -> None:
    """Demo"""
    data_points: int = 1000

    try:
        if check_dependencies():

            data = api_analysis(data_points,
                                'https://api.open-meteo.com/v1/forecast?'
                                'latitude=49.4938&longitude=0.1077&hourly'
                                '=temperature_2m')

            create_visualization(data)

    except Exception as e:
        print(color(1, f' ERROR! {e}'))

    print()


if __name__ == "__main__":
    loading()
