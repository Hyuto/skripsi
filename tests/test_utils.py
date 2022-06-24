import os

from scripts.utils import get_name

current_directory = os.path.dirname(__file__)


def test_get_name():
    test_file = os.path.join(current_directory, "test-file.txt")
    assert get_name(test_file) == test_file

    with open(test_file, "w") as writer:
        writer.write("test file")

    assert get_name(test_file) == os.path.join(current_directory, "test-file (1).txt")

    os.remove(test_file)
