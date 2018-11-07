import datetime
from flask import Flask, jsonify
from typing import List, Tuple

import controller
from exceptions import InvalidInput, ProperNotFound
from kalendar.models import Calendar
from propers.models import Proper

app = Flask(__name__)


lang = 'Polski'


@app.route('/')
@app.route('/date')
def index():
    return date(datetime.datetime.now().strftime('%Y-%m-%d'))


@app.route('/date/<string:date_>')
def date(date_: str):
    try:
        date_object = datetime.datetime.strptime(date_, '%Y-%m-%d').date()
        propers: List[Tuple[Proper, Proper]] = controller.get_proper_by_date(date_object, lang)
    except ValueError:
        return jsonify({'error': str('Incorrect date format, should be %Y-%m-%d')}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        return jsonify([propers[0][0].serialize(), propers[0][1].serialize()])


@app.route('/proper/<string:proper_id>')
def proper(proper_id: str):
    try:
        proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, lang)
    except (InvalidInput, ProperNotFound) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return jsonify([proper_vernacular.serialize(), proper_latin.serialize()])


@app.route('/calendar')
@app.route('/calendar/<int:year>')
def calendar(year: int = None):
    if year is None:
        year = datetime.datetime.now().date().year
    missal: Calendar = controller.get_calendar(year, lang)
    return jsonify(missal.serialize())


@app.route('/search/<string:token>')
def search(token: str):
    payload = {}
    for result in controller.search(token, lang):
        payload[result.id] = result.title
    return jsonify(payload)
