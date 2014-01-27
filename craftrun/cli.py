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
    def server_name(self):
        return self.config['server_name']

    @property
    def java_bin(self):
        return self.config.get('java_bin', 'java')

    @property
    def server_jar(self):
        return self.config['server_jar']

    @property
    def java_args(self):
        default_args = ['-Xmx2G', '-XX:MaxPermSize=256M']
        return self.config.get('java_args', default_args)

    def _absolute_path(self, path):
        config_dir = os.path.dirname(self.cli.config)
        return os.path.join(config_dir, path)

class CraftRunCli(object):
    """
    Creates commands and runs them with apropriate settings.
    """
    def __init__(self):
        self.commands = [
            command.StartCommand,
            command.StopCommand,
            command.ConsoleCommand,
        ]

    def run(self):
        parser = self.get_parser()
        parser.add_argument("-c", "--config", dest="config")
        parsed = parser.parse_args()

        logging.basicConfig(level=logging.INFO)

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
