import argparse, sys

class CraftRunCli(object):
    def run(self):
        parser = self.get_parser()
        parsed = parser.parse_args()
        return 0

    def get_parser(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='sub-command help')

        start = subparsers.add_parser('start')

        return parser

def main():
    """Cli entry point."""
    return CraftRunCli().run()
