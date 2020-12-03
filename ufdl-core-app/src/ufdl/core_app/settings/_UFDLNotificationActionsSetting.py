from typing import Any

from ufdl.json.core.jobs.notification import NotificationActions

from ._UFDLSetting import UFDLSetting


class UFDLNotificationActionsSetting(UFDLSetting):
    """
    Setting type which expects a string as its value.
    """
    def _prepare(self, value: Any) -> Any:
        # Attempt to parse the value
        prepared_value = (
            NotificationActions.from_json_string(value)
            if isinstance(value, str)
            else NotificationActions.from_raw_json(value)
            if isinstance(value, dict)
            else value
        )

        # Must be a NotificationActions
        if not isinstance(prepared_value, NotificationActions):
            self._error(value, f"Not a {NotificationActions.__qualname__}")

        return value
