
class MissalException(Exception):
    pass


class InvalidInput(MissalException):
    pass


class ProperNotFound(MissalException):
    pass


class SectionNotFound(MissalException):
    pass


class SupplementNotFound(MissalException):
    pass
