from nanomsg import Socket, REQ, REP, PUB, SUB, DONTWAIT, PAIR ,NanoMsgAPIError, EAGAIN, SUB_SUBSCRIBE
import time
from gevent import monkey

from gevent.socket import wait_read, wait_write
import gevent

print("REQ/REP Sample")
s1 = Socket(PAIR)
s2 = Socket(PAIR)

s1.bind('inproc://bob')
s2.connect('inproc://bob')

def consumer():
    for index in range(0, 10):
        print("Consumer gevent.socket.wait_read")
        wait_read(s1.recv_fd)
        print("Consumer gevent.socket.wait_read finished")
        req = s1.recv(flags=DONTWAIT)
        s1.send("{} pong {}".format(req, index))

def provider():
    for index in range(0, 10):
        print("Provider send ping...")
        req = s2.send("ping")
        print("Provider gevent.socket.wait_read")
        wait_read(s2.recv_fd)
        print("Provider gevent.socket.wait_read finished")
        rep = s2.recv(flags=DONTWAIT)
        print("Provider receive: {}".format(rep))

try:
    c = gevent.spawn(consumer)
    p = gevent.spawn(provider)

    print("Waiting consumer and provider...")
    gevent.joinall([c, p])
finally:
  s1.close()
  s2.close()




