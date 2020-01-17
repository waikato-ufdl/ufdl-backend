import json
from typing import List

from django.db import models

from ufdl.core_app.apps import UFDLCoreAppConfig
from ufdl.core_app.exceptions import *
from ufdl.core_app.models.files import File

from wai.common.json import RawJSONObject, deep_copy


class CategoriesModel(models.Model):
    """
    Mixin model for adding the ability to add categories to files in
    the file-container.
    """
    # The file containing the image categories
    categories = models.ForeignKey(f"{UFDLCoreAppConfig.label}.File",
                                   on_delete=models.DO_NOTHING,
                                   related_name="+")

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        # Dynamic default for categories is the empty set
        if "categories" not in kwargs:
            kwargs.update(categories=File.get_reference_from_backend("{}".encode()))
        super().__init__(*args, **kwargs)

    @classmethod
    def serialise_categories_file(cls, file: RawJSONObject) -> bytes:
        """
        Serialises the categories file for writing to disk.

        :param file:    The categories file.
        :return:        The write data.
        """
        return json.dumps(file, indent=2, sort_keys=True).encode()

    @classmethod
    def deserialise_categories_file(cls, file: bytes) -> RawJSONObject:
        """
        Deserialises the categories file as read from disk.

        :param file:    The read data.
        :return:        The categories file.
        """
        return json.loads(file.decode())

    def get_categories(self) -> RawJSONObject:
        """
        Gets the categories of this classification data-set.

        :return:    The categories for each image.
        """
        return self.deserialise_categories_file(self.categories.get_data())

    def add_categories(self, images: List[str], categories: List[str]):
        """
        Adds categories to the images in this data-set.

        :param images:      The images to apply the categories to.
        :param categories:  The categories to apply to the images.
        :return:            The changes made to the categories.
        """
        # If images or categories is empty, this is a no-op
        if len(images) == 0 or len(categories) == 0:
            return {}

        # It is an error to supply an empty string as a category
        if any(category == "" for category in categories):
            raise BadName("", "Category names can't be empty")

        # Remove any duplicate images/categories
        images = list(set(images))
        categories = list(set(categories))

        # Load the categories file
        categories_file = self.get_categories()

        # Create a dictionary of additions to make
        additions = {}
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
        if len(additions) > 0:
            # Create a copy
            new_categories_file = deep_copy(categories_file)

            # Add the additions
            for image in additions:
                if image not in new_categories_file:
                    new_categories_file[image] = []
                new_categories_file[image] += additions[image]

            # Create the new categories file
            self.categories = File.get_reference_from_backend(self.serialise_categories_file(new_categories_file))
            self.save()

        return additions

    def remove_categories(self, images: List[str], categories: List[str]):
        """
        Removes categories from the images in this data-set.

        :param images:      The images to remove the categories from.
        :param categories:  The categories to remove from the images.
        :return:            The changes made to the categories.
        """
        # If images or categories is empty, this is a no-op
        if len(images) == 0 or len(categories) == 0:
            return {}

        # It is an error to supply an empty string as a category
        if any(category == "" for category in categories):
            raise BadName("", "Category names can't be empty")

        # Remove any duplicate images/categories
        images = list(set(images))
        categories = list(set(categories))

        # Load the categories file
        categories_file = self.get_categories()

        # Create a dictionary of removals to make
        removals = {}
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
        if len(removals) > 0:
            # Create a copy
            new_categories_file = deep_copy(categories_file)

            # Make the removals
            for image in removals:
                for category in removals[image]:
                    new_categories_file[image].remove(category)

            # Create the new categories file
            self.categories = File.get_reference_from_backend(self.serialise_categories_file(new_categories_file))
            self.save()

        return removals
