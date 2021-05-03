from django.db import models


def filter_by_name(
        query_set: models.QuerySet,
        name: str
) -> models.QuerySet:
    # Get the model for this query-set
    model = query_set.model

    # Should be a named model
    assert issubclass(model, NamedModel), (
        f"Model of "
        f"{query_set.__class__.__name__}"
        f" is not a "
        f"{NamedModel.__qualname__} "
        f"({model.__qualname__})"
    )

    # Get the filter expression for the model name
    filter = model.name_filter_Q(name)

    return query_set.filter(filter)


class NamedModel(models.Model):
    """
    Mixin model for adding the ability to get the name of an object.
    """
    class Meta:
        abstract = True

    @classmethod
    def name_filter_Q(cls, name: str) -> models.Q:
        """
        Gets a query filter for the given name.

        :param name:
                    The name to filter to.
        :return:
                    The name filter.
        """
        # Default name field is 'name'
        return models.Q(name=name)
