from constants import LANGUAGE_LATIN
from missal1962.factory import MissalFactory

missal_buffer = {}


def get_missal(year):
    if year not in missal_buffer:
        missal_buffer[year] = MissalFactory.create(year, lang=LANGUAGE_LATIN)
    return missal_buffer[year]
