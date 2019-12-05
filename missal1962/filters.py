import re
from trans import trans


def newline2br(text):
    return text.replace('\n', '<br>')


def asterisks2em(text):
    return re.sub('\*([^\*]+)\*', '<em>\\1</em>', text)


def slugify(text):
    """
    "Antyfona na Komunię" -> "antyfona-na-komunie"
    :param text:
    :return:
    """
    return trans(text).replace(' ', '-').lower()

