from typing import Any

from ._UFDLSetting import UFDLSetting


class UFDLBoolSetting(UFDLSetting):
    """
    Setting which takes a boolean value.
    """
    def _prepare(self, value: Any) -> Any:
        if not isinstance(value, bool):
            self._error(value, "Not a boolean")

        return value
