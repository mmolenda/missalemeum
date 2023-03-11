from typing import List

from constants import common as constants

# Pages in paper missal/s


def get_pages(pallotinum: int) -> List[str]:
    return [
        f"Pallotinum s. {pallotinum}"
    ]


PAGES = {
    constants.TEMPORA_QUAD2_6: get_pages(207),
    constants.TEMPORA_QUAD3_0: get_pages(212),
    constants.TEMPORA_QUAD3_1: get_pages(215),
    constants.TEMPORA_QUAD3_2: get_pages(218),
    constants.TEMPORA_QUAD3_3: get_pages(221),
    constants.TEMPORA_QUAD3_4: get_pages(224),
    constants.TEMPORA_QUAD3_5: get_pages(226),
    constants.TEMPORA_QUAD3_6: get_pages(230),
    constants.TEMPORA_QUAD4_0: get_pages(235),
    # Votive
    constants.TEMPORA_C_10A: get_pages(649),
    constants.COMMUNE_C_10A: get_pages(649),
    constants.TEMPORA_C_10B: get_pages(652),
    constants.COMMUNE_C_10B: get_pages(652),
    constants.TEMPORA_C_10C: get_pages(654),
    constants.COMMUNE_C_10C: get_pages(654),
    constants.TEMPORA_C_10PASC: get_pages(654),
    constants.COMMUNE_C_10PASC: get_pages(654),
    constants.TEMPORA_C_10T: get_pages(655),
    constants.COMMUNE_C_10T: get_pages(655),
}
