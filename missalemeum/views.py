from functools import wraps
import os
import sys
import logging
from flask import render_template, Blueprint, request, send_from_directory, Response
from jinja2 import TemplateNotFound
import apiv5
from constants.common import LANGUAGES, LANGUAGE_ENGLISH

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s ] %(levelname)s in %(module)s: %(message)s")

log = logging.getLogger(__name__)
views = Blueprint("views", __name__)
body_404 = [{"info": {"title": "404"}, "sections": [{"label": "", "body": [["Page not found"]]}]}]



def render_template_or_404(template, lang, **context):
    try:
        return render_template(template, lang=lang, **context)
    except TemplateNotFound:
        return render_template('index.html', body=body_404, lang=lang), 404


def infer_locale(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'lang' in kwargs:
            if kwargs['lang'] not in LANGUAGES.keys():
                return render_template('index.html', body=body_404, lang=LANGUAGE_ENGLISH), 404
        else:
            kwargs['lang'] = request.accept_languages.best_match(LANGUAGES.keys())
        return f(*args, **kwargs)
    return decorated_function


def get_body(method, required_kwarg, **kwargs):
    body = None
    if not required_kwarg or kwargs.get(required_kwarg):
        resp = getattr(apiv5, method)(**kwargs)
        # for failed request response will be a tuple[Response, int]
        if isinstance(resp, Response) and resp.status_code == 200:
            body = resp.json
        else:
            body = body_404
    return body


@views.route("/")
@views.route("/<string:lang>")
@views.route("/<string:lang>/<string:date_or_id>")
@infer_locale
def proprium(lang: str = LANGUAGE_ENGLISH, date_or_id: str = None):
    body = get_body('v5_proper', 'date_or_id', date_or_id=date_or_id, lang=lang)
    return render_template("index.html", body=body, lang=lang)


@views.route("/<string:lang>/ordo")
@infer_locale
def ordo(lang: str = LANGUAGE_ENGLISH):
    body = get_body('v5_ordo', None, lang=lang)
    return render_template("index.html", body=body, lang=lang)


@views.route("/<string:lang>/canticum")
@views.route("/<string:lang>/canticum/<string:proper_id>")
@infer_locale
def canticum(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    print(request.args.get("format"))
    body = get_body('v5_canticum_by_id', "id_", id_=proper_id, lang=lang)
    return render_template("index.html", body=body, lang=lang)


@views.route("/<string:lang>/oratio")
@views.route("/<string:lang>/oratio/<string:proper_id>")
@infer_locale
def oratio(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    body = get_body('v5_oratio_by_id', "id_", id_=proper_id, lang=lang)
    return render_template("index.html", body=body, lang=lang)


@views.route("/<string:lang>/votive")
@views.route("/<string:lang>/votive/<string:proper_id>")
@infer_locale
def votive(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    body = get_body('v5_proper', 'date_or_id', date_or_id=proper_id, lang=lang)
    return render_template("index.html", body=body, lang=lang)


@views.route("/<string:lang>/supplement")
@views.route("/<string:lang>/supplement/<string:resource>")
@infer_locale
def supplement(lang: str = LANGUAGE_ENGLISH, resource: str = None):
    body = get_body('v5_supplement', "id_", id_=resource, lang=lang)
    return render_template("index.html", body=body, lang=lang)


@views.route("/<string:lang>/info")
@infer_locale
def info(lang: str = LANGUAGE_ENGLISH):
    return render_template("index.html", body=None, lang=lang)


@views.route("/service-worker.js")
def service_worker():
    return send_from_directory(os.path.join(views.root_path, "build"), "service-worker.js")


@views.route("/robots.txt")
def robots():
    return send_from_directory(os.path.join(views.root_path, "build"), "robots.txt")
