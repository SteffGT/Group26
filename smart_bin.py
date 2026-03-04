"""

main controller. Ties all components together and runs event loop

No hardware dependency directly — all hardware is handled by the
individual component classes. This file should not need to be edited
unless the overall sort cycle logic were to require change

To extend:
  - Add new stages to _handle_sort_cycle() (e.g. weight sensing)
  - Add shutdown/cleanup logic to stop() (e.g. GPIO.cleanup())
  - Add a web API or CLI interface on top of run()
"""

import time
from waste_classifier import WasteClassifier
from proximity_sensor import ProximitySensor
from sorting_mechanism import SortingMechanism
from bin_state import BinState
from telemetry_logger import TelemetryLogger
from status_led import StatusLED
from config import WasteCategory


class SmartBin:
    """
    Cycle:
      1. Wait for item (via ProximitySensor)
      2. Capture and classify (via WasteClassifier)
      3. Rotate plate (via SortingMechanism)
      4. Update state (via BinState)
      5. Send telemetry (via TelemetryLogger)
      6. Update LED (via StatusLED)
      7. Repeat

    Usage:
        bin_system = SmartBin()
        bin_system.run()
    """

    def __init__(self):
        print("[SmartBin] Initialising...")
        self.classifier = WasteClassifier()
        self.proximity  = ProximitySensor()
        self.sorter     = SortingMechanism()
        self.state      = BinState()
        self.telemetry  = TelemetryLogger()
        self.led        = StatusLED()
        self.running    = False
        print("[SmartBin] Ready.\n")

    def _handle_sort_cycle(self):
        """Execute a full sort cycle: classify → sort → log."""
        cycle_start = time.time()

        # 1 - classify item
        self.led.standby()
        category, confidence = self.classifier.capture_and_classify()

        # 2 - sort it
        success = category != WasteCategory.UNKNOWN
        if success:
            self.sorter.sort_waste(category)
            self.state.record_sort(category)
            self.led.success()
        else:
            self.led.error()
            self.state.log_error("Classification returned UNKNOWN")

        cycle_time_ms = (time.time() - cycle_start) * 1000

        # 3 - log telemetry
        self.telemetry.log_sort_event(
            category=category,
            confidence=confidence,
            cycle_time_ms=cycle_time_ms,
            success=success,
            bin_state=self.state,
        )

        # 4 - warn if any compartment is nearly full
        if self.state.any_compartment_full():
            print("[SmartBin] WARNING: One or more compartments near full capacity")

        print(
            f"[SmartBin] Cycle complete | Category: {category.value} "
            f"| Confidence: {confidence:.2f} | Time: {cycle_time_ms:.0f}ms\n"
        )

    def run(self, max_cycles: int = None):
        """
        Main event loop, waits for items and runs sort cycles indefinitely

        Args:
            max_cycles: Stop after this many cycles. None = run forever
        """
        self.running = True
        print("[SmartBin] Starting main loop. Waiting for items...\n")

        cycles = 0
        while self.running:
            if max_cycles is not None and cycles >= max_cycles:
                break

            self.led.standby()
            item_present = self.proximity.wait_for_item()

            if item_present:
                print(f"[SmartBin] Item detected. Starting cycle {cycles + 1}...")
                self._handle_sort_cycle()
                cycles += 1

        print(f"[SmartBin] Stopped after {cycles} cycles.")
        print(f"[SmartBin] Final status: {self.state.get_status_summary()}")

    def stop(self):
        #signal the run loop to stop after the current cycle.
        self.running = False

    def status(self) -> dict:
        #return the current bin state summary
        return self.state.get_status_summary()
