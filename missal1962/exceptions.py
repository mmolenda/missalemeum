
class MissalException(Exception):
    pass


class InvalidInput(MissalException):
    pass


class ProperNotFound(MissalException):
    pass


class SupplementNotFound(MissalException):
    pass
