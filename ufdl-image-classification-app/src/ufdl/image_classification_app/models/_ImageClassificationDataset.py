from typing import List, Iterator, Tuple

from ufdl.core_app.exceptions import *
from ufdl.core_app.models import Dataset, DatasetQuerySet, FileReference

from ufdl.json.image_classification import CategoriesFile

from ._Category import Category, CategoryQuerySet


class ImageClassificationDatasetQuerySet(DatasetQuerySet):
    pass


class ImageClassificationDataset(Dataset):
    objects = ImageClassificationDatasetQuerySet.as_manager()

    @classmethod
    def domain_code(cls) -> str:
        return "ic"

    @property
    def categories(self) -> CategoryQuerySet:
        """
        All categories in this dataset.
        """
        return Category.objects.filter(file__in=self.files.all())

    def merge_annotations(self, other: Dataset, files: List[Tuple[FileReference, FileReference]]):
        for source_file_reference, destination_file_reference in files:
            for category in source_file_reference.categories.all():
                label: str = category.category
                if not destination_file_reference.categories.with_category(label).exists():
                    Category(
                        file=destination_file_reference,
                        category=label
                    ).save()


    def clear_annotations(self):
        self.categories.delete()

    def delete_file(self, filename: str):
        # Get the reference to the file
        reference: FileReference = self.get_file_reference(filename)

        # Delete the categories of the file
        if reference is not None:
            reference.categories.all().delete()

        # Delete the file as usual
        return super().delete_file(filename)

    def get_categories_for_file(self, filename: str) -> List[str]:
        """
        Gets the categories for a particular file in the dataset.

        :param filename:
                    The name of the file.
        :return:
                    The list of categories.
        """
        reference: FileReference = self.get_file_reference(filename)
        if reference is None:
            return []
        return [category.category for category in reference.categories.all()]

    def get_categories(self) -> CategoriesFile:
        """
        Gets the categories of this classification data-set.

        :return:    The categories for each image.
        """
        categories_file = CategoriesFile()

        for filename in self.iterate_filenames():
            categories = self.get_categories_for_file(filename)

            if len(categories) > 0:
                categories_file.set_property(filename, categories)

        return categories_file

    def set_categories(self, categories_file: CategoriesFile) -> CategoriesFile:
        """
        Sets the categories to the given file.

        :param categories_file:     The new categories file.
        """
        for filename in categories_file.properties():
            self.categories.for_file(filename).delete()
            self.add_categories([filename], categories_file[filename])

        return categories_file

    def add_categories(self, images: List[str], categories: List[str]) -> CategoriesFile:
        """
        Adds categories to the images in this data-set.

        :param images:      The images to apply the categories to.
        :param categories:  The categories to apply to the images.
        :return:            A categories-file of just the changes made.
        """
        # If images or categories is empty, this is a no-op
        if len(images) == 0 or len(categories) == 0:
            return CategoriesFile()

        # It is an error to supply an empty string as a category
        if any(category == "" for category in categories):
            raise BadName("", "Category names can't be empty")

        # Remove any duplicate images/categories
        images = list(set(images))
        categories = list(set(categories))

        # Create a dictionary of additions to make
        additions = CategoriesFile()
        for image in images:
            reference = self.files.with_filename(image).first()

            # Make sure the image is a file we have
            if reference is None:
                raise BadName(image, "Data-set has no image with this name")

            for category in categories:
                if not reference.categories.with_category(category).exists():
                    instance = Category(
                        file=reference,
                        category=category
                    )
                    instance.save()
                    if image not in additions:
                        additions[image] = [category]
                    else:
                        additions[image] += [category]

        return additions

    def remove_categories(self, images: List[str], categories: List[str]) -> CategoriesFile:
        """
        Removes categories from the images in this data-set.

        :param images:      The images to remove the categories from.
        :param categories:  The categories to remove from the images.
        :return:            A categories-file of just the changes made.
        """
        # If images or categories is empty, this is a no-op
        if len(images) == 0 or len(categories) == 0:
            return CategoriesFile()

        # It is an error to supply an empty string as a category
        if any(category == "" for category in categories):
            raise BadName("", "Category names can't be empty")

        # Remove any duplicate images/categories
        images = list(set(images))
        categories = list(set(categories))

        # Create a dictionary of removals to make
        removals = CategoriesFile()
        for image in images:
            reference = self.files.with_filename(image).first()

            # Make sure the image is a file we have
            if reference is None:
                raise BadName(image, "Data-set has no image with this name")

            for category in categories:
                qs = reference.categories.with_category(category)
                if qs.exists():
                    qs.delete()
                    if image not in removals:
                        removals[image] = [category]
                    else:
                        removals[image] += [category]

        return removals
