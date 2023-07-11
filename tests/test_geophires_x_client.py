from geophires_x_client import longest
from geophires_x_client.cli import main


def test_main():
    assert main([]) == 0


def test_longest():
    assert longest([b'a', b'bc', b'abc']) == b'abc'
