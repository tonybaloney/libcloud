import sys


def test_runtime_dist():
    """
    Check running on 3.5+
    """
    assert sys.version_info >= (3, 5)
