"""
Package containing models to do with specifying attributes of worker nodes.
"""
from ._CUDAVersion import CUDAVersion, CUDAVersionQuerySet
from ._DockerImage import DockerImage, DockerImageQuerySet
from ._Framework import Framework, FrameworkQuerySet
from ._Hardware import Hardware, HardwareQuerySet
from ._Node import Node, NodeQuerySet
