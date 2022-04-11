
import pytest
from verva import VervaContext
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
    ctx = VervaContext("test")

    @ctx.register(min_version=1, max_version=2)
    def a():
        pass
    with pytest.raises(OverlappingVersionException):
        @ctx.register(min_version=1, max_version=2)
        def a():
            pass

