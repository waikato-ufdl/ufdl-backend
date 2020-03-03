import hashlib
import os
from typing import Union, IO, Optional, Iterable

from ._FileSystemBackend import FileSystemBackend


class LocalDiskBackend(FileSystemBackend):
    """
    File system which uses the processes' local disk for storage.
    """
    def __init__(self, root_dir: str):
        # Make sure the root directory exists
        if not os.path.exists(root_dir):
            os.makedirs(root_dir, exist_ok=True)
        if not os.path.isdir(root_dir):
            raise ValueError(f"'{root_dir}' is not a valid root directory for the file-system")

        self._root_dir: str = root_dir

    @classmethod
    def _initialise_backend(cls) -> 'LocalDiskBackend':
        # Import the UFDL settings
        from ...settings import ufdl_settings

        # Get the root directory setting
        root_dir: str = ufdl_settings.LOCAL_DISK_FILE_DIRECTORY

        return LocalDiskBackend(root_dir)

    def save(self, contents: Union[bytes, IO[bytes]]) -> 'Handle':
        # We require all data in memory for hashing/comparison
        if not isinstance(contents, bytes):
            contents = contents.read()

        # Hash the data
        hashcode = self.get_data_hash(contents)

        # Get the directory to store the data in
        directory = self.path_for_hashcode(hashcode)

        # Get any files that share our hashcode in their filename
        files_with_same_hashcode = (
            [file for file in map(os.path.basename, os.listdir(directory)) if file.startswith(hashcode)]
            if os.path.exists(directory) else []
        )

        # Return a handle to an existing file if it is identical
        for handle in map(self.Handle.from_database_string, files_with_same_hashcode):
            if self.all_bytes_equal(self.load(handle), contents):
                return handle

        # Find an unused tail value
        used_tails = set(map(self.Handle.tail_from_database_string, files_with_same_hashcode))
        next_unused_tail = None
        while next_unused_tail in used_tails:
            next_unused_tail = next_unused_tail + 1 if next_unused_tail is not None else 1

        # Create a handle for the data
        handle = self.Handle(hashcode, next_unused_tail)

        # Make sure the directory exist
        os.makedirs(directory, exist_ok=True)

        # Write the data
        with open(os.path.join(directory, handle.to_database_string()), 'wb') as file:
            file.write(contents)

        return handle

    def path_for_hashcode(self, hashcode: str):
        """
        Gets the path that a file with the given hashcode should be stored under.

        :param hashcode:    The file's hashcode.
        :return:            The path.
        """
        return os.path.join(self._root_dir, self.Handle.relative_path_for_hashcode(hashcode))

    def read(self, handle: 'Handle') -> bytes:
        with open(os.path.join(self.path_for_hashcode(handle.hashcode),
                               handle.to_database_string()),
                  'rb') as file:
            return file.read()

    def delete(self, handle: 'Handle'):
        # Get the directory that the file is in
        directory = self.path_for_hashcode(handle.hashcode)

        # Delete the file itself
        os.remove(os.path.join(directory, handle.to_database_string()))

        # Try to remove any directories that are now empty
        head, tail = os.path.split(directory)
        while directory != self._root_dir:
            try:
                os.rmdir(directory)
                directory = head
                head, tail = os.path.split(head)
            except OSError:
                break

    @classmethod
    def get_data_hash(cls, data: bytes) -> str:
        """
        Gets the hash-code for a given set of data as a string.

        :param data:    The data to hash.
        :return:        The string-representation of the data's hash.
        """
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def all_bytes_equal(i1: Union[bytes, Iterable[bytes]], i2: Union[bytes, Iterable[bytes]]) -> bool:
        """
        Checks if the sequence of bytes are identical between two iterables.

        TODO: Could be much tidier, and possibly more efficient, but only gets
              called in the case of a hash-collision, which should be fairly rare.

        :param i1:  The first iterable.
        :param i2:  The second iterable.
        :return:    True if all bytes are equal.
        """
        # If given raw bytes, just put them in a length-one list to make them iterable
        if isinstance(i1, bytes):
            i1 = [i1]
        if isinstance(i2, bytes):
            i2 = [i2]

        # Get iterators over the data-sources
        iter1 = iter(i1)
        iter2 = iter(i2)

        # Get the first item from the first data-source,
        # checking for empty sources
        try:
            item1 = next(iter1)
        except StopIteration:
            try:
                next(iter2)
                return False
            except StopIteration:
                return True

        # Get the first item from the second data-source,
        # checking for empty sources
        try:
            item2 = next(iter2)
        except StopIteration:
            return False

        # Keep comparing data items until finished
        while True:
            # Work out which item is longer
            longer, shorter = (item1, item2) if len(item1) > len(item2) else (item2, item1)

            # Make sure the longer item starts with the shorter item
            if not longer.startswith(shorter):
                return False

            # Get more data for the (now exhausted) shorter item,
            # checking for end-of-data
            if longer is item1:
                item1 = item1[len(item2):]

                try:
                    item2 = next(iter2)
                except StopIteration:
                    try:
                        next(iter1)
                        return False
                    except StopIteration:
                        return len(item1) == 0
            else:
                item2 = item2[len(item1):]

                try:
                    item1 = next(iter1)
                except StopIteration:
                    try:
                        next(iter2)
                        return False
                    except StopIteration:
                        return len(item2) == 0

    class Handle(FileSystemBackend.Handle):
        def __init__(self, hashcode: str, tail: Optional[int] = None):
            self.hashcode: str = hashcode
            self.tail: Optional[int] = tail

        def to_database_string(self) -> str:
            return self.hashcode + (f"-{self.tail}" if self.tail is not None else "")

        @classmethod
        def from_database_string(cls, string: str) -> 'LocalDiskBackend.Handle':
            return cls(cls.hashcode_from_database_string(string),
                       cls.tail_from_database_string(string))

        @classmethod
        def hashcode_from_database_string(cls, string: str) -> str:
            """
            Gets the hashcode from the database string representation.

            :param string:  The handle's database string representation.
            :return:        The handle's hashcode.
            """
            return string if "-" not in string else string[:string.index("-")]

        @classmethod
        def tail_from_database_string(cls, string: str) -> Optional[int]:
            """
            Gets the tail from the database string representation.

            :param string:  The handle's database string representation.
            :return:        The handle's tail.
            """
            return None if "-" not in string else string[string.index("-") + 1:]

        @classmethod
        def relative_path_for_hashcode(cls, hashcode: str) -> str:
            """
            Gets the path to store a file with the given hash under,
            relative to some root directory.

            :param hashcode:    The file's hashcode.
            :return:            The file's path.
            """
            return os.path.join(hashcode[0:3], hashcode[3:6])
