from typing import Optional

from django.db.models.signals import post_init
from django.dispatch import receiver

from ..models import Dataset, DataDomain


@receiver(post_init, dispatch_uid='dataset_domains')
def dataset_domains(sender, **kwargs):
    """
    Sets the domain of a dataset after it's created.

    Default values on fields have no context, which is necessary
    for allowing the domain to be set by individual data-set sub-types

    :param sender:  The sender of the signal (unused).
    :param kwargs:  The signal arguments (should include an 'instance' keyword).
    """
    # Get the instance from the keyword arguments
    instance = kwargs['instance']

    # If it's not a dataset, no need to do anything
    if not isinstance(instance, Dataset):
        return

    # If this is not initial creation of the object (i.e. it is loaded from the database)
    # then abort
    if instance.pk is not None:
        return

    # Get the specified default value for the domain from the sub-type
    domain_code: Optional[str] = instance.domain_code()

    # Sub-types must specify a domain
    if type(instance) is not Dataset and domain_code is None:
        raise ValueError("Sub-types of Dataset must provide a data-domain code")

    # Get the domain via its code
    domain: Optional[DataDomain] = DataDomain.for_code(domain_code) if domain_code is not None else None

    # If the domain wasn't found, error
    if domain is None and domain_code is not None:
        raise ValueError(f"Unknown domain-code '{domain_code}'")

    # Set the domain on the instance
    instance.domain = domain
