import os


def format_suffix(filename: str, suffix: int) -> str:
    """
    Formats a filename with a suffix between the base and extension
    of the given filename.

    :param filename:    The base filename.
    :param suffix:      The suffix value.
    :return:            The formatted filename.
    """
    base, ext = os.path.splitext(filename)

    return f"{base}-{suffix:04}{ext}"
