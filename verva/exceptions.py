"""verva > exceptions

Exceptions generated by Verva
"""


class VervaException(Exception):
    """Base class for all Verva exceptions
    """


class SignatureNotFoundException(VervaException):
    """Exception for when a requested signature hasn't been registered with
    Verva
    """


class NoMatchingVersionException(VervaException):
    """Exception for when a requested signature is found, but doesn't have a
    mapping for the given version

    This indicates that the registered function doesn't exist for the targeted
    API version
    """


class OverlappingVersionException(VervaException):
    """Exception for when two versions registered for a function overlap

    For example, the following versions would overlap:
    * `VersionSpec( >= 10 < 12)` and `VersionSpec( >= 9 )`
    * `VersionSpec( >= 5 < 8)` and `VersionSpec( >= 7.2 )`

    And the following versions would not
    * `VersionSpec( >= 2 < 9)` and `VersionSpec( >= 9 )`
    """
