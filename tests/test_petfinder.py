import pytest
from petfinder.utils.bot import PetAppBot


def test_print(capture_stdout):
    print("hello")
    assert capture_stdout["stdout"] == "hello\n"


def test2():
    # load database and make some basic queries
    # request url and check response is not empty: shows that site url hasn't changed
    # check that some curent items are in database
    pass
