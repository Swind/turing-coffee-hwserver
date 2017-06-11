from utils.logger import get_logger
from sensor.temperature.max31856 import MAX31856 as Ttype
from sensor.temperature.max31865 import MAX31865 as Pt100

logger = get_logger(__name__)


class SensorServer(object):
    def __init__(self, config):
        self.config = config
        self.sensors = []

    def _init_temperature_sensor(self):
        temperature = self.config.get('temperature', {})

        logger.info("Initialize temperature sensors...")

        for name, config in temperature.items():
            sensor_type = config.get('type')
            if sensor_type is None:
                raise RuntimeError("Please select a sensor type in the {}".format(name))

            logger.info("Create temperature sensor {}".format(name))
            fn = getattr(self, '_{}'.format(sensor_type), None)

            try:
                self.sensors.append(fn(config))
            except KeyError as ke:
                logger.error("Failed to initialize sensor {}".format(name))
                logger.error(ke)

    def _max31865(self, config):
        new_sensor = Ttype(config['ce'])
        return new_sensor

    def _max31856(self, config):
        new_sensor = Pt100(
            csPin=config['cs'],
            misoPin=config['miso'],
            mosiPin=config['mosi'],
            clkPin=config['clk']
        )

        return new_sensor
