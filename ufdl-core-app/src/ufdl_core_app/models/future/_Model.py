from django.db import models
from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet, TeamOwnedModel

from ..apps import APP_NAME
from ..mixins import PublicModel, PublicQuerySet


class ModelQuerySet(PublicQuerySet, SoftDeleteQuerySet):
    pass


class Model(TeamOwnedModel, PublicModel, SoftDeleteModel):
    # The name of the model
    name = models.CharField(max_length=200)

    # The version of the model
    version = models.IntegerField(default=1)

    # The model format
    format = models.CharField(max_length=16)

    # Location of the model file
    location = models.CharField(max_length=200)

    # The project the model belongs to
    project = models.ForeignKey(f"{APP_NAME}.Project",
                                on_delete=models.DO_NOTHING,
                                related_name="models")

    objects = ModelQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_models_per_project",
                                    fields=["name", "version", "project"])
        ]

    def get_owning_team(self):
        return self.project.team

    def __str__(self):
        return f"Model \"{self.name}\": {self.project}"
