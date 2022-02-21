"""
Package for exceptions in processing requests.
"""
from ._AcquireMetaJobAttempt import AcquireMetaJobAttempt
from ._BadArgumentType import BadArgumentType
from ._BadArgumentValue import BadArgumentValue
from ._BadDescendantName import BadDescendantName
from ._BadJobTemplate import BadJobTemplate
from ._BadModelType import BadModelType
from ._BadName import BadName
from ._BadNodeID import BadNodeID
from ._BadSource import BadSource
from ._ChildNotificationOverridesForWorkableJob import ChildNotificationOverridesForWorkableJob
from ._CouldntParseType import CouldntParseType
from ._IllegalPhaseTransition import IllegalPhaseTransition
from ._InvalidJobInput import InvalidJobInput
from ._JobAcquired import JobAcquired
from ._JobFinished import JobFinished
from ._JobNotAcquired import JobNotAcquired
from ._JobNotFinished import JobNotFinished
from ._JobNotStarted import JobNotStarted
from ._JobStarted import JobStarted
from ._JSONParseFailure import JSONParseFailure
from ._MergeDisallowed import MergeDisallowed
from ._MissingParameter import MissingParameter
from ._NodeAlreadyWorking import NodeAlreadyWorking
from ._NotServerResidentType import NotServerResidentType
from ._PermissionsUndefined import PermissionsUndefined
from ._TypeIsAbstract import TypeIsAbstract
from ._UnknownParameters import UnknownParameters
