import serial
import time
import paho.mqtt.client as mqtt
import cv2
import numpy as np

THINGSBOARD_HOST = 'thingsboard.cs.cf.ac.uk'
ACCESS_TOKEN = 'QYU1LbKVmwuhmQB8ABjJ'
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
COOLDOWN_SECONDS = 3

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

VALID_COMMANDS = {"YR", "YL", "M", "CARD", "PLAS", "WAST", "CAN"}
VALID_MACROS = {
    "PLASTIC":   ["PLAS","YR", "YL","M"],
    "CARDBOARD": ["CARD", "YR", "YL", "M"],
    "WASTE":     ["WAST", "YR", "YL", "M"],
    "CANS":      ["CAN", "YR", "YL", "M"]
}

counts = {
    "PLASTIC":   0,
    "CARDBOARD": 0,
    "WASTE":     0,
    "CANS":      0
}

COLORS = {
    "YELLOW": [{"lower": np.array([21, 120, 120]),  "upper": np.array([40, 255, 230])}],
    "PINK":   [{"lower": np.array([145, 80,  120]),  "upper": np.array([165, 200, 255])}],
    "GREEN":  [{"lower": np.array([40,  50,  40]),  "upper": np.array([90,  255, 255])}],
    "BLUE":   [{"lower": np.array([85,  80,  80]),  "upper": np.array([100, 255, 255])}],}

COLOR_TO_BIN = {
    "BLUE": "WASTE",
    "YELLOW": "CANS",
    "PINK":   "PLASTIC",
    "GREEN":  "CARDBOARD"
}


def send_command(ser, command):
    command = command.strip().upper()

    if command in VALID_MACROS:
        counts[command] += 25
        client.publish('v1/devices/me/telemetry', str(counts))
        for cmd in VALID_MACROS[command]:
            send_command(ser, cmd)
            time.sleep(1)
        return

    if command not in VALID_COMMANDS:
        print(f"Invalid command '{command}'. Valid macros: {list(VALID_MACROS.keys())}")
        return

    ser.write((command + '\n').encode('utf-8'))
    time.sleep(0.1)

    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print(f"Arduino: {response}")


def detect_color_in_frame(img):
    blurred = cv2.medianBlur(img, 5)
    imgHSV = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for color_name, ranges in COLORS.items():
        mask = np.zeros(imgHSV.shape[:2], dtype=np.uint8)
        for r in ranges:
            mask |= cv2.inRange(imgHSV, r["lower"], r["upper"])

        if cv2.countNonZero(mask) > 500:
            return color_name, mask

    return None, None

# ----------------------------------

def init_camera(width=640, height=480):
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(3, width)
    cap.set(4, height)
    return cap


def init_serial(port, baud_rate, cap):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to Arduino on {port}")
        time.sleep(1)
        return ser
    except serial.SerialException as e:
        print(f"Failed to connect to Arduino: {e}")
        cap.release()
        exit(1)

def process_frame(img, ser):
    detected_color, mask = detect_color_in_frame(img)

    if detected_color:
        bin_name = COLOR_TO_BIN.get(detected_color, "WASTE")
        print(f"Detected: {detected_color} → sending to {bin_name}")
        time.sleep(1.5)
        send_command(ser, bin_name)
        return detected_color, bin_name

    return None, None


def cleanup(ser, cap):
    if ser.is_open:
        ser.close()
        print("Serial connection closed")
    cap.release()


def run():
    cap = init_camera()
    ser = init_serial(SERIAL_PORT, BAUD_RATE, cap)

    print("Camera running. Press Ctrl+C to quit.")
    try:
        while True:
            success, img = cap.read()
            if not success:
                print("Camera read failed")
                break

            detected_color, bin_name = process_frame(img, ser)

            if detected_color:
                print(f"Cooling down for {COOLDOWN_SECONDS}s — camera off.")
                cap.release()

                time.sleep(COOLDOWN_SECONDS)

                print("Restarting camera...")
                cap = init_camera()

    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        cleanup(ser, cap)



if __name__ == "__main__":
    run()