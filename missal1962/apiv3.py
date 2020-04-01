import datetime
from functools import wraps

import flask
import sys

import logging

from flask import jsonify, Blueprint

import controller
from constants import TRANSLATION
from constants.common import LANGUAGE_ENGLISH
from exceptions import InvalidInput, ProperNotFound, SupplementNotFound, SectionNotFound
from kalendar.models import Day, Calendar
from constants.common import LANGUAGES
from utils import format_propers, get_supplement, format_proper_sections, get_pregenerated_proper

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


api = Blueprint('apiv3', __name__)


def validate_locale(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if kwargs['lang'] not in LANGUAGES.keys():
            return jsonify({'error': "Not found"}), 404
        return f(*args, **kwargs)
    return decorated_function


@api.route('/<string:lang>/api/v3/date/<string:date_>')
@validate_locale
def v3_date(date_: str, lang: str = LANGUAGE_ENGLISH):
    try:
        date_object = datetime.datetime.strptime(date_, '%Y-%m-%d').date()
        day: Day = controller.get_day(date_object, lang)
        pregenerated_proper = get_pregenerated_proper(lang, day.get_celebration_id())
        if pregenerated_proper is not None:
            return jsonify(pregenerated_proper)
        return jsonify(format_propers(day))
    except ValueError:
        return jsonify({'error': str('Incorrect date format, should be %Y-%m-%d')}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/<string:lang>/api/v3/proper/<string:proper_id>')
@validate_locale
def v3_proper(proper_id: str, lang: str = LANGUAGE_ENGLISH):
    proper_id = {i['ref']: i['id'] for i in TRANSLATION[lang].VOTIVE_MASSES}.get(proper_id, proper_id)
    try:
        pregenerated_proper = get_pregenerated_proper(lang, proper_id)
        if pregenerated_proper is not None:
            return jsonify(pregenerated_proper)
        proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, lang)
        return jsonify([{
            "info": {
                "id": proper_vernacular.id,
                "rank": proper_vernacular.rank,
                "colors": proper_vernacular.colors,
                "title": proper_vernacular.title,
                "description": proper_vernacular.description,
                "additional_info": proper_vernacular.additional_info
            },
            "sections": format_proper_sections(proper_vernacular, proper_latin)
        }])
    except InvalidInput as e:
        return jsonify({'error': str(e)}), 400
    except ProperNotFound as e:
        return jsonify({'error': str(e)}), 404
    except SectionNotFound as e:
        return jsonify({'error': str(e)}), 500


@api.route("/<string:lang>/api/v3/supplement/<string:resource>")
@api.route("/<string:lang>/api/v3/supplement/<subdir>/<string:resource>")
@validate_locale
def v3_supplement(resource: str, subdir: str = None, lang: str = LANGUAGE_ENGLISH):

    try:
        supplement_yaml = get_supplement(lang, resource, subdir)
    except SupplementNotFound:
        return jsonify({'error': "Not found"}), 404
    else:
        return jsonify(supplement_yaml)


@api.route('/<string:lang>/api/v3/calendar')
@api.route('/<string:lang>/api/v3/calendar/<int:year>')
@validate_locale
def v3_calendar(year: int = None, lang: str = LANGUAGE_ENGLISH):
    if year is None:
        year = datetime.datetime.now().date().year
    missal: Calendar = controller.get_calendar(year, lang)
    return jsonify(missal.serialize())


@api.route('/<string:lang>/api/v3/icalendar')
@api.route('/<string:lang>/api/v3/icalendar/<int:rank>')
@validate_locale
def v3_ical(rank: int = 2, lang: str = LANGUAGE_ENGLISH):
    try:
        rank = int(rank)
        assert rank in range(1, 5)
    except (ValueError, AssertionError):
        rank = 2

    response = flask.Response(controller.get_ical(lang, rank))
    response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
    return response
