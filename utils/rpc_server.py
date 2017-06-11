from utils import channel
from utils import Actor

class DummyChannel:
    def __init__(self):
        pass

    def recv(self):
        return None

    def send(self, *argv, **kwargv):
        pass

class RPCServer:
    def __init__(self, server_id, cmd_addr=None, pub_addr=None):
        self.server_id = server_id

        if cmd_addr:
            self._cmd_chan = channel.Channel(cmd_addr, 'Pair', True)
        else:
            self._cmd_chan = DummyChannel()

        if pub_addr:
            self._pub_chan = channel.Channel(pub_addr, 'Pub', True)
        else:
            self._pub_chan = DummyChannel()

    def pub(self, data):
        self._pub_chan.send(
            {
                'id': self.server_id,
                'data': data
            }
        )


    def start(self):
        while True:
            cmd = self._cmd_chan.recv()


        pass

