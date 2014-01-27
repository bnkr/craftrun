import subprocess, logging

class ScreenSession(object):
    """Interface to the CLI of GNU Screen in order to manage a session which
    contains our server."""

    def __init__(self, name):
        self.name = name

    def start(self, args):
        pipe = self._screen(['-dm'] + args)
        if pipe.wait() != 0:
            raise Exception("screen failed to launch")

    def send(self, data):
        # TODO: wipe current line in case the user left something there
        pipe = self._screen(['-X', 'stuff', data + "\r\n"])
        if pipe.wait() != 0:
            raise Exception("screen failed")

    def is_running(self):
        pipe = self._pipe(['screen', '-list', self.name],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = pipe.communicate()

            for line in out.split("\n"):
                if self.name in line and "Detached" in line:
                    return True

            return False
        finally:
            pipe.wait()

    def _screen(self, args, **kw):
        return self._pipe(['screen', '-S', self.name] + args)

    def _pipe(self, args, **kw):
        logging.info("execute {0!r}".format(args))
        pipe = subprocess.Popen(args, **kw)
        return pipe
