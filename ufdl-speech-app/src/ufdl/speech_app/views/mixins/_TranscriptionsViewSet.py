from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.core_app.exceptions import *
from ufdl.core_app.views.mixins import RoutedViewSet

from ufdl.json.speech import Transcription

from ...models import SpeechDataset


class TranscriptionsViewSet(RoutedViewSet):
    """
    Mixin for view-sets which allow the setting of transcriptions against files.
    """
    # The keyword used to specify when the view-set is in transcriptions mode
    MODE_KEYWORD: str = "transcriptions"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/transcriptions{trailing_slash}$',
                mapping={'get': 'get_transcriptions'},
                name='{basename}-transcriptions',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: TranscriptionsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/transcriptions/(?P<fn>.+){trailing_slash}$',
                mapping={'get': 'get_transcription_for_file',
                         'post': 'set_transcription_for_file'},
                name='{basename}-transcriptions-for-file',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: TranscriptionsViewSet.MODE_KEYWORD}
            )
        ]

    def get_transcriptions(self, request: Request, pk=None):
        """
        Gets the transcriptions of a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the transcriptions.
        """
        # Get the data-set
        dataset = self.get_object_of_type(SpeechDataset)

        # Return the transcriptions
        return Response(dataset.get_transcriptions().to_raw_json())

    def get_transcription_for_file(self, request: Request, pk=None, fn=None):
        """
        Gets the transcription for a single file.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :param fn:          The filename of the audio file.
        :return:            The response containing the transcription.
        """
        # Get the data-set
        dataset = self.get_object_of_type(SpeechDataset)

        # Return the transcriptions
        return Response(dataset.get_transcription(fn).to_raw_json())

    def set_transcription_for_file(self, request: Request, pk=None, fn=None):
        """
        Sets the transcription for a single audio file.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :param fn:          The filename of the audio file.
        :return:            The response containing the transcription.
        """
        # Get the data-set
        dataset = self.get_object_of_type(SpeechDataset)

        # Parse the transcription
        transcription = JSONParseFailure.attempt(dict(request.data), Transcription)

        # Return the transcriptions
        return Response(dataset.set_transcription(fn, transcription).to_raw_json())
