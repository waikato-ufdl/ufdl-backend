from typing import Union

from django.db import models

from ufdl.core_app.apps import UFDLCoreAppConfig
from ufdl.core_app.models import FileReference, NamedFile, Filename


class CategoryQuerySet(models.QuerySet):
    """
    Query-set of categories.
    """
    def for_file(self, file: Union[FileReference, NamedFile, Filename, str]):
        """
        Filters the query-set to those files with the given filename.

        :param file:
                    The file to filter to.
        :return:
                    The filtered query-set.
        """
        if isinstance(file, FileReference) or isinstance(file, NamedFile) or isinstance(file, Filename):
            file = file.filename

        return self.filter(file__file__name__filename=file)

    def with_category(self, category: Union['Category', str]):
        """
        Returns all categories with the given label.

        :param category:
                    The label.
        :return:
                    The filtered query-set.
        """
        if isinstance(category, Category):
            category = category.category

        return self.filter(category=category)


class Category(models.Model):
    # The file in the dataset that the category applies to
    file = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.FileReference",
        on_delete=models.DO_NOTHING,
        related_name="sc_categories"
    )

    # The category
    category = models.TextField()

    objects = CategoryQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_categories_for_spectra",
                fields=["file", "category"]
            )
        ]