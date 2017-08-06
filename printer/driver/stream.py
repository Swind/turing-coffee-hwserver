import serial
from retrying import retry
import gevent
import gevent.socket

class Stream:
    def __init__(self, port, baudrate, timeout=1, write_timeout=1):
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._write_timeout = write_timeout

        self._serial = None

    def open(self):
        self._serial = serial.Serial(str(self._port), self._baudrate, timeout=1, writeTimeout=1)

    def read(self):
        gevent.socket.wait_read(self._serial.fd)
        result = self._serial.readline()

        if result == '':
            ret_str = ''
        else:
            ret_str = result.decode('ascii').strip()

        return ret_str

    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    def write(self, cmd):
        cmd = cmd + '\n'
        self._serial.write(cmd)

        return True


    def close(self):
        self._serial.close()