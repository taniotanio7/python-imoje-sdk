# -*- coding: utf-8 -*-

import pytest
from imoje_sdk.skeleton import fib

__author__ = "Jonatan Witoszek"
__copyright__ = "Jonatan Witoszek"
__license__ = "apache"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
