from itertools import chain
from typing import Iterator, Tuple, IO

from wai.annotations.core.chain import ConversionChain
from wai.annotations.core.component import LocalWriter
from wai.annotations.core.instance import Instance


def converted_annotations_iterator(instances: Iterator[Instance],
                                   *args: str) -> Iterator[Tuple[str, IO[bytes]]]:
    """
    Uses wai.annotations to convert a stream of instances into an iterator
    over the converted files produced by the conversion.

    :param instances:               The instances to convert.
    :param args:                    Any command-line arguments to wai.annotations.
    :return:                        An iterator of filename, file-contents pairs.
    """
    # Make the arguments mutable
    args = list(args)

    # Split of any global options
    global_args, args = ConversionChain.split_global_options(args)

    # Not allowed to provide global arguments
    if len(global_args) > 0:
        raise ValueError(f"Not allowed to use global options; found {', '.join(global_args)}")

    # Split the options into stages
    stage_args = ConversionChain.split_options(args)

    # Create a conversion chain with all stages except the last
    conversion_chain = ConversionChain.from_options(list(chain(*stage_args[:-1])))

    # Make sure the chain doesn't have an input
    if conversion_chain.has_input:
        raise ValueError(f"wai.annotations arguments specify an input stage ({stage_args[0][0]})")

    # Add a dummy output option if none is supplied
    if "-o" not in stage_args[-1] and "--output" not in stage_args[-1]:
        stage_args[-1] += ["-o", "annotations"]

    # Add the output stage to the conversion chain
    conversion_chain.add_stage(stage_args[-1][0], stage_args[-1][1:])

    # Make sure the conversion chain actually has an output stage now
    if not conversion_chain.has_output:
        raise ValueError("No output stage specified")

    # Make sure the output stage is a local writer (required for file iterator)
    if not isinstance(conversion_chain._output_stage.writer, LocalWriter):
        raise TypeError("Output stage of annotations conversion chain is not a local writer")

    return conversion_chain.file_iterator(instances)
