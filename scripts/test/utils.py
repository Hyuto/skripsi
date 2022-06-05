import os
from ..utils import get_name

current_directory = os.path.dirname(__file__)


def test_get_name():
    assert get_name(os.path.join(current_directory, "test-file.txt")) == os.path.join(
        current_directory, "test-file.txt"
    )
    assert get_name(os.path.join(current_directory, "utils.py")) == os.path.join(
        current_directory, "utils (1).py"
    )
