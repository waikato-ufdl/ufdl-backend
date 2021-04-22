"""
Script to delete and re-create the database.
"""
import sys


def reset(argv=sys.argv):
    # Make sure we have access to settings
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufdl.api_site.settings')

    # Reset the database
    from django.db import connections, DEFAULT_DB_ALIAS
    print(f"Resetting database")
    connection = connections[DEFAULT_DB_ALIAS]
    database_type = connection.vendor
    print(f"Detected database type: {database_type}")
    if database_type == "sqlite":
        DB_PATH = connection.settings_dict['NAME']
        if os.path.exists(DB_PATH):
            print(f"Deleting database '{DB_PATH}'")
            os.remove(DB_PATH)
        else:
            print(f"Database '{DB_PATH}' not present; skipping deletion...")
    elif database_type == "mysql":
        with connection.cursor() as cursor:
            cursor.execute("select database();")
            database_name = cursor.fetchone()[0]
            cursor.execute(f"drop database `{database_name}`;"
                           f"create database `{database_name}` character set utf8;"
                           f"use `{database_name}`;")
    elif database_type == "postgresql":
        with connection.cursor() as cursor:
            cursor.execute(f"select tablename from pg_catalog.pg_tables "
                           f"where tableowner = '{connection.settings_dict['USER']}';")
            next = cursor.fetchone()
            tables = []
            while next is not None:
                tables.append(next[0])
                next = cursor.fetchone()
            for table in tables:
                cursor.execute(f"drop table \"{table}\" cascade;")
    else:
        raise Exception(f"Can't reset database type: {database_type}")

    # Remove the file-system
    import shutil
    from ufdl.core_app.settings import core_settings
    FS_PATH = core_settings.LOCAL_DISK_FILE_DIRECTORY
    if os.path.exists(FS_PATH):
        print(f"Deleting filesystem '{FS_PATH}'")
        shutil.rmtree(FS_PATH, ignore_errors=True)
    else:
        print(f"Filesystem '{FS_PATH}' not present; skipping deletion...")

    # Apply the migrations to recreate the database
    from .manage import main
    script = argv[0].replace("reset.py", "manage.py")
    main([script, "migrate"])

    # Create the test superuser
    from ufdl.core_app.models import User
    User.objects.create_superuser("admin", "admin@admin.net", "admin")

    # Run the server if the option is given
    if len(argv) >= 2 and argv[1] == "--run":
        main([script, "runserver"])


if __name__ == '__main__':
    reset()
