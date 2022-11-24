"""
Script to run the server.
"""
import sys


def run(argv=sys.argv):
    from daphne.cli import CommandLineInterface
    sys.exit(CommandLineInterface().run(["ufdl.api_site.asgi:application"] + argv[1:]))


if __name__ == '__main__':
    run()
