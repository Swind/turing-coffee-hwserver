from queue import Queue
from threading import Thread, Event

class ActorExit(Exception):
    pass

class Actor:
    def __init__(self):
        self._mailbox = Queue()


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
        self._terminated = Event()
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()

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