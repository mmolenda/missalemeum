import os

import pytest

from api import app
from api.constants.common import LANGUAGE_LATIN
from api.kalendar.factory import MissalFactory

HERE = os.path.abspath(os.path.dirname(__file__))

missal_buffer = {}


def get_missal(year, lang=LANGUAGE_LATIN):
    missal_id = f'{year}{lang}'
    if missal_id not in missal_buffer:
        missal_buffer[missal_id] = MissalFactory().create(year, lang=lang)
    return missal_buffer[missal_id]


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client
