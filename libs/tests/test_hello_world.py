from _ast import Assert

from libs.ragsearch.hello_world import hello_world

def test_hello_world():
    assert hello_world() is None