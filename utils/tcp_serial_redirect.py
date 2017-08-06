import serial

import gevent
import gevent.socket
from gevent.server import StreamServer


class RedirectServer:
    def __init__(self, host, port, serial_url, baudrate):

        self.serial_url = serial_url
        self.baudrate = baudrate

        self._server = StreamServer((host, port), self.stream_server_handler)
        self._server.max_accept = 1

    def serial_socket_reader(self, serial_socket: serial.Serial, tcp_socket):
        while True:
            gevent.socket.wait_read(serial_socket.fd)
            result = serial_socket.readall()
            tcp_socket.sendall(result)

    def stream_server_handler(self, socket, address):
        print('New connection from %s:%s' % address)

        serial_socket = None

        try:
            serial_socket = serial.Serial(self.serial_url,
                                         self.baudrate,
                                         timeout=1,
                                         writeTimeout=1)
            reader_sapwn = gevent.spawn(self.serial_socket_reader, serial_socket, socket)

            # using a makefile because we want to use readline()
            rfileobj = socket.makefile(mode='rb')

            while True:
                line = rfileobj.readline()

                if not line:
                    print("client disconnected")
                    break

                serial_socket.write(line)

            rfileobj.close()
        finally:
            if serial_socket:
                serial_socket.close()

if __name__ == "__main__":
    redirect_server = RedirectServer('localhost', 9000, '/dev/tty03')
    pass
