
from typing import Iterator, Tuple, IO

from wai.annotations.core.builder import ConversionPipelineBuilder
from wai.annotations.core.component.util import iterate_files
from wai.annotations.core.domain import Instance


def converted_annotations_iterator(
        instances: Iterator[Instance],
        *args: str
) -> Iterator[Tuple[str, IO[bytes]]]:
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
    global_args, args = ConversionPipelineBuilder.split_global_options(args)

    # Not allowed to provide global arguments
    if len(global_args) > 0:
        raise ValueError(f"Not allowed to use global options; found {', '.join(global_args)}")

    # Split the options into stages
    stage_args = ConversionPipelineBuilder.split_options(args)

    # Create a pipeline builder
    builder = ConversionPipelineBuilder()

    # Add all stages except the last to the builder
    for stage in stage_args[:-1]:
        builder.add_stage(stage[0], stage[1:])

    # Add a dummy output option if none is supplied
    if "-o" not in stage_args[-1] and "--output" not in stage_args[-1]:
        stage_args[-1] += ["-o", "annotations"]

    # Add the output stage to the conversion chain
    builder.add_stage(stage_args[-1][0], stage_args[-1][1:])

    # Build the pipeline
    pipeline = builder.to_pipeline()

    # Make sure the chain doesn't have an input
    if pipeline.has_source:
        raise ValueError(f"wai.annotations arguments specify an input stage ({stage_args[0][0]})")

    return iterate_files(pipeline, instances)
