#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main(argv=sys.argv):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufdl.api_site.settings')

    # If the command is reset, do that now
    if argv[1] == 'reset':
        from .reset import reset
        reset([argv[0].replace("manage.py", "reset.py")] + argv[1:])
        return

    # If the command is run, do that now
    if argv[1] == 'run':
        from .run import run
        run([argv[0].replace("manage.py", "run.py")] + argv[1:])
        return

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(argv)


if __name__ == '__main__':
    main()
