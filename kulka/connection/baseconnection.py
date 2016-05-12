from select import select
from kulka.connection import exceptions
from kulka.core.logger import debuglog


class BaseConnection(object):

    def __init__(self, sock):
        self._sock = sock

    @classmethod
    def connect(cls, addr, port=1):
        raise NotImplementedError()

    def fileno(self):
        return self._sock.fileno()

    def close(self):
        self._sock.close()

    @debuglog
    def send(self, data):
        retries = 10
        written = 0

        while retries > 0:
            _, wlist, _ = select([], [self._sock], [], 1)

            if wlist:
                written += wlist[0].send(data[written:])

                if written >= len(data):
                    return written
            else:
                retries -= 1

        raise exceptions.ConnectionLost()

    @debuglog
    def recv(self, num_bytes):
        retries = 10

        while retries > 0:
            rlist, _, _ = select([self._sock], [], [], 1)

            if rlist:
                return rlist[0].recv(num_bytes)
            else:
                retries -= 1

        raise exceptions.ConnectionLost()
