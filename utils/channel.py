import json

from nanomsg import (
    PUB,
    SUB,
    SUB_SUBSCRIBE,
    PAIR,
    DONTWAIT,
    Socket,
    NanoMsgAPIError,
    EAGAIN
)

import gevent

class ServerChannel(object):
    def __init__(self, config):
        pub_addr = config['publish']
        cmd_addr = config['command']

        print(pub_addr)
        self.publish = Channel(pub_addr, 'Pub', True)

        print(cmd_addr)
        self.cmd = Channel(cmd_addr, 'Pair', True)


class Channel(object):

    type_map = {
        'Sub': SUB,
        'Pub': PUB,
        'Pair': PAIR
    }

    def __init__(self, address, channel_type, is_server):
        self.__socket = Socket(self.type_map[channel_type])

        if is_server:
            self.__socket.bind(address)
        else:
            self.__socket.connect(address)

            if channel_type == 'Sub':
                self.__socket.set_string_option(SUB, SUB_SUBSCRIBE, '')

        if channel_type == 'Sub' or channel_type == 'Pair':
            self.recv_fd = self.__socket.recv_fd
        else:
            self.recv_fd = None

    def recv(self, blocking=True):

        if blocking:
            gevent.socket.wait_read(self.__socket.recv_fd)
            result = self.__socket.recv(flags=DONTWAIT)
        else:
            try:
                result = self.__socket.recv(flags=DONTWAIT)
            except NanoMsgAPIError as error:
                if error.errno == EAGAIN:
                    return None

        return json.loads(result)

    def send(self, msg):
        return self.__socket.send(json.dumps(msg))

    def close(self):
        self.__socket.close()
