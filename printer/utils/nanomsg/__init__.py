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


class Requester(object):
    def __init__(self):
        pass

    def req(self, msg):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError


class Responser(object):
    def __init__(self):
        pass

    def rep(self, msg):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError
