"""
Package defining the relational models for the UFDL API.
"""
from ._Dataset import Dataset, DatasetQuerySet
from ._Project import Project, ProjectQuerySet
from ._User import User

# Include all of the file models as well
from .files import *

# And the licence models
from .licences import *
