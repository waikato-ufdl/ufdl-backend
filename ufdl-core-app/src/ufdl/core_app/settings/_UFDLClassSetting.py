from typing import Union, Any

from django.utils.module_loading import import_string

from ._UFDLSetting import UFDLSetting


class UFDLClassSetting(UFDLSetting):
    """
    Setting type which expects a class as its value.
    """
    def __init__(self, default: Union[str, type], base: type):
        super().__init__(default)
        self._base = base

    def _prepare(self, value: Any) -> Any:
        # If it's a string, try decode it
        prepared_value = (
            import_string(value)
            if isinstance(value, str)
            else value
        )

        # Must be a class
        if not isinstance(prepared_value, type):
            self._error(value, f"Not a class")

        # Must be a sub-class of our base class
        if not issubclass(prepared_value, self._base):
            self._error(value, f"Not a sub-class of {self._base.__qualname__}")

        return prepared_value
