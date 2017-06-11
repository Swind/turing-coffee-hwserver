from utils.channel import Channel

class Publisher(object):

    def __init__(self):
        pass

    def pub(self, msg):
        raise NotImplementedError


class Subscriber(object):

    def __init__(self):
        pass

    def update(self):
        raise NotImplementedError

class NanomsgPublisher(Publisher):

    def __init__(self, addr):
        super(NanomsgPublisher, self)
        self.chan = Channel(addr, 'Pub', True)

    def pub(self, msg):
        self.chan.send(msg)


class NanomsgSubscriber(Subscriber):

    def __init__(self, addr):
        super(NanomsgSubscriber, self)
        self.chan = Channel(addr, 'Sub', False)

    def update(self):
        return self.chan.recv(blocking=False)

class SubscribeLooper(object):

    def __init__(self, interval=1):
        self._stop_flag = False
        self._subscribers = []
        self._new_subscribers = []
        self._interval = interval

        self._thread = Thread(target=self._update)
        self._thread.daemon = True
        self._thread.start()

    def __del__(self):
        self._stop_flag = True
        self._thread.join()
        self._subscribers = None
        self._new_subscribers = None

    def _update(self):
        while self._stop_flag is not True:
            self._subscribers.extend(self._new_subscribers)
            for sub in self._subscribers:
                sub.update()
            time.sleep(self._interval)

        self._stop_flag = False

    def sub(self, sub):
        if not isinstance(sub, Subscriber):
            return False
        self._new_subscribers.append(sub)
        return True

    def stop(self):
        self._stop_flag = True

