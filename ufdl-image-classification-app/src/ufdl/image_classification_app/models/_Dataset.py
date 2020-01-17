from ufdl.core_app.models import Dataset as CoreDataset, DatasetQuerySet as CoreDatasetQuerySet

from .mixins import CategoriesModel


class DatasetQuerySet(CoreDatasetQuerySet):
    pass


class Dataset(CategoriesModel, CoreDataset):
    objects = DatasetQuerySet.as_manager()

    def copy(self, *, creator=None, new_name=None, **kwargs) -> 'Dataset':
        # Create the copy as usual
        copy = super().copy(creator=creator, new_name=new_name, **kwargs)

        # Add our categories to the copy
        copy.categories = self.categories
        copy.save()

        return copy
