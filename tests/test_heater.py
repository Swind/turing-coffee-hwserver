import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print("Append path {}".format(dir_path))
sys.path.append(dir_path)
print("PYTHONPATH: {}".format(sys.path))

from heater import server

def test_server():
    pass