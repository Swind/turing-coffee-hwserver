import time
import RPi.GPIO as GPIO

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Refill(object):
    def __init__(self, config):
        GPIO.setwarnings(False)
        self._stop = False
        # Read Config
        self.config = config

        # Setup Raspberry Pi GPIO
        GPIO.setmode(GPIO.BOARD)

        self._init_water_level_pins()
        self._init_motor_pin()

    def _init_water_level_pins(self):
        # Water Level
        self.water_pin_out, self.water_pin_in = self.config['water_level_pin']
        GPIO.setup(self.water_pin_out, GPIO.OUT)
        GPIO.output(self.water_pin_out, True)

        GPIO.setup(self.water_pin_in,
                   GPIO.IN,
                   pull_up_down=GPIO.PUD_DOWN)

        logger.info('Set water level GPIO {} to OUT and {} to IN'.format(
            self.water_pin_out,
            self.water_pin_in))

    def _init_motor_pin(self):
        self.motor_pin_pwm, self.motor_pin_direct = self.config['motor_pin']

        GPIO.setup(self.motor_pin_pwm, GPIO.OUT)
        self.pwm = GPIO.PWM(self.motor_pin_pwm, 1000)

        GPIO.setup(self.motor_pin_direct, GPIO.OUT)
        logger.info('Set motor GPIO {} and {} to OUT'.format(
            self.motor_pin_pwm,
            self.motor_pin_direct))

        self.motor_direct = self.config['motor_direct']

    def is_water_full(self):
        result = self.water_pin_in
        logger.debug('Read water level pin value: {}'.format(result))

        if GPIO.input(result):
            return True
        else:
            return False

    def stop(self):
        self._stop = True

    def refill_water(self):
        GPIO.output(self.motor_pin_direct, self.motor_direct)

        try:
            self.pwm.start(50)

            while (not self.is_water_full() and not self._stop):
                logger.debug("water is not full")
                time.sleep(0.5)

            logger.info("water is full")
            self.pwm.stop()

        finally:
            GPIO.output(self.water_pin_out, False)

            GPIO.output(self.motor_pin_pwm, False)
            GPIO.output(self.motor_pin_direct, False)

            self._stop = False

    def cleanup(self):
        GPIO.cleanup()


if __name__ == "__main__":
    config = {
        "water_level_pin": [11, 12],
        "motor_pin": [13, 15],
        "motor_direct": False
    }

    refill = Refill(config)
    refill.refill_water()
