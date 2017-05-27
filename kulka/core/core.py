from kulka import request
from kulka.connection.exceptions import ConnectionLost
from kulka.connection import Connection
from kulka.response import parser

class Kulka(object):

    def __init__(self, addr):
        self._addr = addr
        self._connection = Connection.connect(addr)
        self._sequence = 0
        self._recv_buffer = bytearray()
        self._data = []

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def close(self):
        self._connection.close()

    def sequence(self):
        self._sequence = (self._sequence + 1) & 0xFF
        return self._sequence

    def data_stream(self):
        return self._data.pop()

    def _send(self, request_):
        request_.sequence = self.sequence()
        try:
            self._connection.send(request_.tobytes())
            self._wait_for_ack(request_.sequence)
        except ConnectionLost:
            self._reconnect()

    def _wait_for_ack(self, sequence):
        while True:
            try:
                response, consumed = parser(self._recv_buffer)
                self._recv_buffer = self._recv_buffer[consumed:]
                self._data.append(response)
                if getattr(response, 'seq', None) == sequence:
                    break
            except ValueError:
                self._recv_buffer.extend(self._connection.recv(1024))

    def _reconnect(self):
        self._connection.close()
        self._connection = Connection.connect(self._addr)

    def set_inactivity_timeout(self, timeout):
        return self._send(request.SetInactivityTimeout(timeout))

    def set_rgb(self, red, green, blue, flag=0):
        return self._send(request.SetRGB(red, green, blue, flag))

    def roll(self, speed=0, heading=0, state=1):
        return self._send(request.Roll(speed, heading, state))

    def set_back_led(self, bright):
        return self._send(request.SetBackLed(bright))

    def set_heading(self, heading):
        return self._send(request.SetHeading(heading))

    def sleep(self, wakeup=0, macro=0, orb_basic=0):
        return self._send(request.Sleep(wakeup, macro, orb_basic))

    def read_locator(self):
        return self._send(request.ReadLocator())
