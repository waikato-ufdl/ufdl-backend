from enum import Enum


class Transition(Enum):
    """
    Enumeration of the transitions a job can go through.
    """
    ACQUIRE = 0
    RELEASE = 1
    START = 2
    PROGRESS = 3
    FINISH = 4
    ERROR = 5
    RESET = 6
    ABORT = 7
    CANCEL = 8

    @property
    def json_property_name(self) -> str:
        """
        Gets the name of the JSON property for this transition.
        """
        return f"on_{self.name.lower()}"
