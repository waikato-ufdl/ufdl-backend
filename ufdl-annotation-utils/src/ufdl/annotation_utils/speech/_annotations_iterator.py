from typing import Iterator, Callable, Iterable

from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.speech import SpeechInstance, Transcription


def annotations_iterator(filenames: Iterable[str],
                         transcription_supplier: Callable[[str], str],
                         image_data_supplier: Callable[[str], bytes]) -> Iterator[SpeechInstance]:
    """
    Creates an iterator over the speech files in an annotations file in
    the format expected by wai.annotations.

    :param filenames:               An iterator over the filenames in the dataset.
    :param transcription_supplier:  A supplier of transcriptions for the files.
    :param image_data_supplier:     A callable that takes the filename of an audio file and returns
                                    the file's data.
    :return:                        The iterator.
    """

    # Process each known audio file
    for filename in filenames:
        yield SpeechInstance(
            Audio.from_file_data(filename, image_data_supplier(filename)),
            Transcription(transcription_supplier(filename))
        )
