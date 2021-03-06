from ._AllowNone import AllowNone
from ._IsAdminUser import IsAdminUser
from ._IsAuthenticated import IsAuthenticated
from ._IsMember import IsMember
from ._IsNode import IsNode
from ._IsOwnMembership import IsOwnMembership
from ._IsPublic import IsPublic
from ._IsSelf import IsSelf
from ._JobIsWorkable import JobIsWorkable
from ._MemberHasAdminPermission import MemberHasAdminPermission
from ._MemberHasExecutePermission import MemberHasExecutePermission
from ._MemberHasWritePermission import MemberHasWritePermission
from ._MemberPermission import MemberPermission
from ._NodeIsSelf import NodeIsSelf
from ._NodeOwnsJob import NodeOwnsJob
from ._NodePermission import NodePermission
from ._NodeWorkingJob import NodeWorkingJob

# A combination permission that allows members with write permissions or
# nodes with execute permissions to perform an action
WriteOrNodeExecutePermission = MemberHasWritePermission | (IsNode & MemberHasExecutePermission)
