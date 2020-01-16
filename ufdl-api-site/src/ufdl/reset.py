"""
Script to delete and re-create the database.
"""
# Remove the database
DB_PATH = "ufdl-api-site/src/ufdl/db.sqlite3"
import os
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Remove the file-system
FS_PATH = "fs"
import shutil
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
