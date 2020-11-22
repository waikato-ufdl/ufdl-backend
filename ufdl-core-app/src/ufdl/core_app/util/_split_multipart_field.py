from typing import List


def split_multipart_field(field: str) -> List[str]:
    """
    Splits a multi-part field into its component parts.

    :param field:   The multi-part field's value.
    :return:        The parts.
    """
    return field.split("|", maxsplit=2)
