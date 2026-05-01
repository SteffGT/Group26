import serial
import time
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'thingsboard.cs.cf.ac.uk'
ACCESS_TOKEN = 'QYU1LbKVmwuhmQB8ABjJ'
client = mqtt.Client()

client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

SERIAL_PORT = '/dev/rfcomm0'
BAUD_RATE = 9600

VALID_COMMANDS = {"XR","XL", "YR", "YL"}

VALID_MACROS= {
    "PLASTIC" : ["YR", "YL"],
    "CARDBOARD" : ["XL", "YL", "YR", "XR"],
    "WASTE" : ["YL", "YR"],
    "CANS": ["XL", "YR", "YL", "XR"]
    }

counts ={
    "PLASTIC" :0,
    "CARDBOARD":0,
    "WASTE":0,
    "CANS":0
    }
client.publish(json.dumps(counts))

def send_command(ser, command):
    command = command.strip().upper()

    if command in 	VALID_MACROS:
        for cmd in VALID_MACROS[command]:
            send_command(ser, cmd)
            time.sleep(1)
        return
    
    if command not in VALID_COMMANDS:
        print(f"Invalid command '{command}'. Use XR, XL, YR, YL or a macro like {list(MACROS.keys())}")
        return
    
    ser.write((command + '\n').encode('utf-8'))
    time.sleep(0.1)
              
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print(f"Arduino: {response}")
        print(counts)
        
def update_thingsboard(user_input):
    if user_input == "CANS":
        counts["CANS"] = counts.get("CANS", 0) + 25
        client.publish( 'v1/devices/me/telemetry', json.dumps({"CANS": counts["CANS"]}))
    elif user_input == "PLASTIC":
        counts["PLASTIC"] = counts.get("PLASTIC", 0) + 25
        client.publish( 'v1/devices/me/telemetry', json.dumps({"PLASTIC": counts["PLASTIC"]}))
    elif user_input == "CARDBOARD":
        counts["CARDBOARD"] = counts.get("CARDBOARD", 0) + 25
        client.publish( 'v1/devices/me/telemetry', json.dumps({"CARDBOARD": counts["CARDBOARD"]}))
    elif user_input == "WASTE":
        counts["WASTE"] = counts.get("WASTE", 0) + 25
        client.publish( 'v1/devices/me/telemetry', json.dumps({"WASTE": counts["WASTE"]}))
        
              
              
def main():
    try:
        ser = serial.Serial(SERIAL_PORT,BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"Connected to Arduinoon {SERIAL_PORT}")
        print("Commands: XR, XL, YR, YL | Type 'quit' to exit")
        
        while True:
            user_input = input("Enter command: ").strip()
            if user_input.lower() == 'quit':
                break
            send_command(ser, user_input)
            update_thingsboard(user_input.upper())
            
    except serial.SerialException as e:
            print(f"Serial error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed")

if __name__ == "__main__":
    main()