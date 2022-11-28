"""
Script to run the server.
"""
import sys


def run(argv=sys.argv):
    # Check if we need to reset the database first
    import os
    should_reset = os.environ.get('UFDL_RESET_BACKEND_ON_RUN', 'false').upper()
    if should_reset in ('1', 'YES', 'Y', 'TRUE'):
        from .reset import reset
        script = argv[0].replace("run.py", "reset.py")
        reset([script])

    from daphne.cli import CommandLineInterface
    sys.exit(CommandLineInterface().run(["ufdl.api_site.asgi:application"] + argv[1:]))


if __name__ == '__main__':
    run()
