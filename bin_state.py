"""
bin_state.py
------------
Tracks the internal state of the bin in software.

No hardware dependency - this is pure Python logic.
Manages fill levels per compartment, cycle count, and error history.

To extend:
  - Add weight sensor readings by updating record_sort() to accept a weight param
  - Add persistent storage (e.g. write state to a JSON file on each update)
  - Add per-compartment full alerts if needed
"""

import datetime
from config import WasteCategory, CATEGORY_TO_QUADRANT, FILL_THRESHOLD_PERCENT, FILL_INCREMENT_PER_ITEM


class BinState:
    """
    Tracks fill levels, cycle counts, and errors.
    Updated by SmartBin after each successful sort cycle.
    Read by TelemetryLogger when building payloads.
    """

    def __init__(self):
        self.fill_levels = {cat: 0.0 for cat in CATEGORY_TO_QUADRANT}
        self.cycle_count = 0
        self.errors: list[str] = []

    def record_sort(self, category: WasteCategory,
                    fill_increment: float = FILL_INCREMENT_PER_ITEM):
        """
        Record a successful sort event.
        Increments the fill level for the relevant compartment.
        fill_increment is an estimated % fill per item.
        """
        if category in self.fill_levels:
            self.fill_levels[category] = min(
                100.0, self.fill_levels[category] + fill_increment
            )
        self.cycle_count += 1

    def is_full(self, category: WasteCategory) -> bool:
        """Returns True if the given compartment is at or above the fill threshold."""
        return self.fill_levels.get(category, 0) >= FILL_THRESHOLD_PERCENT

    def any_compartment_full(self) -> bool:
        """Returns True if any compartment has reached the fill threshold."""
        return any(self.is_full(cat) for cat in CATEGORY_TO_QUADRANT)

    def get_status_summary(self) -> dict:
        """
        Returns a dictionary snapshot of the current bin state.
        Used by TelemetryLogger and SmartBin for reporting.
        """
        return {
            "cycle_count": self.cycle_count,
            "fill_levels": {cat.value: level for cat, level in self.fill_levels.items()},
            "any_full":    self.any_compartment_full(),
            "errors":      self.errors,
        }

    def log_error(self, message: str):
        """Append a timestamped error message to the error log."""
        timestamp = datetime.datetime.now().isoformat()
        entry = f"[{timestamp}] {message}"
        self.errors.append(entry)
        print(f"[BinState] Error logged: {message}")
