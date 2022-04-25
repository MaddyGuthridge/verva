
import pytest
from verva.version import VersionSpec


def test_basic():
    VersionSpec(min_version=None, max_version=None)
    VersionSpec(min_version=4, max_version=5)


def test_order():
    with pytest.raises(ValueError):
        VersionSpec(min_version=5, max_version=4)


def test_not_eq():
    with pytest.raises(ValueError):
        VersionSpec(min_version=5, max_version=5)
