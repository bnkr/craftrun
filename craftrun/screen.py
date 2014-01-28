import subprocess, logging, pty

class ScreenSession(object):
    """Interface to the CLI of GNU Screen in order to manage a session which
    contains our server."""

    def __init__(self, name):
        self.name = name

    def start(self, args):
        # TODO:
        #   Would be nice to get the log if the session ends abruptly.
        #   Otherwise it's hard to know that the command was ok or some other
        #   problem...
        (master, slave) = pty.openpty()
        pipe = self._screen(['-dm'] + args, stdout=slave,
                            stdin=slave, stderr=slave)
        if pipe.wait() != 0:
            raise Exception("screen failed to launch")

    def join(self):
        """Although this is designed for fooling processes (like su) to read
        from stdin when it's not a tty, it seems to work OK to avoid pty
        ownership issues."""
        pty.spawn(['screen', '-r', self.name])

    def send(self, data):
        # TODO: wipe current line in case the user left something there
        pipe = self._screen(['-X', 'stuff', data + "\n"])
        if pipe.wait() != 0:
            raise Exception("screen failed")

    def is_running(self):
        pipe = self._pipe(['screen', '-list', self.name],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = pipe.communicate()

            for line in out.split("\n"):
                if self.name in line:
                    return True

            return False
        finally:
            pipe.wait()

    def _screen(self, args, **kw):
        return self._pipe(['screen', '-S', self.name] + args)

    def _pipe(self, args, **kw):
        logging.debug("execute {0!r}".format(args))
        pipe = subprocess.Popen(args, **kw)
        return pipe
