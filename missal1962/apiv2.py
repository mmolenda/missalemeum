import datetime
import flask
import sys

import logging
from flask import jsonify, Blueprint
from typing import List, Tuple

import controller
from constants.common import LANGUAGE_VERNACULAR
from exceptions import InvalidInput, ProperNotFound
from kalendar.models import Day, Calendar
from propers.models import Proper

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


api = Blueprint('api', __name__)


@api.route('/api/v2/date/<string:date_>')
# @api.route('/<string:lang>/api/v2/date/<string:date_>')
def v2_date(date_: str, lang: str = LANGUAGE_VERNACULAR):
    try:
        date_object = datetime.datetime.strptime(date_, '%Y-%m-%d').date()
        day: Day = controller.get_day(date_object, lang)
        propers: List[Tuple[Proper, Proper]] = day.get_proper()
    except ValueError:
        return jsonify({'error': str('Incorrect date format, should be %Y-%m-%d')}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        retvals = []
        for propers_vernacular, propers_latin in propers:
            # In most of the cases calculate the celebration title from the Observance object falling on
            # a given day; in case of days with multiple masses (02 Nov, 25 Dec) get the title from
            # proper's comment directly
            title = day.get_celebration_name() if len(propers) < 2 else propers_vernacular.title
            tempora_name: str = day.get_tempora_name()
            info = {
                "id": day.get_celebration_id(),
                "title": title,
                "description": propers_vernacular.description,
                "additional_info": propers_vernacular.additional_info,
                "tempora": tempora_name if tempora_name != title else None,
                "rank": propers_vernacular.rank,
                "date": date_,
            }
            retvals.append({
                "info": info,
                "proper_vernacular": propers_vernacular.serialize(),
                "proper_latin": propers_latin.serialize()
            })
        return jsonify(retvals)


@api.route('/api/v2/proper/<string:proper_id>')
# @api.route('/<string:lang>/api/v2/proper/<string:proper_id>')
def v2_proper(proper_id: str, lang: str = LANGUAGE_VERNACULAR):
    try:
        proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, lang)
    except (InvalidInput, ProperNotFound) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return jsonify([proper_vernacular.serialize(), proper_latin.serialize()])


@api.route('/api/v2/calendar')
@api.route('/api/v2/calendar/<int:year>')
# @api.route('/<string:lang>/api/v2/calendar')
# @api.route('/<string:lang>/api/v2/calendar/<int:year>')
def v2_calendar(year: int = None, lang: str = LANGUAGE_VERNACULAR):
    if year is None:
        year = datetime.datetime.now().date().year
    missal: Calendar = controller.get_calendar(year, lang)
    return jsonify(missal.serialize())


@api.route('/api/v2/icalendar')
@api.route('/api/v2/icalendar/<int:rank>')
# @api.route('/<string:lang>/api/v2/icalendar')
# @api.route('/<string:lang>/api/v2/icalendar/<int:rank>')
def v2_ical(rank: int = 2, lang: str = LANGUAGE_VERNACULAR):
    try:
        rank = int(rank)
        assert rank in range(1, 5)
    except (ValueError, AssertionError):
        rank = 2

    response = flask.Response(controller.get_ical(lang, rank))
    response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
    return response
