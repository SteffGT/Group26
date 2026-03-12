"""
controls the RGB status LED for user feedback

Hardware dependencies (TODO for hardware team):
  - RGB LED connected to GPIO pins on Raspberry Pi

To implement:
  - Fill in _initialise_gpio() with GPIO pin setup
  - Fill in set_colour() with GPIO HIGH/LOW output calls

Colour conventions (can be changed here if its needed):
  - blue   = standby / waiting for item
  - green  = sort successful
  - red    = error / unknown item
  - Off    = system idle / shutdown
"""

from config import WasteCategory


class StatusLED:
    """
    Simple RGB LED controller
    Called by SmartBin at each stage of the sort cycle to give visual feedback
    """

    def __init__(self):
        self._initialise_gpio()

    def _initialise_gpio(self):
        """
        TODO: HARDWARE
        Set up GPIO pins for the RGB LED

        Example (RPi.GPIO):
            import RPi.GPIO as GPIO
            self.RED   = 12
            self.GREEN = 18
            self.BLUE  = 16
            for pin in [self.RED, self.GREEN, self.BLUE]:
                GPIO.setup(pin, GPIO.OUT)
        """
        print("[StatusLED] GPIO initialised (stub)")

    def set_colour(self, red: bool, green: bool, blue: bool):
        """
        TODO: HARDWARE
        Set LED colour by toggling GPIO pins HIGH or LOW

        Example:
            GPIO.output(self.RED,   GPIO.HIGH if red   else GPIO.LOW)
            GPIO.output(self.GREEN, GPIO.HIGH if green else GPIO.LOW)
            GPIO.output(self.BLUE,  GPIO.HIGH if blue  else GPIO.LOW)
        """
        print(f"[StatusLED] colour set R={red} G={green} B={blue} (stub)")

    def success(self):
        """Green — item successfully sorted."""
        self.set_colour(red=False, green=True, blue=False)

    def error(self):
        """Red — classification failed or unknown item."""
        self.set_colour(red=True, green=False, blue=False)

    def standby(self):
        """Blue — waiting for an item."""
        self.set_colour(red=False, green=False, blue=True)

    def off(self):
        """All off."""
        self.set_colour(red=False, green=False, blue=False)
