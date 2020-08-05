from django.db import models

from ...apps import UFDLCoreAppConfig


class NodeQuerySet(models.Model):
    """
    A query-set over worker nodes.
    """
    def delete(self, using=None, keep_parents=False):
        raise Exception("Can't delete nodes")


class Node(models.Model):
    """
    A worker node.
    """
    # The IP address of the worker node
    ip = models.CharField(max_length=39)

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
    last_seen = models.DateTimeField()

    # The job the node is currently working on
    current_job = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Job",
                                    on_delete=models.DO_NOTHING,
                                    related_name="+",
                                    null=True)

    objects = NodeQuerySet.as_manager()

    def delete(self, using=None, keep_parents=False):
        raise Exception("Can't delete nodes")
