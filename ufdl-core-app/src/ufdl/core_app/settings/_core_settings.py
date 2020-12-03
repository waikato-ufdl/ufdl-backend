"""
Defines the core settings for UFDL.
"""
from ufdl.json.core.jobs.notification import *

from ..backend.filesystem import FileSystemBackend
from ._UFDLClassSetting import UFDLClassSetting
from ._UFDLNotificationActionsSetting import UFDLNotificationActionsSetting
from ._UFDLSettings import UFDLSettings
from ._UFDLStringSetting import UFDLStringSetting


class UFDLCoreSettings(UFDLSettings):
    """
    The settings for the core UFDL app.
    """
    @classmethod
    def namespace(cls) -> str:
        return "UFDL"

    # ==================== #
    # File-System Settings #
    # ==================== #
    # The backend to use for storing files
    FILESYSTEM_BACKEND = UFDLClassSetting(
        default="ufdl.core_app.backend.filesystem.LocalDiskBackend",
        base=FileSystemBackend
    )

    # The directory to store files under when using a local-disk file-system backend
    LOCAL_DISK_FILE_DIRECTORY = UFDLStringSetting(default="./fs")

    # ===================== #
    # Notification Settings #
    # ===================== #
    # The default set of notifications to send when a workable job transitions
    DEFAULT_WORKABLE_NOTIFICATIONS = UFDLNotificationActionsSetting(
        default=NotificationActions(
            on_start=[
                PrintNotification(
                    message="Job #{pk} started",
                    suppress_for_parent=False
                ),
                EmailNotification(
                    subject="Job #{pk} started",
                    body="Job #{pk} has now been started by node #{node}\n"
                         "\n"
                         "Job description:\n"
                         "{description}\n"
                         "\n"
                         "Congrats! You received an email from the UFDL server!\n",
                    suppress_for_parent=False
                )
            ],
            on_finish=[
                PrintNotification(
                    message="Job #{pk} finished",
                    suppress_for_parent=False
                )
            ],
            on_error=[
                PrintNotification(
                    message="Job #{pk} finished with error:\n{error}",
                    suppress_for_parent=False
                )
            ]
        )
    )

    # The default set of notifications to send when a meta-job transitions
    DEFAULT_META_NOTIFICATIONS = UFDLNotificationActionsSetting(
        default=NotificationActions(
            on_start=[
                PrintNotification(
                    message="Job #{pk} started",
                    suppress_for_parent=False
                ),
                EmailNotification(
                    subject="Job #{pk} started",
                    body="Job #{pk} has now been started (triggered by a sub-job)\n"
                         "\n"
                         "Job description:\n"
                         "{description}\n"
                         "\n"
                         "Congrats! You received an email from the UFDL server!\n",
                    suppress_for_parent=False
                )
            ],
            on_finish=[
                PrintNotification(
                    message="Job #{pk} finished",
                    suppress_for_parent=False
                )
            ],
            on_error=[
                PrintNotification(
                    message="Job #{pk} finished with error:\n{error}",
                    suppress_for_parent=False
                )
            ]
        )
    )


# Create a singleton instance to export
core_settings: UFDLCoreSettings = UFDLCoreSettings()
