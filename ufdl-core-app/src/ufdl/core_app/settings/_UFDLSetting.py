from typing import Any

from django.conf import settings

from ._UFDLSettings import UFDLSettings


class UFDLSetting:
    """
    Class representing an individual setting available to the UFDL backend.
    """
    def __init__(self, default):
        self._name: str = None
        self._owner: UFDLSettings = None
        self._default = default
        self._cache = None
        self._cached = False

    # region Descriptor

    def __get__(self, instance, owner):
        # Check the cache
        if self._cached:
            return self._cache

        # Get the raw value from the Django settings file
        raw_value = self._get_raw_value_from_settings()

        # Prepare the value
        value = self._prepare(raw_value)

        # Cache the prepared value
        self._cache = value
        self._cached = True

        return value

    def __delete__(self, instance):
        raise RuntimeError("Cannot delete settings")

    def __set_name__(self, owner, name):
        # Owner can only be UFDLSettings
        # (local import to avoid circularity error)
        from ._UFDLSettings import UFDLSettings
        if not issubclass(owner, UFDLSettings):
            raise Exception(
                f"Only sub-classes of {UFDLSettings.__qualname__} can "
                f"own {type(self).__qualname__} descriptors"
            )

        # Can't re-use a settings object (create new instance per setting)
        if self._name is not None:
            raise Exception(
                f"Can't re-use {type(self).__qualname__} descriptors"
            )

        # Save our name and owner
        self._name = name
        self._owner = owner

    # endregion

    # region Raw

    def _get_raw_value_from_settings(self):
        """
        Gets the value the user set for this setting from the Django
        settings, or the default if it is not set.

        :return:
                    The specified or default value for this setting.
        """
        # Get the namespace for this setting
        namespace = self._owner.namespace()

        # Get the namespace dictionary
        settings_dict = getattr(settings, namespace, {})

        # If it's not a dictionary, alert the user
        if not isinstance(settings_dict, dict):
            raise TypeError(
                f"'{namespace}' setting should be a dictionary "
                f"but was a '{type(settings_dict).__qualname__}'"
            )

        # Return the default if the setting isn't set explicitly
        if self._name not in settings_dict:
            return self._default

        # Get our value from the dictionary
        return settings_dict[self._name]

    # endregion

    # region Validation

    def _prepare(self, value: Any) -> Any:
        """
        Parses the raw settings value and prepares it for use.

        :param value:
                    The raw settings value.
        :return:
                    The prepared value of this setting.
        """
        return value

    def _error(
            self,
            raw_value: Any,
            reason: str
    ):
        """
        Should be called by prepare to report an error with the
        raw setting value.

        :param raw_value:
                    The raw value of the setting.
        :param reason:
                    The reason for the error.
        """
        raise ValueError(
            f"Error preparing setting value for {self._name}: {raw_value}\n"
            f"{reason}"
        )

    # endregion
