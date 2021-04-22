"""
Script to run the server.
"""


def run():
    import sys
    from .manage import main
    script = sys.argv[0].replace("reset.py", "manage.py")
    main([script, "runserver"] + sys.argv[1:])


if __name__ == '__main__':
    run()
