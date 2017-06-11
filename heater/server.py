from heater.controller import PIDActor
from heater.pid import PID
from heater.device import Heater

from sensor.temperature.max31865 import MAX31865

from utils import channel

import logging

logger = logging.getLogger(__name__)


class HeaterServer(object):
    def __init__(self, config):
        self.config = config

        self.pid = None
        self.actor = None

        self.pub_channel = None
        self.cmd_channel = None

    def start(self):
        logger.info("Heater server is starting ...")

        logger.info("Initialize pid ...")
        self.pid = self._init_pid()

        logger.info("Initialize channel ...")
        self.pub_channel, self.cmd_channel = self._init_channel()

        logger.info("Initialize actor ...")
        self._init_actor()

        logger.info("Heater server start successfully...")

        # The main thread will receive and set the pid parameters by nanomsg
        self.receive()

    def _init_pid(self):
        # Init PID
        pid_config = self.config['pid']
        pid = PID(
            pid_config['cycle time'],
            pid_config['k'],
            pid_config['i'],
            pid_config['d']
        )

        return pid

    def _init_channel(self):
        # That other process can subscribe the pid controller status
        channel_config = self.config['channel']
        pub_channel_addr = channel_config['publish']
        logger.info("Open heater server publish channel at {}".format(pub_channel_addr))
        pub_channel = channel.Channel(pub_channel_addr, 'Pub', True)

        # Receive the pid controller command
        cmd_channel_addr = channel_config['command']
        logger.info("Open heater server command channel at {}".format(cmd_channel_addr))
        cmd_channel = channel.Channel(cmd_channel_addr, 'Pair', True)

        return pub_channel, cmd_channel

    def _init_heater(self):
        pin_number = self.config['heater pin']
        logger.info("Initialize heater: pin {}".format(pin_number))
        heater = Heater(pin_number)
        return heater

    def _init_actor(self, pid, sensor, heater, callback):
        config = self.config['']
        pass

    # ============================================================================================================
    #
    #   nanomsg API
    #
    # ============================================================================================================
    def publish_pid_status(self, cycle_time, duty_cycle, set_point, temperature):
        """
        Publish pid status:
        e.g

        {
            "cycle_time": 5,
            "duty_cycle": 70,
            "set_point": 80,
            "temperature": 26.53
        }
        """
        # print "Publish cycle_time:{}, duty_cycle:{},
        # set_point:{}".format(cycle_time, duty_cycle, set_point, temperature)
        self.pub_channel.send({
                'cycle_time': cycle_time,
                'duty_cycle': duty_cycle,
                'set_point': set_point,
                'temperature': temperature
            })

    def receive(self):
        """
        Receive pid parameters:
        e.g
        {
            "cycle_time": 1,
            "k": 44,
            "i": 165,
            "d": 4,
            "set_point": 80
        }
        """
        # The main thread will handle the command socket
        while (True):
            cmd = self.cmd_channel.recv()
            self.pid_controller.set_params(
                cmd['cycle_time'],
                cmd['k'],
                cmd['i'],
                cmd['d'],
                cmd['set_point'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = HeaterServer()
    server.start()

