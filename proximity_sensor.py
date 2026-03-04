"""
detects when an item is placed on the sorting plate

Hardware dependencies (TODO for hardware team):
  - HC-SR04 ultrasonic sensor
  - GPIO pins on Raspberry Pi

To implement:
  - Fill in _initialise_sensor() with GPIO pin setup
  - Fill in item_detected() to measure distance and return True/False
"""

import time
from config import PROXIMITY_TIMEOUT


class ProximitySensor:
    """
    polls the ultrasonic sensor to detect when an item is present

    the main entry point for the rest of the system is wait_for_item()
    which blocks until an item is detected or the timeout is reached
    """

    def __init__(self):
        self._initialise_sensor()

    def _initialise_sensor(self):
        """
        TODO: HARDWARE
        Set up GPIO pins for the HC-SR04 sensor.

        Example (RPi.GPIO):
            import RPi.GPIO as GPIO
            self.TRIG = 23
            self.ECHO = 24
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.TRIG, GPIO.OUT)
            GPIO.setup(self.ECHO, GPIO.IN)
        """
        print("[ProximitySensor] Sensor initialised (stub)")

    def item_detected(self) -> bool:
        """
        TODO: HARDWARE
        Returns True if an item is detected within range (< ~20cm).

        Example:
            distance_cm = self._measure_distance()
            return distance_cm < 20

        Where _measure_distance() triggers a pulse and measures echo duration.
        """
        print("[ProximitySensor] item_detected() called (stub) - returning False")
        return False  # placeholder

    def wait_for_item(self, poll_interval: float = 0.1,
                      timeout: float = PROXIMITY_TIMEOUT) -> bool:
        """
        Blocks until an item is detected or timeout is reached
        Returns True if item detected, False if timed out
        Called by SmartBin in the main run loop
        """
        start = time.time()
        while time.time() - start < timeout:
            if self.item_detected():
                return True
            time.sleep(poll_interval)
        return False
