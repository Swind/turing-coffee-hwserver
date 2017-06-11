from utils.actor import Actor
import time
import atexit

from utils import ON, OFF

import RPi.GPIO as GPIO


def close_heater(pin_number):
    GPIO.output(pin_number, OFF)


class Heater(object):
    def __init__(self, pin_number):
        self.pin_number = pin_number

    def init_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        if self.pin_number > 0:
            GPIO.setup(self.pin_number, GPIO.OUT)
            atexit.register(close_heater, self.pin_number)

    def _getonofftime(self, cycle_time, duty_cycle):
        duty = duty_cycle / 100.0

        on_time = cycle_time * (duty)
        off_time = cycle_time * (1.0 - duty)

        return on_time, off_time

    def heat(self, cycle_time, duty_cycle):
        on_time, off_time = self._getonofftime(cycle_time, duty_cycle)
        if on_time > 0:
            GPIO.output(self.pin_number, ON)
            time.sleep(on_time)

        if off_time > 0:
            GPIO.output(self.pin_number, OFF)
            time.sleep(off_time)

    def close(self):
        close_heater(self.pin_number)
