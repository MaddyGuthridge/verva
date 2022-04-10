
from verva.version import VersionSpec


def test_any():
    s = VersionSpec(min_version=None, max_version=None)
    assert 1 in s


def test_min():
    s = VersionSpec(min_version=1, max_version=None)
    assert 2 in s
    assert 0 not in s


def test_max():
    s = VersionSpec(min_version=None, max_version=10)
    assert 9 in s
    assert 10 not in s


def test_longer_min():
    s = VersionSpec(min_version=(1, 0, 1), max_version=None)
    assert 1 not in s
    assert (1, 0, 1) in s


def test_longer_max():
    s = VersionSpec(min_version=None, max_version=(1, 0, 1))
    assert 1 in s
    assert (1, 0, 1) not in s
