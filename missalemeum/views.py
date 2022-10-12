import json
from functools import wraps

import os

import datetime
import sys

import logging
import re
from flask import render_template, Blueprint, request, send_from_directory, redirect, render_template_string
from flask_babel import _
from jinja2 import TemplateNotFound

import controller
from constants import TRANSLATION, BLOCKS
from constants.common import LANGUAGES, LANGUAGE_ENGLISH, ORDO_DIR
from exceptions import SupplementNotFound
from kalendar.models import Day
from utils import get_supplement, format_propers, supplement_index, get_pregenerated_proper

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s ] %(levelname)s in %(module)s: %(message)s")

log = logging.getLogger(__name__)


views = Blueprint("views", __name__)


def render_template_or_404(template, lang, **context):
    try:
        return render_template(template, lang=lang, **context)
    except TemplateNotFound:
        return render_template('404.html', lang=lang), 404


def infer_locale(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'lang' in kwargs:
            if kwargs['lang'] not in LANGUAGES.keys():
                return render_template('404.html', lang=LANGUAGE_ENGLISH), 404
        else:
            kwargs['lang'] = request.accept_languages.best_match(LANGUAGES.keys())
        return f(*args, **kwargs)
    return decorated_function


@views.route("/")
@views.route("/<string:date_or_id>")
@views.route("/<string:lang>")
@views.route("/<string:lang>/<string:date_or_id>")
@infer_locale
def proprium(lang: str = LANGUAGE_ENGLISH, date_or_id: str = None):
    if date_or_id is not None:
        try:
            date_object = datetime.datetime.strptime(date_or_id, "%Y-%m-%d").date()
        except ValueError:
            if date_or_id not in BLOCKS[lang].ALL_IDS:
                return render_template('404.html', lang=lang), 404
            proper = controller.get_proper_by_id(date_or_id, lang)
            date_or_id = None
            fmt_propers = format_propers([proper])
        else:
            day: Day = controller.get_day(date_object, lang)
            fmt_propers = format_propers(day.get_proper(), day)
        title = fmt_propers[0]['info']['title']
    else:
        title = None
        fmt_propers = None
    return render_template("proprium.html", title=title, propers=fmt_propers, date=date_or_id, proper_active=True, lang=lang)


@views.route("/ordo")
@views.route("/<string:lang>/ordo")
@infer_locale
def ordo(lang: str = LANGUAGE_ENGLISH):
    with open(os.path.join(ORDO_DIR, lang, 'ordo.json')) as fh:
        data = json.load(fh)
    return render_template("ordo.html", data=data, lang=lang)


@views.route("/canticum")
@views.route("/canticum/<string:proper_id>")
@views.route("/<string:lang>/canticum")
@views.route("/<string:lang>/canticum/<string:proper_id>")
@infer_locale
def canticum(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    index = supplement_index.get_canticum_index(lang)
    title = supplement_index.get_canticum_title(lang, proper_id) or _("Songs")
    try:
        supplement_yaml = get_supplement(lang, proper_id, "canticum")
    except SupplementNotFound:
        body = None
    else:
        body = supplement_yaml["body"]
    return render_template("supplement_nested.html", title=title, index=index, body=body, lang=lang)


@views.route("/oratio")
@views.route("/oratio/<string:proper_id>")
@views.route("/<string:lang>/oratio")
@views.route("/<string:lang>/oratio/<string:proper_id>")
@infer_locale
def oratio(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    index = supplement_index.get_oratio_index(lang)
    title = supplement_index.get_oratio_title(lang, proper_id) or _("Prayers")
    try:
        supplement_yaml = get_supplement(lang, proper_id, "oratio")
    except SupplementNotFound:
        body = None
    else:
        body = supplement_yaml["body"]
    return render_template("supplement_nested.html", title=title, index=index, body=body, lang=lang)


@views.route("/votive")
@views.route("/votive/<string:proper_id>")
@views.route("/<string:lang>/votive")
@views.route("/<string:lang>/votive/<string:proper_id>")
@infer_locale
def votive(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    index = TRANSLATION[lang].VOTIVE_MASSES
    proper_id = {i['ref']: i['id'] for i in index}.get(proper_id, proper_id)
    title = None
    fmt_propers = None
    if proper_id is not None:
        fmt_propers = get_pregenerated_proper(lang, proper_id)
        if not fmt_propers:
            proper = controller.get_proper_by_id(proper_id, lang)
            fmt_propers = format_propers([proper])
        title = fmt_propers[0]['info']['title']
    return render_template("votive.html", title=title, propers=fmt_propers, index=index, lang=lang)


@views.route("/supplement")
@views.route("/supplement/<string:resource>")
@views.route("/supplement/<subdir>/<string:resource>")
@views.route("/<string:lang>/supplement")
@views.route("/<string:lang>/supplement/<string:resource>")
@views.route("/<string:lang>/supplement/<subdir>/<string:resource>")
@infer_locale
def supplement(lang: str = LANGUAGE_ENGLISH, subdir: str = None, resource: str = None):
    if resource is None:
        return render_template_or_404(f"{lang}/supplement-main.html", lang=lang)
    try:
        supplement_yaml = get_supplement(lang, resource, subdir)
    except SupplementNotFound:
        return render_template_or_404("404.html", lang=lang), 404
    else:
        title = supplement_yaml["title"]
        html = supplement_yaml["body"]
        ref = request.args.get("ref")
        if ref is None or re.sub(r'[\w\-/]', '', ref) != "":
            ref = None
        return render_template_or_404("supplement.html", title=title, data=html, ref=ref, lang=lang)


@views.route("/icalendar")
def icalendar():
    return redirect("/supplement", code=302)


@views.route("/info")
@views.route("/<string:lang>/info")
@infer_locale
def info(lang: str = LANGUAGE_ENGLISH):
    return render_template_or_404(f"{lang}/info.html", lang=lang)


@views.route("/service-worker.js")
def service_worker():
    return send_from_directory(os.path.join(views.root_path, "static", "js"), "service-worker.js")


@views.route("/robots.txt")
def robots():
    return render_template_string("User-agent: *\nDisallow:")
