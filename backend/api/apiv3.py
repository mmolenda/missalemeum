
import sys

import logging

from flask import Blueprint, redirect

from apiv5 import validate_locale
from constants.common import LANGUAGE_ENGLISH

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


api = Blueprint('apiv3', __name__)


@api.route('/<string:lang>/api/v3/icalendar')
@api.route('/<string:lang>/api/v3/icalendar/<int:rank>')
@validate_locale
def v3_ical(rank: int = 2, lang: str = LANGUAGE_ENGLISH):
    location = f"/{lang}/api/v5/icalendar"
    if rank:
        location += f"/{rank}"
    return redirect(location, code=302)
