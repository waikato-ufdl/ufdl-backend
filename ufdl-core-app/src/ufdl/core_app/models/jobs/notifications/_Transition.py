from enum import Enum


class Transition(Enum):
    """
    Enumeration of the transitions a job can go through.
    """
    ACQUIRE = 0
    RELEASE = 1
    START = 2
    FINISH = 3
    ERROR = 4
    RESET = 5
    ABORT = 6
    PROGRESS = 7

    @property
    def json_property_name(self) -> str:
        """
        Gets the name of the JSON property for this transition.
        """
        return f"on_{self.name.lower()}"
