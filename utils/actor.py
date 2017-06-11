import gevent

import threading
import queue

class ActorExit(Exception):
    pass

class Actor:
    def __init__(self, greenlet=True):

        self.greenlet = greenlet

        if self.greenlet:
            self._mailbox = gevent.Queue()
            self._terminated = gevent.Event()
        else:
            self._mailbox = queue.Queue()
            self._terminated = threading.Event()

        self._thread = None

    def send(self, msg):
        '''
        Send a message to actor
        '''
        self._mailbox.put(msg)

    def recv(self, block=True, timeout=None):
        '''
        Receive an incoming message
        '''
        msg = self._mailbox.get(block=block, timeout=timeout)
        if msg is ActorExit:
            raise ActorExit

    def close(self):
        '''
        Close the actor, thus shutting it down
        '''
        self.send(ActorExit)

    def start(self):
        '''
        Start concurrent execution
        '''
        if self.greenlet:
            self._thread = gevent.spawn(self._bootstrap)
        else:
            self._thread = threading.Thread(target=self._bootstrap)
            self._thread.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        '''
        Run method to be implemented by the user
        '''
        while True:
            msg = self.recv()