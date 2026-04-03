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

def sample_analysis() -> np.ndarray:
    """Standard NumPy simulation (Default)."""
    print(color(3, " Analyzing Matrix data..."))
    print(color(3, " Processing 1000 data points..."))
    return np.random.standard_normal(1000)


def api_analysis(url: str) -> np.ndarray:
    """
    REQUESTS METHOD: External Mainframe Access.
    Fetches real-time temperature data from Le Havre.
    'Requests' handles the HTTP handshake, while 'NumPy'
    is used to structure the resulting data for analysis.
    """

    print(color(3, " Accessing Mainframe: Le Havre Meteo..."))
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # Extract list of temperatures
        raw_data = response.json().get("hourly", {}).get("temperature_2m", [])

        # Convert to NumPy array
        data = np.array(raw_data)
        if len(data) < 1000:
            data = np.tile(data, (1000 // len(data) + 1))[:1000]

        return data

    except Exception as e:
        print(color(5, f" CONNECTION ERROR: {e}"))
        print(color(3, " Falling back to NumPy simulation..."))
        return sample_analysis()


# ----------------------------------------------------------------------------
#  Visualization Logic
# ----------------------------------------------------------------------------

def create_visualization(data: np.ndarray) -> None:
    """Use pandas for analysis and matplotlib for output."""
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
        print(color(2, f" Results saved to: {file_name}"))

        print(color(6, " Opening visualization window..."))
        plt.show()

    except Exception as e:
        print(color(1, f" ERROR: Visualization failure: {e}"))


# ----------------------------------------------------------------------------
#  Analyze "Matrix data" and generate visualization
# ----------------------------------------------------------------------------

def loading() -> None:
    """Demo"""
    print()

    try:
        if check_dependencies():

            print()
            data = api_analysis('https://api.ope-meteo.com/v1/forecast?'
                                'latitude=49.4938&longitude=0.1077&hourly'
                                '=temperature_2m')

            print()
            create_visualization(data)

        else:
            print()

    except Exception as e:
        print(color(1, f' ERROR! {e}'))

    print()


if __name__ == "__main__":
    loading()
