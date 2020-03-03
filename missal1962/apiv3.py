import datetime
import flask
import sys

import logging

from flask import jsonify, Blueprint

import controller
from constants.common import LANGUAGE_VERNACULAR
from exceptions import InvalidInput, ProperNotFound, SupplementNotFound
from kalendar.models import Day, Calendar
from utils import format_propers, get_supplement

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


api = Blueprint('apiv3', __name__)


@api.route('/<string:lang>/api/v3/date/<string:date_>')
def v3_date(date_: str, lang: str = LANGUAGE_VERNACULAR):
    try:
        date_object = datetime.datetime.strptime(date_, '%Y-%m-%d').date()
        day: Day = controller.get_day(date_object, lang)
    except ValueError:
        return jsonify({'error': str('Incorrect date format, should be %Y-%m-%d')}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        return jsonify(format_propers(day))


@api.route('/<string:lang>/api/v3/proper/<string:proper_id>')
def v3_proper(proper_id: str, lang: str = LANGUAGE_VERNACULAR):
    try:
        proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, lang)
    except (InvalidInput, ProperNotFound) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return jsonify([proper_vernacular.serialize(), proper_latin.serialize()])


@api.route("/<string:lang>/api/v3/supplement/<string:resource>")
@api.route("/<string:lang>/api/v3/supplement/<subdir>/<string:resource>")
def v3_supplement(resource: str, subdir: str = None, lang: str = LANGUAGE_VERNACULAR):

    try:
        supplement_yaml = get_supplement(api.root_path, lang, resource, subdir)
    except SupplementNotFound:
        return jsonify({'error': "Not found"}), 404
    else:
        return jsonify(supplement_yaml)


@api.route('/<string:lang>/api/v3/calendar')
@api.route('/<string:lang>/api/v3/calendar/<int:year>')
def v3_calendar(year: int = None, lang: str = LANGUAGE_VERNACULAR):
    if year is None:
        year = datetime.datetime.now().date().year
    missal: Calendar = controller.get_calendar(year, lang)
    return jsonify(missal.serialize())


@api.route('/<string:lang>/api/v3/icalendar')
@api.route('/<string:lang>/api/v3/icalendar/<int:rank>')
def v3_ical(rank: int = 2, lang: str = LANGUAGE_VERNACULAR):
    try:
        rank = int(rank)
        assert rank in range(1, 5)
    except (ValueError, AssertionError):
        rank = 2

    response = flask.Response(controller.get_ical(lang, rank))
    response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
    return response
