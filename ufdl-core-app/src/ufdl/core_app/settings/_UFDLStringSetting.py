from typing import Any

from ._UFDLSetting import UFDLSetting


class UFDLStringSetting(UFDLSetting):
    """
    Setting type which expects a string as its value.
    """
    def _prepare(self, value: Any) -> Any:
        # Must be a string
        if not isinstance(value, str):
            self._error(value, f"Not a string")

        return value
