import sys

import logging
from flask import Flask

from apiv2 import api as apiv2
from filters import slugify, asterisks2em, newline2br
from views import views

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')

app = Flask(__name__)
app.register_blueprint(views)
app.register_blueprint(apiv2)
app.jinja_env.filters['slugify'] = slugify
app.jinja_env.filters['asterisks2em'] = asterisks2em
app.jinja_env.filters['newline2br'] = newline2br
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
