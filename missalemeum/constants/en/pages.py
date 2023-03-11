from typing import List

from constants import common as constants

# Pages in paper missal/s


def get_pages(angelus: int, lasance: int, baronius: int) -> List[str]:
    return [
        f"Angelus Press p. {angelus}",
        f"Father Lasance p. {lasance}",
        f"Baronius Press p. {baronius}",
    ]


PAGES = {
    constants.TEMPORA_QUAD2_6: get_pages(353, 283, 369),
    constants.TEMPORA_QUAD3_0: get_pages(359, 294, 377),
    constants.TEMPORA_QUAD3_1: get_pages(363, 294, 380),
    constants.TEMPORA_QUAD3_2: get_pages(368, 303, 385),
}
