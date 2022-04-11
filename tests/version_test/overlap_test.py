
from verva.version import VersionSpec

def test_same():
    """Versions should overlap with themselves"""
    a = VersionSpec(min_version=1, max_version=2)
    assert a.overlap(a)

def test_simple():
    a = VersionSpec(min_version=1, max_version=3)
    b = VersionSpec(min_version=2, max_version=4)
    assert a.overlap(b)
    assert b.overlap(a)

def test_no_overlap():
    a = VersionSpec(min_version=1, max_version=3)
    b = VersionSpec(min_version=3, max_version=4)
    assert not a.overlap(b)
    assert not b.overlap(a)

def test_min():
    """Test with unspecified min_version"""
    a = VersionSpec(min_version=None, max_version=5)
    b = VersionSpec(min_version=1, max_version=2)
    assert a.overlap(b)
    assert b.overlap(a)

def test_max():
    """Test with unspecified max_version"""
    a = VersionSpec(min_version=3, max_version=None)
    b = VersionSpec(min_version=5, max_version=7)
    assert a.overlap(b)
    assert b.overlap(a)
