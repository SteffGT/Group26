"""
sends telemetry data to ThingsBoard via MQTT over WiFi

Hardware dependencies (TODO for hardware team):
  - WiFi connection on Raspberry Pi
  - paho-mqtt library (pip install paho-mqtt)
  - thingsboard_credentials.json in the project root

Expected credentials JSON format:
    {
        "broker": "demo.thingsboard.io",
        "port": 1883,
        "access_token": "YOUR_TOKEN_HERE"
    }

To implement:
  - Fill in _connect() with paho-mqtt client setup
  - Fill in publish() with client.publish() call
"""

import json
import datetime
from config import WasteCategory, DEVICE_ID, THINGSBOARD_CREDENTIALS_PATH
from bin_state import BinState


class TelemetryLogger:
    """
    builds and publishes telemetry payloads to ThingsBoard

    main entry point for the rest of the system is log_sort_event()
    which is called by SmartBin at the end of each sort cycle
    """

    def __init__(self, credentials_path: str = THINGSBOARD_CREDENTIALS_PATH):
        self.connected = False
        self.client    = None
        self._load_credentials(credentials_path)
        self._connect()

    def _load_credentials(self, path: str):
        """load ThingsBoard broker address and access token from JSON file."""
        try:
            with open(path) as f:
                creds = json.load(f)
            self.broker = creds.get("broker", "demo.thingsboard.io")
            self.port   = creds.get("port", 1883)
            self.token  = creds.get("access_token", "")
        except FileNotFoundError:
            print(f"[TelemetryLogger] Credentials file not found: {path} (stub mode)")
            self.broker = self.token = ""

    def _connect(self):
        """
        TODO: HARDWARE / NETWORK
        Connect to the ThingsBoard MQTT broker.

        Example (paho-mqtt):
            import paho.mqtt.client as mqtt
            self.client = mqtt.Client()
            self.client.username_pw_set(self.token)
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
            self.connected = True
        """
        print("[TelemetryLogger] MQTT connect() called (stub)")

    def publish(self, payload: dict):
        """
        TODO: HARDWARE / NETWORK
        Publish a telemetry payload dict to ThingsBoard.

        Example:
            if self.connected:
                self.client.publish(
                    "v1/devices/me/telemetry",
                    json.dumps(payload)
                )
        """
        print(f"[TelemetryLogger] publish() called with:\n{json.dumps(payload, indent=2)} (stub)")

    def log_sort_event(self, category: WasteCategory, confidence: float,
                       cycle_time_ms: float, success: bool, bin_state: BinState):
        """
        build and publish a full telemetry payload for a completed sort cycle
        called by SmartBin._handle_sort_cycle() at the end of each cycle
        """
        payload = {
            "timestamp":      datetime.datetime.now().isoformat(),
            "device_id":      DEVICE_ID,
            "classification": category.value,
            "confidence":     round(confidence, 3),
            "cycle_time_ms":  round(cycle_time_ms),
            "success":        success,
            **{f"fill_{cat.value}": level
               for cat, level in bin_state.fill_levels.items()},
        }
        self.publish(payload)
