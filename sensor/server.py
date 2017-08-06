from utils.logger import get_logger
from sensor.temperature.max31856 import MAX31856 as Ttype
from sensor.temperature.max31865 import MAX31865 as Pt100

from utils.channel import ServerChannel

import gevent
import gevent.socket

logger = get_logger(__name__)


class SensorServer(object):
    def __init__(self, config):
        self.config = config
        self.interval = config.get("interval", 5)
        self.sensors = {}
        self.values = {}
        self.monitor = None

    def start(self):
        self._init_temperature_sensor()
        self._init_channel()
        self.monitor = gevent.spawn(self._monitor_all_sensors)

    def wait_cmd(self):
        while(True):
            gevent.socket.wait_read(self.channel.cmd.recv_fd)
            cmd = self.channel.cmd.recv()
            logger.info("Receive command: {}".format(cmd))
            gevent.sleep(5)


    def _monitor_all_sensors(self):
        while(True):
            for name, sensor in self.sensors.items():
                value = sensor.read()
                logger.debug("Sensor {} => Value: {}".format(name, value))
                self.values[name] = value

            self.channel.publish.send(self.values)
            gevent.sleep(self.interval)

    def _init_temperature_sensor(self):
        temperature = self.config.get('temperature', {})

        logger.info("Initialize temperature sensors...")

        for name, config in temperature.items():
            sensor_type = config.get('type')
            if sensor_type is None:
                raise RuntimeError("Please select a sensor type in the {}".format(name))

            logger.info("Create temperature sensor {}".format(name))
            logger.info("By config {}".format(config))
            fn = getattr(self, '_{}'.format(sensor_type), None)

            try:
                self.sensors[name] = (fn(config))
                self.values[name] = None
            except KeyError as ke:
                logger.error("Failed to initialize sensor {}".format(name))
                logger.error(ke)

    def _init_channel(self):
        channel_config = self.config.get('channel', None)
        if not channel_config:
            logger.info("There is no channel config in the sensor server...")

        logger.info("Create channel {}".format(channel_config))
        self.channel = ServerChannel(channel_config)

    def _max31856(self, config):
        new_sensor = Ttype(config['ce'])
        new_sensor.open()
        return new_sensor

    def _max31865(self, config):
        new_sensor = Pt100(
            csPin=config['cs'],
            misoPin=config['miso'],
            mosiPin=config['mosi'],
            clkPin=config['clk']
        )
        new_sensor.open()

        return new_sensor

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)


    import yaml
    config = yaml.load("""
    temperature:
        tank:
          name: tank
          type: max31865
          cs: 29
          miso: 33
          mosi: 31
          clk: 35

        output:
          name: output
          type: max31856
          ce: 0

    channel:
        publish: ipc:///tmp/sensor_pub_channel
        command: ipc:///tmp/sensor_cmd_channel
    """)
    logger.info("Sensor Config:")
    logger.info(config)
    sensor_server = SensorServer(config)
    sensor_server.start()
    sensor_server.wait_cmd()
