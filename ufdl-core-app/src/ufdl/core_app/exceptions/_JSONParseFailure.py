from typing import Type, TypeVar

from rest_framework import status
from rest_framework.exceptions import APIException

from wai.json.error import JSONError
from wai.json.object import JSONObject
from wai.json.raw import RawJSONObject

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

    @staticmethod
    def attempt_multi(
            raw_json,
            definition: Type[DefinitionType],
            *definitions: Type[DefinitionType]
    ) -> DefinitionType:
        """
        Attempts to parse the raw JSON into one of many types,
        raising this error type on failure.

        :param raw_json:        The raw JSON to parse.
        :param definition:      The definition of the first JSON structure to try.
        :param definitions:
                                Any subsequent JSON structures to try.
        :return:                The parsed document.
        """
        try:
            return definition.from_raw_json(raw_json)
        except JSONError as e:
            if len(definitions) == 0:
                raise JSONParseFailure(raw_json, definition, str(e))
            try:
                return JSONParseFailure.attempt_multi(raw_json, *definitions)
            except JSONParseFailure as e2:
                raise JSONParseFailure(raw_json, definition, str(e)) from e2

    @staticmethod
    def validate(raw_json: RawJSONObject, definition: Type[DefinitionType]):
        """
        Validates the raw JSON, raising this error type on failure.

        :param raw_json:        The raw JSON to validate.
        :param definition:      The definition of the JSON structure.
        """
        try:
            definition.validate_raw_json(raw_json)
        except JSONError as e:
            raise JSONParseFailure(raw_json, definition, str(e))
