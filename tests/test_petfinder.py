import pytest
from petfinder.utils.bot import PetAppBot


def test_print(capture_stdout):
    print("hello")
    assert capture_stdout["stdout"] == "hello\n"
