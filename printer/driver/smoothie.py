import logging
import serial

from printer.driver.stream import Stream

from retrying import retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Smoothie(object):

    def __init__(self, port=None, baudrate=None):
        self._stream = Stream(port=port, baudrate=baudrate)

    def __del__(self):
        if self._serial is not None:
            self._serial.close()

    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    def open(self):
        steps = ['Smoothie', 'ok']

        logger.info("Open serial '{}' with baudrate '{}'".format(self._port, self._baudrate))
        self._serial = serial.Serial(str(self._port), self._baudrate, timeout=1, writeTimeout=1)

        for index, step in enumerate(steps):
            line = self.readline().strip()
            if line != step:
                self._serial.close()
                raise RuntimeError("The {} message should be '{}', but received msg is {}, open the serial again to reset the status")

        # Use G command to check it is alive or note
        self.write('G')
        if self.readline().strip() == 'ok':
            return True

    def close(self):
        self._serial.close()

    def write(self, cmd):
        self._stream.write(cmd)

    def readline(self):
        return self._stream.read()

if __name__ == "__main__":
    smooth = Smoothie("/dev/ttyACM1", 115200)
    print(smooth.open())
    try:
        while(True):
            cmd = input(">")
            if(cmd=="exit"):
                break;
        smooth.write(cmd)
        print(smooth.readline())
    finally:
        smooth.close()
