import os

import datetime
import re
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from typing import List, Tuple, Union

import controller
from exceptions import InvalidInput, ProperNotFound
from kalendar.models import Calendar, Day
from propers.models import Proper, ProperSection

app = Flask(__name__)
CORS(app)


lang = 'Polski'


@app.route('/')
@app.route('/<path:path>')
def frontend(path=''):
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return send_file(index_path)


def _parse_comment(comment: Union[None, ProperSection]) -> dict:
    retval = {
        "title": "",
        "description": "",
        "additional_info": []
    }
    if comment is None:
        return retval
    for ln in comment.get_body():
        if ln.startswith('#'):
            retval['title'] = re.split("[–—-]", ln.strip("#"), 1)[-1].strip()
        elif ln.strip().startswith('*') and ln.endswith('*'):
            retval['additional_info'].append(ln.replace('*', ''))
        else:
            retval['description'] += ln + '\n'
    return retval


@app.route('/date/<string:date_>')
def date(date_: str):
    try:
        date_object = datetime.datetime.strptime(date_, '%Y-%m-%d').date()
        missal: Calendar = controller.get_calendar(date_object.year, lang)
        day: Day = missal.get_day(date_object)
        propers: List[Tuple[Proper, Proper]] = day.get_proper()
    except ValueError:
        return jsonify({'error': str('Incorrect date format, should be %Y-%m-%d')}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        retvals = []
        for propers_vernacular, propers_latin in propers:
            info = {
                "title": None,
                "description": None,
                "additional_info": None,
                "tempora": None,
                "date": date_,
            }
            comment: ProperSection = propers_vernacular.pop_section('Comment')
            parsed_comment: dict = _parse_comment(comment)
            # In most of the cases calculate the celebration title from the Observance object falling on
            # a given day; in case of days with multiple masses (02 Nov, 25 Dec) get the title from
            # proper's comment directly
            info['title'] = day.get_celebration_name() if len(propers) < 2 else parsed_comment['title']
            info['description'] = parsed_comment['description']
            info['additional_info'] = parsed_comment['additional_info']

            tempora_name: str = day.get_tempora_name()
            info["tempora"] = tempora_name if tempora_name != info["title"] else None

            retvals.append({
                "info": info,
                "proper_vernacular": propers_vernacular.serialize(),
                "proper_latin": propers_latin.serialize()
            })
        return jsonify(retvals)


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


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)
