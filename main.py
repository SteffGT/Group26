"""
main.py
-------
Entry point for the Smart Bin system.
Run this file on the Raspberry Pi to start the system.

Usage:
    python main.py
"""

from smart_bin import SmartBin


if __name__ == "__main__":
    bin_system = SmartBin()
    bin_system.run()
