from django.utils.module_loading import import_string

from ._UFDLSetting import UFDLSetting


class UFDLClassSetting(UFDLSetting):
    """
    Setting type which expects a class as its value.
    """
    def _get(self):
        # Get the raw value as usual
        value = super()._get()

        # If it's a string, try decode it
        if isinstance(value, str):
            value = import_string(value)

        return value
