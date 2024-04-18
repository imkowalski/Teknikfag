#from flask import Flask, jsonify
#import threading
# Define Pin numbers (modify according to your Raspberry Pi setup)
PUMP_WATER = 18  # BCM pin numbering (modify based on your wiring)
PUMP_LONG = 14
PUMP_DEEP = 15

# Define time constants (in seconds)
LONG_TIME = 80 # 80 s
DEEP_TIME = 28 # 28 S
HOUR = 3600  # One hour in seconds

# Water level sensor pin (modify based on your sensor)
WATER_LEVEL = 18

# Stepper motor pins (modify based on your setup)
STEPPER_1 = 23
STEPPER_2 = 24
STEPPER_3 = 25
ENABLE_STEPPER = 26

# All purpose relay pin (modify based on your setup)
ALL_RELAY = 21

# Removed functionalities (due to missing libraries)
# - am2320 temperature and humidity sensor
# - WiFi and web server functionalities

import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

import am2320
import website
import camera
import threading
am = am2320.AM2320()



def setup():
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    # Set pump pins as output
    GPIO.setup(PUMP_WATER, GPIO.OUT)
    GPIO.setup(PUMP_LONG, GPIO.OUT)
    GPIO.setup(PUMP_DEEP, GPIO.OUT)

    # Set stepper motor pins as output
    GPIO.setup(ENABLE_STEPPER, GPIO.OUT)
    GPIO.setup(STEPPER_1, GPIO.OUT)
    GPIO.setup(STEPPER_2, GPIO.OUT)
    GPIO.setup(STEPPER_3, GPIO.OUT)

    # Set all purpose relay pin as output
    GPIO.setup(ALL_RELAY, GPIO.OUT)


def loop():
    sleep(5)
    now = datetime.now()
    print(str(now.hour)+":"+str(now.minute),end="\r")

    picture_hour = [8,9,10,11,12,13,20,21,22,23,24,1]
    if (now.minute == 15 or now.minute == 45) and now.hour in picture_hour:
        camera.take_picture("img")
        print(">>Taken a picrute for the Website\n")
        sleep(60)
            
    if (now.hour == 9 or now.hour == 13 or now.hour == 21 or now.hour == 1) and now.minute == 0:
        img_name = camera.take_picture()
        print(">>Taken a picture for timelapse >"+str(img_name)+"\n")
        sleep(60)
    if now.minute == 0:
        sleep(0.5)
        print(">>Watering\n")
        turn_on_relays()
        sleep(1)

        # Removed: Fertilizer schedule based on missing information
        print(">>Watering Tomatoes")
        # Deep watering
        pump_water(DEEP_TIME, PUMP_DEEP)
        sleep(5)
        print(">>Watering Latuce")
        # Long watering
        pump_water(LONG_TIME, PUMP_LONG)
        sleep(1)

        turn_off_relays()
    if now.hour == 10 and datetime.today().weekday() == 0 and now.minute == 30:
        print("="*20+"\nFERTILIZING INITIALIZED\n"+"="*20)
        pump_stepper(2,22)
        pump_stepper(2,27)
        
            

def pump_stepper(volume_ml, stepper_pin):
    """
    Controls a stepper motor for a specified volume (in milliliters).

    Args:
        volume_ml (int): The desired volume to be dispensed in milliliters.
        stepper_pin (int): The GPIO pin connected to the stepper motor.
    """

    # Disable the stepper motor initially
    GPIO.output(ENABLE_STEPPER, GPIO.LOW)
    sleep(0.5)  # 500 milliseconds delay converted to seconds

    for _ in range(volume_ml):
        GPIO.output(stepper_pin, GPIO.HIGH)
        sleep(0.0001)
        GPIO.output(stepper_pin, GPIO.LOW)
        sleep(0.0001)

    # Enable the stepper motor after movement
    sleep(0.5)  # 500 milliseconds delay converted to seconds
    GPIO.output(ENABLE_STEPPER, GPIO.HIGH)
    sleep(0.25)  # 250 milliseconds delay converted to second

def pump_water(duration, pump_pin):
    """
    Activates a specific pump for a given duration.
    """
    GPIO.output(pump_pin, GPIO.HIGH)
    sleep(duration)
    GPIO.output(pump_pin, GPIO.LOW)


def turn_on_relays():
    """
    Activates all relays connected to the ALL_RELAY pin.
    """
    GPIO.output(ALL_RELAY, GPIO.HIGH)


def turn_off_relays():
    """
    Deactivates all relays connected to the ALL_RELAY pin.
    """
    GPIO.output(ALL_RELAY, GPIO.LOW)


if __name__ == "__main__":
    setup()
    web = threading.Thread(target=website.run)
    web.start()
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on exit
        print("Exiting program")
