import argparse, sys, yaml, os, logging
from craftrun import command

class Settings(object):
    """Cli and config file settings."""
    def __init__(self, cli):
        self.cli = cli

        with open(cli.config, 'r') as io:
            self.config = yaml.load(io.read())

    @property
    def base_dir(self):
        return self._absolute_path(self.config['base_dir'])

    @property
    def backup_dir(self):
        return self._absolute_path(self.config['backup_dir'])

    @property
    def server_name(self):
        return self.config['server_name']

    @property
    def java_bin(self):
        command = self.config.get('java_bin', 'java')
        if '/' in command:
            return self._absolute_path(command)
        else:
            return command

    @property
    def server_jar(self):
        return self.config['server_jar']

    @property
    def java_args(self):
        default_args = ['-Xmx2G', '-XX:MaxPermSize=256M']
        return self.config.get('java_args', default_args)

    def _absolute_path(self, path):
        config_dir = os.path.dirname(self.cli.config)
        return os.path.realpath(os.path.join(config_dir, path))

class CraftRunCli(object):
    """
    Creates commands and runs them with apropriate settings.
    """
    def __init__(self):
        self.commands = [
            command.StartCommand,
            command.StopCommand,
            command.ConsoleCommand,
            command.TailCommand,
            command.BackupCommand,
        ]

    def run(self):
        parser = self.get_parser()
        parser.add_argument("-v", "--verbose", action='store_true',
                            help="Show informational messages.")
        parser.add_argument("-d", "--debug", action='store_true',
                            help="Show debugging messages.")
        parser.add_argument("-c", "--config", dest="config", required=True,
                            help="Server configuration.")
        parsed = parser.parse_args()

        if parsed.debug:
            level = logging.DEBUG
        elif parsed.verbose:
            level = logging.INFO
        else:
            level = logging.WARNING

        logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                            level=level,)

        selected = next((command for command in self.commands
                         if command.name == parsed.command))

        config = Settings(cli=parsed)

        return selected(config).run()

    def get_parser(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='operation', dest="command")

        for command in self.commands:
            subparser = subparsers.add_parser(command.name, help=command.help)
            command.configure_cli(subparser)

        return parser

def main():
    """Cli entry point."""
    return CraftRunCli().run()
