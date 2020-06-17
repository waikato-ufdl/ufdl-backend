from ufdl.core_app.exceptions import *
from ufdl.core_app.models import Dataset, DatasetQuerySet

from ufdl.json.speech import TranscriptionsFile, Transcription


class SpeechDatasetQuerySet(DatasetQuerySet):
    pass


class SpeechDataset(Dataset):
    objects = SpeechDatasetQuerySet.as_manager()

    def __init__(self, *args, **kwargs):
        # Initialise as usual
        super().__init__(*args, **kwargs)

        # Set a default of no transcriptions
        if self.unstructured == "":
            self.unstructured = "{}"

        # Make sure the unstructured data is valid
        TranscriptionsFile.validate_json_string(self.unstructured)

    def delete_file(self, filename: str):
        # Delete the file as usual
        file = super().delete_file(filename)

        # Remove the file from the transcriptions as well
        transcriptions = self.get_transcriptions()
        if transcriptions.has_property(filename):
            transcriptions.delete_property(filename)
            self.set_transcriptions(transcriptions)

        return file

    def get_transcriptions(self) -> TranscriptionsFile:
        """
        Gets the transcriptions of this speech data-set.

        :return:    The transcriptions for each audio file.
        """
        return TranscriptionsFile.from_json_string(self.unstructured)

    def set_transcriptions(self, transcriptions_file: TranscriptionsFile):
        """
        Sets the transcriptions to the given file.

        :param transcriptions_file:     The new transcriptions file.
        """
        self.unstructured = transcriptions_file.to_json_string()
        self.save()

    def get_transcription(self, filename: str) -> Transcription:
        """
        Gets the transcription of a single audio file.

        :param filename:    The file to get the transcription for.
        :return:            The transcription.
        """
        # Make sure the file exists
        self.has_file(filename, True)

        # Get the transcription file
        transcriptions_file = self.get_transcriptions()

        # Return an empty transcription if none exists
        if not transcriptions_file.has_property(filename):
            return Transcription()

        return transcriptions_file[filename]

    def set_transcription(self, filename: str, transcription: Transcription) -> Transcription:
        """
        Sets the transcription for a file in the data-set.

        :param filename:            The file to set the transcription for.
        :param transcription:       The transcription.
        :return:                    The new transcription.
        """
        # Make sure the file is known
        self.has_file(filename)

        # Load the transcriptions file
        transcriptions_file = self.get_transcriptions()

        # Set the transcription
        transcriptions_file[filename] = transcription

        # Save the transcription
        self.set_transcriptions(transcriptions_file)

        # Return a new transcription file with just the change made
        return transcription
