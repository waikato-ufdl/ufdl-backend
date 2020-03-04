from typing import List

from ufdl.core_app.exceptions import *
from ufdl.core_app.models import Dataset, DatasetQuerySet

from ..json import CategoriesFile


class ImageClassificationDatasetQuerySet(DatasetQuerySet):
    pass


class ImageClassificationDataset(Dataset):
    objects = ImageClassificationDatasetQuerySet.as_manager()

    def __init__(self, *args, **kwargs):
        # Initialise as usual
        super().__init__(*args, **kwargs)

        # Set a default of no categories
        if self.unstructured == "":
            self.unstructured = "{}"

        # Make sure the unstructured data is valid
        CategoriesFile.validate_json_string(self.unstructured)

    def delete_file(self, filename: str):
        # Delete the file as usual
        file = super().delete_file(filename)

        # Remove the file from the categories as well
        categories = self.get_categories()
        if categories.has_property(filename):
            categories.delete_property(filename)
            self.set_categories(categories)

        return file

    def get_categories(self) -> CategoriesFile:
        """
        Gets the categories of this classification data-set.

        :return:    The categories for each image.
        """
        return CategoriesFile.from_json_string(self.unstructured)

    def set_categories(self, categories_file: CategoriesFile):
        """
        Sets the categories to the given file.

        :param categories_file:     The new categories file.
        """
        self.unstructured = categories_file.to_json_string()
        self.save()

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

        # Load the categories file
        categories_file = self.get_categories()

        # Create a dictionary of additions to make
        additions = CategoriesFile()
        for image in images:
            # Make sure the image is a file we have
            if not self.files.with_filename(image).exists():
                raise BadName(image, "Data-set has no image with this name")

            # Determine the set of categories to add to the image
            if image not in categories_file:
                additions[image] = categories
            else:
                categories_to_add = list(set(categories) - set(categories_file[image]))
                if len(categories_to_add) > 0:
                    additions[image] = categories_to_add

        # If there are additions to be made, make them
        if sum(1 for _ in additions.properties()) > 0:  # TODO: Replace with wai.common.iterate.count when released
            # Add the additions
            for image in additions:
                categories_file[image] += additions[image]

            # Replace the old categories with the new one
            self.set_categories(categories_file)

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

        # Load the categories file
        categories_file = self.get_categories()

        # Create a dictionary of removals to make
        removals = CategoriesFile()
        for image in images:
            # Make sure the image is a file we have
            if not self.files.with_filename(image).exists():
                raise BadName(image, "Data-set has no image with this name")

            # Determine the set of categories to remove from the image
            if image in categories_file:
                categories_to_remove = list(set(categories).intersection(set(categories_file[image])))
                if len(categories_to_remove) > 0:
                    removals[image] = categories_to_remove

        # If there are removals to be made, make them
        if sum(1 for _ in removals.properties()) > 0:
            # Make the removals
            for image in removals:
                for category in removals[image]:
                    categories_file[image].remove(category)

            # Replace the old categories with the new one
            self.set_categories(categories_file)

        return removals
