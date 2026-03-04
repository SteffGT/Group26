"""
controls the motorised sorting plate.

Hardware dependencies (TODO for hardware team):
  - NEMA 17 stepper motor
  - A4988 motor driver
  - GPIO pins on Raspberry Pi

To implement:
  - Fill in _initialise_motor() with GPIO/stepper setup
  - Fill in rotate_to_quadrant() with step calculation and motor control
"""

import time
from config import WasteCategory, CATEGORY_TO_QUADRANT, SORT_SETTLE_TIME


class SortingMechanism:
    """
    rotates the sorting plate to direct waste into the correct compartment

    the main entry point for the rest of the system is sort_waste()
    which accepts a WasteCategory and handles rotation + return to neutral
    """

    def __init__(self):
        self.current_quadrant = 0
        self._initialise_motor()

    def _initialise_motor(self):
        """
        TODO: HARDWARE
        Set up GPIO pins for the stepper motor driver (A4988)

        Example (RPi.GPIO):
            import RPi.GPIO as GPIO
            self.STEP_PIN = 17
            self.DIR_PIN  = 27
            GPIO.setup(self.STEP_PIN, GPIO.OUT)
            GPIO.setup(self.DIR_PIN,  GPIO.OUT)
        """
        print("[SortingMechanism] Motor initialised (stub)")

    def rotate_to_quadrant(self, quadrant: int):
        """
        TODO: HARDWARE
        Rotate the plate to the given quadrant (0-3), where each is 90° apart.

        Example:
            steps_needed = self._calculate_steps(self.current_quadrant, quadrant)
            self._step_motor(steps_needed)
            self.current_quadrant = quadrant
        """
        print(f"[SortingMechanism] Rotating to quadrant {quadrant} (stub)")
        self.current_quadrant = quadrant

    def return_to_neutral(self):
        """Return the plate to the default neutral position (quadrant 0)."""
        self.rotate_to_quadrant(0)
        print("[SortingMechanism] Returned to neutral")

    def sort_waste(self, category: WasteCategory):
        """
        method called by SmartBin.
        Rotates to the correct quadrant for the given category,
        waits for the item to settle, then returns to neutral.
        Does nothing if category is UNKNOWN.
        """
        if category == WasteCategory.UNKNOWN:
            print("[SortingMechanism] Unknown category - no rotation")
            return

        quadrant = CATEGORY_TO_QUADRANT[category]
        self.rotate_to_quadrant(quadrant)
        time.sleep(SORT_SETTLE_TIME)
        self.return_to_neutral()
