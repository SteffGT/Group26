# Smart Waste Sorting Bin — Software Documentation as of 04/03/2024
**Team 26 | IoT Module**

---

## Overview

This codebase controls the Smart Bin's software logic. It is structured so that hardware-dependent code is isolated in individual component files, making it straightforward for the hardware team to drop in their implementations without the need to understand the full system.

The software side owns: object classification (camera + ML model), state tracking, and telemetry logging.
The hardware side owns: filling in the stub functions marked `# TODO: HARDWARE` in each component file.

---

## Project Structure (subject to change)

```
smartbin/
├── main.py                 # Entry point — run this on the Pi
├── config.py               # All constants, enums, and settings
├── smart_bin.py            # Main controller — orchestrates all components
├── waste_classifier.py     # Camera capture + ML classification (hardware stubs)
├── proximity_sensor.py     # Ultrasonic item detection (hardware stub)
├── sorting_mechanism.py    # Stepper motor / plate control (hardware stubs)
├── bin_state.py            # Fill levels, cycle count, error log (pure software)
├── telemetry_logger.py     # ThingsBoard MQTT logging (hardware/network stubs)
└── status_led.py           # RGB LED feedback (hardware stubs)
```

---

## File-by-File Guide

### `main.py`
The only file you need to run. Creates a `SmartBin` instance and starts the event loop. You should not need to edit this.

---

### `config.py`
Central place for all constants and settings. If anything needs changing system-wide such as the waste categories, fill thresholds, file paths, timing — change it here and it will apply everywhere.

Key things defined here:
- `WasteCategory` enum — the four waste types (GENERAL, PLASTIC, PAPER, TINS_GLASS) plus UNKNOWN
- `CATEGORY_TO_QUADRANT` — maps each category to a physical plate quadrant (0–3)
- `FILL_THRESHOLD_PERCENT` — at what % fill level to trigger a full alert
- `MODEL_PATH` — path to the `.tflite` model file
- `THINGSBOARD_CREDENTIALS_PATH` — path to the credentials JSON

**To add a new waste category:** add it to the `WasteCategory` enum and add a mapping in `CATEGORY_TO_QUADRANT`. The rest of the system will pick it up automatically.

---

### `smart_bin.py` — Main Controller
Ties everything together. Runs the main event loop and calls each component in sequence during a sort cycle.

Sort cycle order:
1. Wait for item (`ProximitySensor`)
2. Capture image and classify it (`WasteClassifier`)
3. Rotate plate to correct compartment (`SortingMechanism`)
4. Update fill levels and cycle count (`BinState`)
5. Send telemetry payload (`TelemetryLogger`)
6. Update LED colour (`StatusLED`)

You should not need to edit this file unless the overall cycle logic changes (e.g. adding a new step like weight sensing).

---

### `waste_classifier.py` — Camera + ML
Owns the camera and the TFLite model. The rest of the system calls `capture_and_classify()` which returns `(WasteCategory, confidence)`.

**Hardware stubs to fill in:**
- `_initialise_camera()` — set up Pi Camera Module 3 with picamera2
- `_load_model()` — load the `.tflite` model with TFLite runtime
- `capture_image()` — capture and return a numpy array from the camera
- `classify(image)` — run inference, return `(WasteCategory, float)`

The model output categories need to map to the `WasteCategory` enum. If the model uses different labels, do the remapping inside `classify()`.

---

### `proximity_sensor.py` — Item Detection
Detects when an item is placed on the sorting plate using the HC-SR04 ultrasonic sensor.

**Hardware stubs to fill in:**
- `_initialise_sensor()` — set up GPIO TRIG and ECHO pins
- `item_detected()` — measure distance and return `True` if item is within range

`wait_for_item()` is already fully implemented — it polls `item_detected()` on a loop and is called by `SmartBin`.

---

### `sorting_mechanism.py` — Motor Control
Controls the  motor to rotate the plate to the correct compartment.

**Hardware stubs to fill in:**
- `_initialise_motor()` — set up STEP and DIR GPIO pins for the driver
- `rotate_to_quadrant(quadrant)` — calculate steps needed and drive the motor

`sort_waste(category)` is already implemented — it looks up the correct quadrant from `config.py`, calls `rotate_to_quadrant()`, waits for the item to settle, then returns to neutral. It is called by `SmartBin`.

---

### `bin_state.py` — State Tracking
Pure Python (no hardware dependency). Tracks fill levels per compartment, total cycle count, and any errors.

Updated by `SmartBin` after each sort cycle via `record_sort()`. Read by `TelemetryLogger` when building payloads.

**To extend:**
- To incorporate real weight sensor data, update `record_sort()` to accept a weight parameter instead of using a fixed increment
- To persist state across restarts, add file I/O (e.g. write to JSON on each update)

---

### `telemetry_logger.py` — ThingsBoard MQTT
Sends telemetry data to ThingsBoard after each sort cycle. Reads credentials from `thingsboard_credentials.json`.

**Hardware/network stubs to fill in:**
- `_connect()` — set up paho-mqtt client and connect to broker
- `publish(payload)` — publish the JSON payload to `v1/devices/me/telemetry`

`log_sort_event()` is fully implemented — it builds the payload and calls `publish()`. Called by `SmartBin` at the end of each cycle.

Expected credentials file format:
```json
{
    "broker": "demo.thingsboard.io",
    "port": 1883,
    "access_token": "YOUR_TOKEN_HERE"
}
```

---

### `status_led.py` — RGB LED
Gives visual feedback to the user via an RGB LED.

**Hardware stubs to fill in:**
- `_initialise_gpio()` — set up GPIO pins for R, G, B channels
- `set_colour(red, green, blue)` — toggle GPIO pins HIGH/LOW

Convenience methods already implemented: `success()`, `error()`, `standby()`, `off()`. These are called by `SmartBin` at each stage of the cycle.

---

## How to Add New Functionality

**Adding a new waste category:**
1. Add the category to `WasteCategory` in `config.py`
2. Add a quadrant mapping to `CATEGORY_TO_QUADRANT` in `config.py`
3. Nothing else needs changing

**Adding a new sensor or component:**
1. Create a new file (e.g. `weight_sensor.py`) following the same pattern — class with `_initialise_*()` and main methods
2. Import it in `smart_bin.py` and add it to `__init__()`
3. Call it at the appropriate point in `_handle_sort_cycle()`

**Changing the sort cycle:**
Edit `_handle_sort_cycle()` in `smart_bin.py` only.

**Changing timing or thresholds:**
Edit `config.py` only.

---

## Running the System

```bash
python main.py
```

when running in stub mode (no hardware connected), the system will print the actions it would take at each stage. This allows software logic to be tested without the Pi or physical components.

---

## Dependencies

```
picamera2          # Camera capture
tflite-runtime     # ML model inference
RPi.GPIO           # GPIO control
paho-mqtt          # ThingsBoard MQTT
```

to install this on the Pi:
```bash
pip install picamera2 tflite-runtime RPi.GPIO paho-mqtt
```
