
from verva.util import getSignature

from . import my_module


def test_function_signatures():
    assert (
        getSignature(my_module.function)
        == "tests.test_signatures.my_module.function"
    )


def test_class_signatures():
    assert (
        getSignature(my_module.Class)
        == "tests.test_signatures.my_module.Class"
    )


def test_method_signatures():
    assert (
        getSignature(my_module.Class.method)
        == "tests.test_signatures.my_module.Class.method"
    )
