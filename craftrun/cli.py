import argparse, sys
from craftrun.command import StartCommand

class CraftRunCli(object):
    """
    Creates commands and runs them with apropriate settings.
    """
    def __init__(self):
        self.commands = [
            StartCommand(),
        ]

    def run(self):
        parser = self.get_parser()
        parsed = parser.parse_args()

        selected = next((command for command in self.commands
                         if command.name == parsed.command))

        return selected.run(parsed)

    def get_parser(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='sub-command help', dest="command")

        for command in self.commands:
            subparser = subparsers.add_parser(command.name)
            command.configure_cli(subparser)

        return parser

def main():
    """Cli entry point."""
    return CraftRunCli().run()
