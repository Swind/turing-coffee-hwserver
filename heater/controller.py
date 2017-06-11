from utils.logger import get_logger
from utils.actor import Actor

from sensor.temperature import TemperatureSensor
from heater.device import Heater
from heater.pid import PID

import time
from typing import Callable

logger = get_logger(__name__)


class PIDActor(Actor):
    def __init__(self,
                 cycle_time: float,
                 pid: PID,
                 sensor: TemperatureSensor,
                 heater: Heater,
                 observer: Callable[[float, float, float, float], None],
                 set_point: float):

        logger.info("Starting PID actor...")
        super(Actor, self).__init__()

        self._pid = pid

        self._cycle_time = cycle_time
        self._set_point = set_point

        self._sensor = sensor
        self._heater = heater
        self._observer = observer

        logger.info("PID actor is started...")

    def _set_point(self, point):
        self._set_point = point

    def _set_pid_params(self, k_param, i_param, d_param):
        self._pid.set_params(self._cycle_time, k_param, i_param, d_param)

    def _set_cycle_time(self, cycle_time):
        self._cycle_time = cycle_time
        self._pid.set_params(cycle_time, self._pid.kc, self._pid.ti, self._pid.td)

    def _heat(self):
        # Get the average of all sensors
        try:
            temperature = self._sensor.read()
            logger.debug('Heater -> temperature: {}, set_point: {}'.format(temperature, self._set_point))

            if (self._set_point - 5) < temperature < self._set_point:
                duty_cycle = self._pid.calcPID_reg4(
                    temperature,
                    self._set_point,
                    True)

            elif temperature >= self._set_point:
                duty_cycle = 0
            else:
                duty_cycle = 100


            self._heater.heat(self._cycle_time, duty_cycle)

            # notify the observer
            self._observer(self._cycle_time, duty_cycle, self._set_point, temperature)
        except:
            logger.warning("Tank Sensor seems broken, restart it")
            self._sensor.close()
            time.sleep(0.2)
            self._sensor.open()

    def run(self):
        while (True):
            func, *params = self.recv(block=False)
            if func and params:
                logger.debug("Execute function {} with parameters {}".format(func, params))
                getattr(self, func)(*params)

            self._heat()
