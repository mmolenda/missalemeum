import sys

import logging
from flask import Flask, request
from flask_babel import Babel
from werkzeug.routing import BaseConverter, ValidationError

from missal1962.__version__ import __version__
from missal1962.apiv3 import api as apiv3
from missal1962.filters import slugify, asterisks2em, newline2br
from missal1962.constants.common import LANGUAGES
from missal1962.views import views

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


class LangConverter(BaseConverter):

    def to_python(self, value):
        if value is None or value in LANGUAGES.keys():
            return value
        raise ValidationError()


app = Flask(__name__)
app.jinja_env.filters['slugify'] = slugify
app.jinja_env.filters['asterisks2em'] = asterisks2em
app.jinja_env.filters['newline2br'] = newline2br
app.url_map.converters['lang'] = LangConverter
app.register_blueprint(views)
app.register_blueprint(apiv3)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)
babel = Babel(app)


@app.context_processor
def inject_globals():
    return {
        "version": __version__,
        "langs": LANGUAGES
    }


@babel.localeselector
def get_locale():
    for lang in LANGUAGES.keys():
        if request.path.strip("/").startswith(lang):
            return lang
    return request.accept_languages.best_match(LANGUAGES.keys())


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
