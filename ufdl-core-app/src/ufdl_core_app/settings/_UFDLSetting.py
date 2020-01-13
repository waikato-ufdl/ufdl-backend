from typing import Optional, Callable, Any

from django.conf import settings

# The settings name for the UFDL settings dictionary
UFDL_SETTINGS_SETTING = "UFDL"


class UFDLSetting:
    """
    Class representing an individual setting available to the UFDL.
    """
    def __init__(self, *, default=None, validator: Optional[Callable[[Any], str]] = None):
        self._default = default
        self._validator: Optional[Callable[[Any], str]] = validator

    def __get__(self, instance, owner):
        # Get the value
        value = self._get()

        # Validate it
        self._validate(value)

        return value

    def _get(self):
        # Get the namespaced UFDL settings dictionary
        settings_dict = getattr(settings, UFDL_SETTINGS_SETTING, {})

        # If it's not a dictionary, alert the user
        if not isinstance(settings_dict, dict):
            raise TypeError(f"'{UFDL_SETTINGS_SETTING}' setting should be a dict "
                            f"but was a '{settings_dict.__class__.__name__}'")

        # Return the default if the setting isn't set explicitly
        if self._name not in settings_dict:
            return self._default

        # Get our value from the dictionary
        return settings_dict[self._name]

    def __delete__(self, instance):
        raise RuntimeError("Cannot delete settings")

    def __set_name__(self, owner, name):
        self._name = name

    def _validate(self, value):
        """
        Validates the value if a validator is available.

        :param value:   The value to validate.
        """
        # No validator, no validation
        if self._validator is None:
            return

        # Perform validation
        error = self._validator(value)

        if error is not None:
            raise ValueError(f"UFDL setting error for '{self._name}': {error}")
