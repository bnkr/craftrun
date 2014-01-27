import os, contextlib, subprocess, logging, time
from craftrun.screen import ScreenSession

class StartCommand(object):
    """Start the server."""
    name = "start"

    class Error(Exception):
        pass

    @classmethod
    def configure_cli(cls, parser):
        pass

    def __init__(self, settings):
        self.settings = settings
        self.screen = ScreenSession(name=settings.server_name)

    def run(self):
        if self.screen.is_running():
            why = "session {0!r} already running"
            logging.info(why.format(self.screen.name))
            return 0

        try:
            with self.in_dir(self.settings.base_dir):
                self._launch_server()
            return 0
        except self.Error as ex:
            logging.error(ex)
            return 1

    def _get_command(self, settings):
        java = [settings.java_bin] + settings.java_args
        server = ["-jar", settings.server_jar, 'nogui']
        return java + server

    def _launch_server(self):
        command = self._get_command(self.settings)
        self.screen.start(command)

        time.sleep(1)

        if not self.screen.is_running():
            raise self.Error("server did not start")

        logging.info("probably running")

    @contextlib.contextmanager
    def in_dir(self, path):
        restore_to = os.getcwd()
        try:
            logging.info("chdir {0!r}".format(path))
            os.chdir(path)
            yield
        finally:
            os.chdir(restore_to)

class StopCommand(object):
    """Stop the server if running."""
    name = "stop"

    @classmethod
    def configure_cli(cls, parser):
        pass

    def __init__(self, settings):
        self.settings = settings
        self.screen = ScreenSession(name=settings.server_name)

    def run(self):
        if not self.screen.is_running():
            logging.info("already stopped")
            return 0

        self.screen.send("stop")

        tries = 0
        max_tries = 5

        while self.screen.is_running() and tries < max_tries:
            time.sleep(0.5)

        if self.screen.is_running():
            logging.error("session did not stop")
            return 1

        logging.info("session has stopped")
        return 0
