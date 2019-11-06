import sys

import os

import datetime
import logging
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from typing import List, Tuple

import controller
from constants.common import LANGUAGE_VERNACULAR
from exceptions import InvalidInput, ProperNotFound
from kalendar.models import Calendar, Day
from propers.models import Proper

app = Flask(__name__)
CORS(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


@app.route('/')
@app.route('/<path:path>')
def frontend(path=''):
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return send_file(index_path)


@app.route('/date/<string:date_>')
def date(date_: str):
    try:
        date_object = datetime.datetime.strptime(date_, '%Y-%m-%d').date()
        day: Day = controller.get_day(date_object, LANGUAGE_VERNACULAR)
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


@app.route('/proper/<string:proper_id>')
def proper(proper_id: str):
    try:
        proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, LANGUAGE_VERNACULAR)
    except (InvalidInput, ProperNotFound) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return jsonify([proper_vernacular.serialize(), proper_latin.serialize()])


@app.route('/calendar')
@app.route('/calendar/<int:year>')
def calendar(year: int = None):
    if year is None:
        year = datetime.datetime.now().date().year
    missal: Calendar = controller.get_calendar(year, LANGUAGE_VERNACULAR)
    return jsonify(missal.serialize())


@app.route('/ical')
def ical():
    return controller.get_ical(LANGUAGE_VERNACULAR)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
