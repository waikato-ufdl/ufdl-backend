from typing import List, NoReturn

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ...exceptions import BadArgumentValue
from ...models.nodes import Hardware
from ...serialisers.nodes import HardwareSerialiser
from ._RoutedViewSet import RoutedViewSet


class GetHardwareGenerationViewSet(RoutedViewSet):
    """
    Mixin for the hardware view-set which adds the ability to
    get the name of a hardware generation from the compute
    capability.
    """
    # The keyword used to specify when the view-set is in get-hardware-generation mode
    MODE_KEYWORD: str = "get-hardware-generation"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/get-hardware-generation/(?P<compute>.+){trailing_slash}$',
                mapping={'get': 'get_hardware_generation'},
                name='{basename}-get-hardware-generation',
                detail=False,
                initkwargs={cls.MODE_ARGUMENT_NAME: GetHardwareGenerationViewSet.MODE_KEYWORD}
            )
        ]

    def get_hardware_generation(self, request: Request, compute=None):
        """
        Action to get the hardware generation for a given level
        of compute capability.

        :param request:     The request.
        :param compute:     The level of compute capability.
        :return:            The response containing the job.
        """
        # Attempt to parse the compute level
        try:
            capability = float(compute)
        except ValueError:
            self._bad_argument(compute)

        # Get the hardware generation that corresponds to the compute level
        generation = Hardware.objects.for_compute_capability(capability)

        # If none do, raise an error
        if generation is None:
            self._bad_argument(compute)

        return Response(HardwareSerialiser().to_representation(generation))

    def _bad_argument(self, compute: str) -> NoReturn:
        """
        Handles the case when the compute value is not valid.

        :param compute:     The compute value.
        """
        # Get the allowed range of compute values
        min, max = Hardware.objects.get_full_compute_range()

        # Raise a bad-argument error
        raise BadArgumentValue(self.action, "compute", compute, f"[{min}, {max})")
