"""
Script to run the server.
"""
import sys


def run(argv=sys.argv):
    from .manage import main
    script = argv[0].replace("run.py", "manage.py")
    main([script, "runserver"] + sys.argv[1:])


if __name__ == '__main__':
    run()
