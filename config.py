"""
config.py
---------
Central configuration for the Smart Bin system.

All constants, enums, and system-wide settings live here.
If you need to change a category, threshold, or file path,
this is the only file you should need to edit.
"""

from enum import Enum


class WasteCategory(Enum):
    GENERAL     = "general"
    PLASTIC     = "plastic"
    PAPER       = "paper"
    TINS_GLASS  = "tins_glass"
    UNKNOWN     = "unknown"


# Maps each waste category to a physical compartment/quadrant (0-3)
# Change these if the physical plate layout changes
CATEGORY_TO_QUADRANT = {
    WasteCategory.GENERAL:    0,
    WasteCategory.PLASTIC:    1,
    WasteCategory.PAPER:      2,
    WasteCategory.TINS_GLASS: 3,
}

# Alert when a compartment reaches this fill percentage
FILL_THRESHOLD_PERCENT = 80

# Estimated % fill added per sorted item (rough default)
FILL_INCREMENT_PER_ITEM = 2.0

# Seconds to wait for item to slide into compartment after plate rotates
SORT_SETTLE_TIME = 1.5

# How long (seconds) to wait for an item before looping again
PROXIMITY_TIMEOUT = 30.0

# Path to the TFLite model file
MODEL_PATH = "ml_model.tflite"

# Path to ThingsBoard credentials JSON
THINGSBOARD_CREDENTIALS_PATH = "thingsboard_credentials.json"

# ThingsBoard device identifier
DEVICE_ID = "smart_bin_001"
