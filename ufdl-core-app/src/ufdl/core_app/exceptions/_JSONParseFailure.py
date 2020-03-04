from typing import Type, TypeVar

from rest_framework import status
from rest_framework.exceptions import APIException

from wai.json.error import JSONError
from wai.json.object import JSONObject

# The type of definition being parsed
DefinitionType = TypeVar("DefinitionType", bound=JSONObject)


class JSONParseFailure(APIException):
    """
    Error for when parsing of JSON fails.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'json_parse_failure'

    def __init__(self, raw_json, definition: Type[DefinitionType], reason: str):
        super().__init__(f"Unable to parse JSON: {reason}\n"
                         f"\n"
                         f"{raw_json}\n"
                         f"\n"
                         f"Schema:\n"
                         f"{definition.get_json_validation_schema()}")

    @staticmethod
    def attempt(raw_json, definition: Type[DefinitionType]) -> DefinitionType:
        """
        Attempts to parse the raw JSON, raising this error type on failure.

        :param raw_json:        The raw JSON to parse.
        :param definition:      The definition of the JSON structure.
        :return:                The parsed document.
        """
        try:
            return definition.from_raw_json(raw_json)
        except JSONError as e:
            raise JSONParseFailure(raw_json, definition, str(e))
