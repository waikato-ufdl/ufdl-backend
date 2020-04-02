"""
Script to delete and re-create the database.
"""
# Remove the database
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Remove the file-system
import shutil
from ufdl.core_app.settings import ufdl_settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufdl.api_site.settings')
FS_PATH = ufdl_settings.LOCAL_DISK_FILE_DIRECTORY
if os.path.exists(FS_PATH):
    shutil.rmtree(FS_PATH)

# Apply the migrations to recreate the database
from ufdl.manage import main
import sys
script = sys.argv[0].replace("reset.py", "manage.py")
main([script, "migrate"])

# Create the test superuser
from ufdl.core_app.models import User
User.objects.create_superuser("admin", "admin@admin.net", "admin")

# Run the server if the option is given
if len(sys.argv) >= 2 and sys.argv[1] == "--run":
    main([script, "runserver"])
