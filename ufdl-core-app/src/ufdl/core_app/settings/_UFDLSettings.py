class UFDLSettings:
    """
    Class representing all of the available settings for the UFDL.
    """
    # The registry of settings classes, keyed by their declared namespace
    __registry = {}

    @classmethod
    def namespace(cls) -> str:
        """
        The namespace for the settings.
        """
        raise NotImplementedError(UFDLSettings.namespace.__qualname__)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Get the provided namespace
        namespace = cls.namespace()

        # Make sure it's a string
        if not isinstance(namespace, str):
            raise Exception("Must provide a namespace as a string")

        # Make sure it's an identifier
        if not namespace.isidentifier():
            raise Exception(f"'{namespace}' is not a valid identifier")

        # Make sure it's not already taken
        if namespace in UFDLSettings.__registry:
            raise Exception(f"Namespace '{namespace}' already in use")

        # Add the new class to the registry
        UFDLSettings.__registry[namespace] = cls
