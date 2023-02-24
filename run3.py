################
# Dependencies #
################

import RPi.GPIO as GPIO
import time


#############
# Functions #
#############


def forward(motor):
    # Turn on headlights
    GPIO.output(headlightsPin, GPIO.HIGH)

    print("Forward\n")
    GPIO.output(motorRightForwardPin, GPIO.HIGH)
    GPIO.output(motorRightReversePin, GPIO.LOW)
    GPIO.output(motorLeftForwardPin, GPIO.HIGH)
    GPIO.output(motorLeftReversePin, GPIO.LOW)

    print("Motor: " + motor + " Power: " + str(motorRightForwardSpeed) + "\n")
    motorRightPwm.ChangeDutyCycle(motorRightForwardSpeed)

    print("Motor: " + motor + " Power: " + str(motorLeftForwardSpeed) + "\n")
    motorLeftPwm.ChangeDutyCycle(motorLeftForwardSpeed)


def stop():
    print("Stopping\n")
    
    # Turn off headlights
    GPIO.output(headlightsPin, GPIO.LOW)
    
    # Stop motors
    GPIO.output(motorRightForwardPin, GPIO.LOW)
    GPIO.output(motorRightReversePin, GPIO.LOW)
    GPIO.output(motorLeftForwardPin, GPIO.LOW)
    GPIO.output(motorLeftReversePin, GPIO.LOW)


def reverse():
    print("Reversing\n")
    motorRightPwm.ChangeDutyCycle(motorRightReverseSpeed)
    motorLeftPwm.ChangeDutyCycle(motorLeftReverseSpeed)
    GPIO.output(motorRightForwardPin, GPIO.LOW)
    GPIO.output(motorRightReversePin, GPIO.HIGH)
    GPIO.output(motorLeftForwardPin, GPIO.LOW)
    GPIO.output(motorLeftReversePin, GPIO.HIGH)


def rotateRight():
    print("Rotating right\n")
    motorLeftPwm.ChangeDutyCycle(motorLeftRotateSpeed)
    motorRightPwm.ChangeDutyCycle(motorRightRotateSpeed)
    GPIO.output(motorRightReversePin, GPIO.LOW)
    GPIO.output(motorLeftForwardPin, GPIO.LOW)
    GPIO.output(motorRightForwardPin, GPIO.HIGH)
    GPIO.output(motorLeftReversePin, GPIO.HIGH)


def checkDistance():
    GPIO.output(distanceTriggerPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(distanceTriggerPin, GPIO.LOW)

    while GPIO.input(distanceEchoPin) == 0:
        pulse_start_time = time.time()
    while GPIO.input(distanceEchoPin) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print("Distance: ", distance, " CM\n")
    return distance


def redirect():
    reverse()
    time.sleep(0.5)
    rotateRight()
    time.sleep(0.5)
    stop()

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

# Right motor speed
motorRightReverseSpeed = 23
motorRightForwardSpeed = 70,4
motorRightRotateSpeed = 78

# Left motor speed
motorLeftReverseSpeed = 32
motorLeftForwardSpeed = 77,6
motorLeftRotateSpeed = 87


#########
# Setup #
#########

# GPIO numbering (BCM) instead of pin numbering (BOARD)
GPIO.setmode(GPIO.BCM)

# Distance sensor
GPIO.setup(distanceTriggerPin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(distanceEchoPin, GPIO.IN)

# Right motor
GPIO.setup(motorRightForwardPin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motorRightReversePin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motorRightPwmPin, GPIO.OUT)
motorRightPwm = GPIO.PWM(motorRightPwmPin, 1000) # Create PWM instance with 1000 Hz

# Left motor
GPIO.setup(motorLeftForwardPin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motorLeftReversePin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motorLeftPwmPin, GPIO.OUT)
motorLeftPwm = GPIO.PWM(motorLeftPwmPin, 1000) # Create PWM instance with 1000 Hz

# Headlights
GPIO.setup(headlightsPin, GPIO.OUT)


###########################
# Destructobot 9000 Brain #
###########################

try:
    while True: # Infinite loop
        distance = checkDistance()
        if distance > 50:
            forward()
        else:
            redirect()
finally:
    print("Cleaning up and exit\n")
    GPIO.cleanup()
