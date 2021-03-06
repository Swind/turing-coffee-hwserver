#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reqrep import Requester, Responser
from utils.channel import Channel


class NanomsgResponser(Responser):

    def __init__(self, addr):
        super(NanomsgResponser, self)
        self._chan = Channel(addr, 'Pair', True)

    def rep(self, msg):
        raise NotImplementedError

    def recv(self):
        return self._chan.recv()


class NanomsgRequester(Requester):

    def __init__(self, addr):
        super(NanomsgRequester, self)
        self._chan = Channel(addr, 'Pair', False)

    def req(self, msg):
        return self._chan.send(msg)

    def recv(self):
        return self._chan.recv()
