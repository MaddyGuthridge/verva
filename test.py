
from verva import VervaContext

verva = VervaContext("test", ["test"])

def a():
    pass

@verva.register(a, 3)
def __a():
    pass
