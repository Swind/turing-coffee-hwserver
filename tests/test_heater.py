import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print("Append path {}".format(dir_path))
sys.path.append(dir_path)
print("PYTHONPATH: {}".format(sys.path))

from heater.server import HeaterServer
import gevent

def test_server():
    config = {
        "pid": {
            "cycle time": 1,
            "k": 70,
            "i": 165,
            "d": 16
        },

        "channel": {
            "publish": "ipc:///tmp/heater_pub_channel",
            "command": "ipc:///tmp/heater_cmd_channel"
        },

        "heater pin": 7
    }
    server = HeaterServer(config)
    server.start()
    gevent.sleep(5)
    server.stop()
    pass