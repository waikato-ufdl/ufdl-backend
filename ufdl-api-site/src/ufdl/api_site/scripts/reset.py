"""
Script to delete and re-create the database.
"""


def reset():
    # Make sure we have access to settings
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufdl.api_site.settings')

    # Remove the database
    from ..settings import gen_database_name
    DB_PATH = gen_database_name()
    if os.path.exists(DB_PATH):
        print(f"Deleting database '{DB_PATH}'")
        os.remove(DB_PATH)
    else:
        print(f"Database '{DB_PATH}' not present; skipping deletion...")

    # Remove the file-system
    import shutil
    from ufdl.core_app.settings import ufdl_settings
    FS_PATH = ufdl_settings.LOCAL_DISK_FILE_DIRECTORY
    if os.path.exists(FS_PATH):
        print(f"Deleting filesystem '{FS_PATH}'")
        shutil.rmtree(FS_PATH)
    else:
        print(f"Filesystem '{FS_PATH}' not present; skipping deletion...")

    # Apply the migrations to recreate the database
    import sys
    from .manage import main
    script = sys.argv[0].replace("reset.py", "manage.py")
    main([script, "migrate"])

    # Create the test superuser
    from ufdl.core_app.models import User
    User.objects.create_superuser("admin", "admin@admin.net", "admin")

    # Run the server if the option is given
    if len(sys.argv) >= 2 and sys.argv[1] == "--run":
        main([script, "runserver"])


if __name__ == '__main__':
    reset()
