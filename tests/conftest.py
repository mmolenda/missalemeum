from missal import MissalFactory

missal_buffer = {}


def get_missal(year):
    if year not in missal_buffer:
        missal_buffer[year] = MissalFactory.create(year)
    return missal_buffer[year]
