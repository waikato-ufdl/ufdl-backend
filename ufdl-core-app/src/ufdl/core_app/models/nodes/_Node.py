from typing import Optional

from django.db import models

from ...apps import UFDLCoreAppConfig
from ...exceptions import BadNodeID
from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class NodeQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set over worker nodes.
    """
    pass


class Node(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A worker node.
    """
    # The IP address of the worker node
    ip = models.CharField(max_length=39)

    # An identifier to disambiguate between multiple nodes on the same system
    index = models.PositiveSmallIntegerField()

    # The NVidia driver version
    driver_version = models.CharField(max_length=16)

    # The hardware generation of graphics on the node
    hardware_generation = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Hardware",
                                            on_delete=models.DO_NOTHING,
                                            related_name="nodes",
                                            null=True)

    # The amount of GPU memory available on the node, in MB
    gpu_mem = models.PositiveIntegerField()

    # The amount of CPU memory available on the node, in MB
    cpu_mem = models.PositiveIntegerField()

    # The timestamp when the node last made contact
    last_seen = models.DateTimeField(null=True, default=None)

    # The job the node is currently working on
    current_job = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Job",
                                    on_delete=models.DO_NOTHING,
                                    related_name="+",
                                    null=True,
                                    default=None)

    objects = NodeQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure each unique node is only registered once
            models.UniqueConstraint(name="unique_nodes",
                                    fields=["ip", "index"])
        ]

    @property
    def is_working_job(self) -> bool:
        """
        Whether this node is currently working a job.
        """
        return self.current_job is not None

    @classmethod
    def from_request(cls, request) -> Optional['Node']:
        """
        Gets the node from the request, if there is one.

        :param request:     The request.
        :return:            The node, or None if there isn't one.
        """
        # Get the node ID from the header if specified
        node_id = request.headers.get("Node-Id", None)

        # If not specified, return None
        if node_id is None:
            return None

        # Attempt to parse the node ID
        try:
            node = int(node_id)
        except ValueError as e:
            raise BadNodeID(node_id, "Unable to parse into an integer primary-key")

        # Filter the primary-key into a node object
        node = cls.objects.filter(pk=node).first()

        # If the node doesn't exist, raise an error
        if node is None:
            raise BadNodeID(node_id, "No node with this primary-key")

        return node
