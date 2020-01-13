from typing import Optional


def IS_SUBCLASS_OF(cls: type):
    """
    Returns a validator that ensures the value of a class setting
    is of a particular type.

    :param cls:     The class that values should be a sub-class of.
    :return:        The validator function.
    """
    def validator(value) -> Optional[str]:
        if not issubclass(value, cls):
            return f"{value} is not a sub-class of {cls}"

        return None

    return validator
