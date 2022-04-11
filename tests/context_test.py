
import pytest
from verva import VervaContext, getSignature
from verva.exceptions import OverlappingVersionException

# BUG: When we start automatically registering contexts, we'll need to clear
# them after each test case

def test_registered():
    """Test that items get registered to a context properly"""
    ctx = VervaContext("test")

    @ctx.register(min_version=1, max_version=2)
    def test():
        pass
    def test2():
        pass

    assert ctx.is_registered(test)
    assert not ctx.is_registered(test2)

def test_register_overlap():
    """Do we get an OverlappingVersionException if we try to register
    a function twice for a version
    """
    ctx = VervaContext("test")

    @ctx.register(min_version=1, max_version=2)
    def a():
        pass
    with pytest.raises(OverlappingVersionException):
        @ctx.register(min_version=1, max_version=2)
        def a():
            pass

def test_register_multi():
    """Can we register the a function twice for different versions"""
    ctx = VervaContext("test")

    @ctx.register(min_version=1, max_version=2)
    def a():
        pass
    @ctx.register(min_version=2, max_version=3)
    def a():
        pass
    assert ctx.num_versions(a) == 2

def test_get_associated():
    """Are different registered values associated correctly?"""
    ctx = VervaContext("test")

    @ctx.register(min_version=1, max_version=2)
    def a():
        return 1
    @ctx.register(min_version=2, max_version=3)
    def a():
        return 2

    sign = getSignature(a)

    assert ctx.get_version_mapping(sign, 1)() == 1
    assert ctx.get_version_mapping(sign, 2)() == 2
