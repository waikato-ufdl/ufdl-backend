from abc import ABC, abstractmethod
from typing import IO, Union, Type, Iterator


class FileSystemBackend(ABC):
    """
    Base-class for file-systems supported by UFDL.
    """
    # The singleton instance of the backend
    _instance: 'FileSystemBackend' = None

    @classmethod
    def instance(cls) -> 'FileSystemBackend':
        """
        Gets the singleton instance of the file-system backend.

        :return:    The backend instance.
        """
        # Create the singleton instance on first access
        if cls._instance is None:
            cls._instance = cls._initialise_backend()

        return cls._instance

    @classmethod
    @abstractmethod
    def _initialise_backend(cls) -> 'FileSystemBackend':
        """
        Initialises the file-system backend. Takes no arguments,
        if configuration arguments are needed, they should be
        added to the settings.

        :return:    The initialised backend.
        """
        pass

    def migrate(self, other: Union['FileSystemBackend', Type['FileSystemBackend']]):
        """
        Migrates the data from this backend to another.

        :param other:   The other file-system.
        """
        # Get the backend instance
        if not isinstance(other, FileSystemBackend):
            other = other.instance()

        # Can't migrate to ourselves
        if other is self:
            raise ValueError("Cannot migrate a file-system backend to itself")

        # Migrate all files
        for handle in self:
            other.save(self.read(handle))

    @abstractmethod
    def save(self, contents: Union[bytes, IO[bytes]]) -> 'Handle':
        """
        Saves a file to the file-system.

        :param contents:    The binary contents of the file to save.
        :return:            A unique handle to the file.
        """
        pass

    @abstractmethod
    def read(self, handle: 'Handle') -> Union[bytes, IO[bytes]]:
        """
        Reads a file from the file-system.

        :param handle:  The handle to the file.
        :return:        The file contents.
        """
        pass

    def load(self, handle: 'Handle') -> bytes:
        """
        Loads a file from the file-system into memory.

        :param handle:  The handle to the file.
        :return:        The file contents.
        """
        # Get the file contents (may be the data or a stream)
        contents = self.read(handle)

        # Read the entire file into memory if given as a stream
        if not isinstance(contents, bytes):
            contents = contents.read()

        return contents

    @abstractmethod
    def delete(self, handle: 'Handle'):
        """
        Deletes a file from the file-system.

        :param handle:  The handle of the file to delete.
        """
        pass

    @abstractmethod
    def all(self) -> Iterator['Handle']:
        """
        Gets an iterator over all files in the backend.

        :return:    The file handle iterator.
        """
        pass

    def __iter__(self) -> Iterator['Handle']:
        return self.all()

    class Handle(ABC):
        """
        Represents a single file on the file-system. Must be convertible
        to a unique string representation.
        """
        # The maximum length of the string representation of the handle
        # (so it can be stored in a database char-field)
        MAX_STRING_REPR_LENGTH: int = 128

        @abstractmethod
        def to_database_string(self) -> str:
            """
            Returns a string representation of the file-handle.

            :return:    The handle string.
            """
            pass

        @classmethod
        @abstractmethod
        def from_database_string(cls, string: str) -> 'FileSystemBackend.Handle':
            """
            Converts the database string representation into a handle object.

            :param string:  The handle string representation.
            :return:        The handle.
            """
            pass
