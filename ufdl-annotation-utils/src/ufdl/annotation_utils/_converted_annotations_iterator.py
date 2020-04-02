from typing import Callable, Iterator, Tuple, IO

from wai.annotations.main.parsing import MainParserConfigurer

from ufdl.json.object_detection import AnnotationsFile

from ._annotations_iterator import annotations_iterator


def converted_annotations_iterator(
        annotations_file: AnnotationsFile,
        image_data_supplier: Callable[[str], bytes],
        *args: str) -> Iterator[Tuple[str, IO[bytes]]]:
    """
    Similar to annotations_iterator, except takes a wai.annotations format and
    command-line arguments, and returns an iterator over the annotations files
    produced by converting the annotations using wai.annotations.

    :param annotations_file:        The annotations file.
    :param image_data_supplier:     A callable that takes the filename of an image and returns
                                    the image's data.
    :param args:                    Any command-line arguments to wai.annotations.
    :return:                        An iterator of filename, file-contents pairs.
    """
    # Make the arguments mutable
    args = list(args)

    # Add a dummy output option if none is supplied
    if "-o" not in args and "--output" not in args:
        args += ["-o", "annotations"]

    # Parse the args and retrieve the output chain
    main_settings, input_side, output_side = MainParserConfigurer(no_input=True).parse(args)
    assert output_side is not None
    output_chain = output_side[1]

    # Return a function which invokes the conversion components
    return output_chain.file_iterator(annotations_iterator(annotations_file, image_data_supplier))
