from typing import List, Union, Type

from django.db.models import Manager, Model
from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.json.core import LicenceSubdescriptorModSpec

from wai.json.raw import RawJSONObject

from ...exceptions import *
from ...models.licences import Licence, Permission, Condition, Limitation
from ...serialisers import LicenceSerialiser
from ._RoutedViewSet import RoutedViewSet


class LicenceSubdescriptorViewSet(RoutedViewSet):
    """
    Mixin for the LicenceViewSet which adds the ability to add/remove subdescriptors.
    """
    # The keyword used to specify when the view-set is in licence mode
    MODE_KEYWORD: str = "licence"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/subdescriptors{trailing_slash}$',
                mapping={'patch': 'modify_subdescriptors'},
                name='{basename}-subdescriptors',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: LicenceSubdescriptorViewSet.MODE_KEYWORD}
            )
        ]

    def modify_subdescriptors(self, request: Request, pk=None):
        """
        Action to modify the sub-descriptors of a licence.

        :param request:     The request.
        :param pk:          The primary key of the team being accessed.
        :return:            The response containing the new membership record.
        """
        # Get the mod-spec from the request
        mod_spec = JSONParseFailure.attempt(dict(request.data), LicenceSubdescriptorModSpec)

        # Get the method to use to make the modification
        method = self.add_subdescriptors if mod_spec.method == "add" else self.remove_subdescriptors

        return Response(method(self.get_object(), mod_spec.type, mod_spec.names))

    def add_subdescriptors(self, licence: Licence, type: str, values: List[Union[int, str]]) -> RawJSONObject:
        """
        Adds sub-descriptors of the given type to the licence.

        :param licence:         The licence to add sub-descriptors to.
        :param type:            The type of sub-descriptor to add.
        :param values:          The values to add for the sub-descriptor.
        :return:                The JSON representation of the licence.
        """
        # Get the relation manager for the sub-descriptor type
        subdescriptor_manager = getattr(licence, type)

        # process each value in turn
        for value in values:
            # If we already have an entry with this value, this is a no-op
            if self.get_subdescriptor(subdescriptor_manager, value) is not None:
                continue

            # Get the model for which we are creating an entry
            model = self.get_model(type)

            # See if there exists any entry for this value already
            created = self.get_subdescriptor(model.objects, value)

            # If not, create it
            if created is None:
                # Must supply by name for new entries
                if isinstance(value, int):
                    raise BadArgumentValue(self.action, "names", str(value))

                # Perform actual creation
                created = model(name=value)
                created.save()

            # Add the entry to the licence
            subdescriptor_manager.add(created)

        # Save the changes
        licence.save()

        return LicenceSerialiser().to_representation(licence)

    def remove_subdescriptors(self, licence: Licence, type: str, values: List[Union[int, str]]) -> RawJSONObject:
        """
        Removes sub-descriptors of the given type from the licence.

        :param licence:         The licence to remove sub-descriptors from.
        :param type:            The type of sub-descriptor to remove.
        :param values:          The values to remove for the sub-descriptor.
        :return:                The JSON representation of the licence.
        """
        # Get the relation manager for the sub-descriptor type
        subdescriptor_manager = getattr(licence, type)

        # Process each value in turn
        for value in values:
            # Get the sub-descriptor attached to the licence
            present = self.get_subdescriptor(subdescriptor_manager, value)

            # If there isn't one, this is a no-op
            if present is None:
                continue

            # Remove the sub-descriptor and attempt to delete it
            # (sub-descriptors only successfully delete when all
            # references are removed).
            subdescriptor_manager.remove(present)
            licence.save()
            present.delete()

        return LicenceSerialiser().to_representation(licence)

    def get_model(self, type: str) -> Type[Model]:
        """
        Gets the model associated with the given sub-descriptor type-string.

        :param type:    The sub-descriptor type-string.
        :return:        The model type.
        """
        if type == "permissions":
            return Permission
        elif type == "conditions":
            return Condition
        elif type == "limitations":
            return Limitation
        else:
            raise BadArgumentValue(self.action, "type", type, "permissions, limitations, conditions")

    def get_subdescriptor(self, manager: Manager, value: Union[int, str]):
        """
        Gets the sub-descriptor with the given name/pk from the manager.

        :param manager:     The manager.
        :param value:       The name/pk of the sub-descriptor.
        :return:            The sub-descriptor entry.
        """
        if isinstance(value, str):
            return manager.filter(name=value).first()
        else:
            return manager.filter(pk=value).first()