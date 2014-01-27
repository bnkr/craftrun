import os, contextlib, subprocess, logging, time, sys
from datetime import datetime as DateTime
from craftrun.screen import ScreenSession

@contextlib.contextmanager
def in_dir(path):
    restore_to = os.getcwd()
    try:
        logging.info("chdir {0!r}".format(path))
        os.chdir(path)
        yield
    finally:
        os.chdir(restore_to)

class StartCommand(object):
    """Start the server."""
    name = "start"
    help = "Start a single instance of the server."

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
            with in_dir(self.settings.base_dir):
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

        # TODO:
        #   We could use a hardcopy and grep it?
        logging.info("probably running")

class StopCommand(object):
    """Stop the server if running."""
    name = "stop"
    help = "Stop server if running."

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

class ConsoleCommand(object):
    """Join the screen session."""
    name = "console"
    help = "Press C a-d to detach again."

    @classmethod
    def configure_cli(cls, parser):
        pass

    def __init__(self, settings):
        self.screen = ScreenSession(name=settings.server_name)

    def run(self):
        if not sys.stdin.isatty():
            logging.error("won't join wile not on a tty")
            return 1
        self.screen.join()
        return 0

class BackupCommand(object):
    """Generate a backup tarball.  If it's just the worlds, then you still
    extract the tarball in the base dir."""
    name = "backup"
    help = "Press C a-d to detach again."

    @classmethod
    def configure_cli(cls, parser):
        parser.add_argument("-w", "--world-only", action='store_true',
                            help="Only back up worlds.")
        parser.add_argument("-T", "--flush-wait-time", type=int, default=10,
                            help='Seconds to wait for the world to be saved.')

    def __init__(self, settings):
        self.settings = settings
        self.screen = ScreenSession(name=settings.server_name)
        self._is_running = None

    @property
    def is_running(self):
        if self._is_running is None:
            self._is_running = self.screen.is_running()
        return self._is_running

    @property
    def flush_time(self):
        return self.settings.cli.flush_wait_time

    @property
    def backup_type(self):
        return self.settings.cli.world_only and "world" or "full"

    def run(self):
        output = self._get_output_path()
        target = self._get_backup_target()

        if not self.is_running:
            logging.info("server is not running")

        with self._in_dir_above_server():
            try:
                self._say("{0} backup of {1} starting".format(
                    self.backup_type, self.settings.server_name))
                self._set_saving(enabled=False)
                self._flush_worlds()
                self._tarball(output, target)
                self._say("backup finished")
            except:
                self._say("backup failed")
                logging.error("exception during backup")
                raise
            finally:
                self._set_saving(enabled=True)

        return 0

    def _say(self, text):
        if self.is_running:
            self.screen.send("say {0}".format(text))

    @contextlib.contextmanager
    def _in_dir_above_server(self):
        path = os.path.dirname(self.settings.base_dir)
        with in_dir(path):
            yield

    def _tarball(self, output, backup):
        logging.info("making tarball from {0}".format(backup))
        command = ['tar', 'cjf', output, backup]
        logging.debug("execute {0!r}".format(command))
        pipe = subprocess.Popen(command)
        if pipe.wait() != 0:
            raise Exception("tar failed")

    def _flush_worlds(self):
        if self.is_running:
            logging.info("flushing data")
            self.screen.send('save-all')
            logging.info("waiting {0}s for flush".format(self.flush_time))
            time.sleep(self.flush_time)

    def _set_saving(self, enabled):
        if not self.is_running:
            return

        command = enabled and "on" or "off"
        logging.info("turning saving {0}".format(command))
        self.screen.send('save-{0}'.format(command))

    def _get_backup_target(self):
        server = os.path.basename(self.settings.base_dir)
        if self.settings.cli.world_only:
            return os.path.join(server, "world")
        else:
            return server

    def _get_output_path(self):
        output_name = DateTime.now().strftime("%Y-%m-%d.%H-%M-%S")
        full_name = "{0}-{1}-{2}.tar.bz2".format(
                self.settings.server_name, self.backup_type, output_name)
        output = os.path.join(self.settings.backup_dir, full_name)
        if os.path.exists(output):
            raise Exception("refusing to overwrite backup")

        return output
