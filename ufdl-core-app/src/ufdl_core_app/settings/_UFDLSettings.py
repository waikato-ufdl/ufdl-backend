from ..backend.filesystem import FileSystemBackend
from .validators import IS_SUBCLASS_OF
from ._UFDLSetting import UFDLSetting
from ._UFDLClassSetting import UFDLClassSetting


class UFDLSettings:
    """
    Class representing all of the available settings for the UFDL.
    """
    # ==================== #
    # File-System Settings #
    # ==================== #
    # The backend to use for storing files
    FILESYSTEM_BACKEND = UFDLClassSetting(default="ufdl_core_app.backend.filesystem.LocalDiskBackend",
                                          validator=IS_SUBCLASS_OF(FileSystemBackend))

    # The directory to store files under when using a local-disk file-system backend
    LOCAL_DISK_FILE_DIRECTORY = UFDLSetting(default="./fs")


# Create a singleton instance to export
ufdl_settings: UFDLSettings = UFDLSettings()
