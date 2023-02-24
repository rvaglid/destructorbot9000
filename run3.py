################
# Dependencies #
################

import RPi.GPIO as GPIO
import time


#############
# Functions #
#############

def stop():
    # Stop motors
    GPIO.output(motorRightForwardPin, GPIO.LOW)
    GPIO.output(motorRightReversePin, GPIO.LOW)
    GPIO.output(motorLeftForwardPin, GPIO.LOW)
    GPIO.output(motorLeftReversePin, GPIO.LOW)

def direction(motorLeftSpeed, motorRightSpeed, motorLeftForwards, motorRightForwards, motorLeftReverse, motorRightReverse):
    stop()

    # Set power
    motorRightPwm.ChangeDutyCycle(float(motorRightSpeed))
    motorLeftPwm.ChangeDutyCycle(float(motorLeftSpeed))

    # Set direction
    GPIO.output(motorRightForwardPin, motorLeftForwards)
    GPIO.output(motorRightReversePin, motorRightForwards)
    GPIO.output(motorLeftForwardPin, motorLeftReverse)
    GPIO.output(motorLeftReversePin, motorRightReverse)


def forward():
    print("Forward (Left power: " + str(motorLeftForwardSpeed) + " Right power: " + str(motorRightForwardSpeed) + "\n")
    direction(motorLeftForwardSpeed, motorRightForwardSpeed, GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW)    


def reverse(duration):
    print("Reversing\n")
    direction(motorLeftReverseSpeed, motorRightReverseSpeed, GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH)
    time.sleep(duration)
    stop()


def rotateRight(duration):
    print("Rotating right\n")
    motorLeftPwm.ChangeDutyCycle(float(motorLeftRotateSpeed))
    motorRightPwm.ChangeDutyCycle(float(motorRightRotateSpeed))
    direction(motorLeftRotateSpeed, motorRightRotateSpeed, GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH)
    time.sleep(duration)
    stop()


def tooClose():
    GPIO.output(distanceTriggerPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(distanceTriggerPin, GPIO.LOW)

    while GPIO.input(distanceEchoPin) == 0:
        pulse_start_time = time.time()
    while GPIO.input(distanceEchoPin) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    if distance < distanceMinimum:
        print("Too close: " + str(distance) + " CM (Minimum: " + str(distanceMinimum) + ")\n")
        return True
    else:
        print("Distance OK: " + str(distance) + " CM (Minimum: " + str(distanceMinimum) + ")\n")
        return False
    return distance


#################
# Configuration #
#################

# Pins
distanceTriggerPin = 18
distanceEchoPin = 1
motorRightPwmPin = 9
motorRightForwardPin = 24
motorRightReversePin = 23
motorLeftPwmPin = 25
motorLeftForwardPin = 10
motorLeftReversePin = 11
headlightsPin = 21

# Distance
distanceMinimum = 50

# Right motor speed
motorRightReverseSpeed = 23
motorRightForwardSpeed = 70.4
motorRightRotateSpeed = 78

# Left motor speed
motorLeftReverseSpeed = 32
motorLeftForwardSpeed = 77.6
motorLeftRotateSpeed = 87


#########
# Setup #
#########

# GPIO numbering (BCM) instead of pin numbering (BOARD)
GPIO.setmode(GPIO.BCM)

# Distance sensor
GPIO.setup(distanceTriggerPin, GPIO.OUT)
GPIO.output(distanceTriggerPin, GPIO.LOW)
GPIO.setup(distanceEchoPin, GPIO.IN)

# Right motor
GPIO.setup(motorRightForwardPin, GPIO.OUT)
GPIO.output(motorRightForwardPin, GPIO.LOW)
GPIO.setup(motorRightReversePin, GPIO.OUT)
GPIO.output(motorRightReversePin, GPIO.LOW)
GPIO.setup(motorRightPwmPin, GPIO.OUT)
motorRightPwm = GPIO.PWM(motorRightPwmPin, 1000) # Create PWM instance with 1000 Hz

# Left motor
GPIO.setup(motorLeftForwardPin, GPIO.OUT)
GPIO.output(motorLeftForwardPin, GPIO.LOW)
GPIO.setup(motorLeftReversePin, GPIO.OUT)
GPIO.output(motorLeftReversePin, GPIO.LOW)
GPIO.setup(motorLeftPwmPin, GPIO.OUT)
motorLeftPwm = GPIO.PWM(motorLeftPwmPin, 1000) # Create PWM instance with 1000 Hz

# Headlights
GPIO.setup(headlightsPin, GPIO.OUT)
GPIO.output(motorLeftForwardPin, GPIO.HIGH) # On


###########################
# Destructorbot 9000 Brain #
###########################

try:
    # Keep rotating until minimum distance found
    while tooClose():
        rotateRight(0.5)

    # Move forwards
    forward()

    # Infinite loop
    while True: 
        if tooClose():
            reverse(0.5)
            rotateRight(0.5)

            # Keep rotating until minimum distance found
            while tooClose():
                rotateRight(0.5)

            # Move forwards
            forward()
finally:
    print("Cleaning up and exit\n")
    GPIO.cleanup()
