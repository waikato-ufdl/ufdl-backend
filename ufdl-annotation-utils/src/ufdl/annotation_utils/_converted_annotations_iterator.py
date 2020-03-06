from argparse import ArgumentParser
from typing import Callable, Iterator, Tuple, IO

from wai.annotations.core import set_settings, Settings, InternalFormatConverter, Writer
from wai.annotations.core.cli import CommandLineSeparateImageWriterFactory
from wai.annotations.main import get_internal_format_converter_factory, get_writer_factory

from ufdl.json.object_detection import AnnotationsFile

from ._annotations_iterator import annotations_iterator


def converted_annotations_iterator(
        annotations_file: AnnotationsFile,
        image_data_supplier: Callable[[str], bytes],
        format: str,
        *args: str) -> Iterator[Tuple[str, IO[bytes]]]:
    """
    Similar to annotations_iterator, except takes a wai.annotations format and
    command-line arguments, and returns an iterator over the annotations files
    produced by converting the annotations using wai.annotations.

    :param annotations_file:        The annotations file.
    :param image_data_supplier:     A callable that takes the filename of an image and returns
                                    the image's data.
    :param format:                  The wai.annotations format string of the output.
    :param args:                    Any command-line arguments to wai.annotations.
    :return:                        An iterator of filename, file-contents pairs.
    """
    # Make the arguments mutable
    args = list(args)

    # Add a dummy output option if none is supplied
    if "-o" not in args and "--output" not in args:
        args += ["-o", "annotations"]

    # Get the converter and writer for the annotations format
    converter_factory = get_internal_format_converter_factory(format)
    writer_factory = get_writer_factory(format)

    # Ensure --no-images argument for separate image writers
    if issubclass(writer_factory, CommandLineSeparateImageWriterFactory) and "--no-images" not in args:
        args.append("--no-images")

    # Create an argument parser to read the given arguments
    parser = ArgumentParser()
    Settings.configure_parser(parser)
    converter_factory.configure_parser(parser)
    writer_factory.configure_parser(parser)

    # Parse the given arguments
    namespace = parser.parse_args(args)

    # Set the wai.annotations library settings
    set_settings(Settings.instance_from_namespace(namespace))

    # Create the conversion components
    converter: InternalFormatConverter = converter_factory.instance_from_namespace(namespace)
    writer: Writer = writer_factory.instance_from_namespace(namespace)

    # Return a function which invokes the conversion components
    return writer.file_iterator(converter.convert_all(annotations_iterator(annotations_file, image_data_supplier)))
